import typer
from typing_extensions import Annotated
import pandas as pd
from dynatrace import Dynatrace
from dynatrace.environment_v2.extensions import MonitoringConfigurationDto
from rich.progress import track
from rich import print

import json
from typing import Optional, List

app = typer.Typer()

EF1_EXTENSION_ID = "custom.remote.python.remote_agent"
EF2_EXTENSION_ID = "custom:remote-unix"


def build_authentication_from_ef1(ef1_config: dict):
    authentication = {"username": ef1_config.get("username")}

    password = ef1_config.get("password")
    ssh_key_contents = ef1_config.get("ssh_key_contents")
    ssh_key_file = ef1_config.get("ssh_key_file")
    ssh_key_passphrase = ef1_config.get("ssh_key_passphrase", "")

    # doesn't seem like a good way to pre-build the auth since the secrets (password or key contents) will always be null
    if True:
        authentication.update(
            {"password": "password", "scheme": "password", "useCredentialVault": False}
        )
    elif ssh_key_contents:
        authentication.update(
            {
                "ssh_key_contents": ssh_key_contents,
                "passphrase": ssh_key_passphrase,
                "scheme": "ssh_key_contents",
            }
        )
    elif ssh_key_file:
        authentication.update(
            {
                "key_path": ssh_key_file,
                "passphrase": ssh_key_passphrase,
                "scheme": "key_path",
            }
        )
    return authentication


def build_ef2_config_from_ef1(
    version: str,
    description: str,
    skip_endpoint_authentication: bool,
    ef1_configurations: pd.DataFrame,
):

    # {
    #     "os": "Generic Linux",
    #     "disable_iostat": "false",
    #     "ssh_key_contents": None,
    #     "top_threads_mode": "false",
    #     "log_level": "INFO",
    #     "persist_ssh_connection": "true",
    #     "mounts_to_exclude": "",
    #     "additional_props": "key=value\ntest=tess1",
    #     "ssh_key_file": "",
    #     "ssh_key_passphrase": None,
    #     "hostname": "172.26.231.39",
    #     "password": None,
    #     "disable_rsa2": "false",
    #     "fail_on_initial_error": "false",
    #     "mounts_to_include": ".*\nabc\ndef",
    #     "port": "22",
    #     "process_filter": "ssh;SSH",
    #     "custom_path": "",
    #     "alias": "ubuntu",
    #     "max_channel_threads": "5",
    #     "username": "jpwk",
    #     "group": "testing",
    # }

    base_config = {
        "enabled": False,
        "description": description,
        "version": version,
        "featureSets": ["default"],
        "pythonRemote": {"endpoints": []},
    }

    print(
        f"{len(ef1_configurations)} endpoints will attempt to be added to the monitoring configuration."
    )
    for index, row in ef1_configurations.iterrows():
        enabled = row["enabled"]
        properties: dict = json.loads(row["properties"])
        endpoint_configuration = {
            "enabled": enabled,
            "hostname": properties.get("hostname"),
            "port": int(properties.get("port")),
            "alias": properties.get("alias"),
            "os": properties.get("os"),
            "additional_properties": [],
            "top_processes": {"top_count": 10, "report_log_events": False},
            "process_filters": [],
            "mount_filters": [],
            "advanced": {
                "persist_ssh_connection": (
                    "REUSE"
                    if bool(properties.get("persist_ssh_connection"))
                    else "RECREATE"
                ),
                "disable_rsa2": (
                    "DISABLE" if bool(properties.get("disable_rsa2")) else "ENABLE"
                ),
                "top_mode": (
                    "THREADS_MODE"
                    if bool(properties.get("top_threads_mode"))
                    else "DEFAULT"
                ),
                "max_channel_threads": int(properties.get("max_channel_threads")),
                "log_output": False,
            },
        }

        if not skip_endpoint_authentication:
            endpoint_configuration["authentication"] = build_authentication_from_ef1(
                properties
            )

        if properties.get("custom_path", None):
            endpoint_configuration["advanced"]["custom_path"] = properties[
                "custom_path"
            ]

        if properties.get("additional_props"):
            for prop in properties.get("additional_props", "").split("\n"):
                key, value = prop.split("=")
                endpoint_configuration["additional_properties"].append(
                    {"key": key, "value": value}
                )

        if properties.get("process_filter"):
            for process in properties.get("process_filter").split("\n"):
                pattern, group_key = process.split(";")
                endpoint_configuration["process_filters"].append(
                    {"group_key": group_key, "pattern": pattern, "user": None}
                )

        if properties.get("mounts_to_include"):
            for pattern in properties.get("mounts_to_include").split("\n"):
                endpoint_configuration["mount_filters"].append(
                    {"filter_type": "include", "pattern": pattern}
                )

        if properties.get("mounts_to_exclude"):
            for pattern in properties.get("mounts_to_exclude").split("\n"):
                endpoint_configuration["mount_filters"].append(
                    {"filter_type": "exclude", "pattern": pattern}
                )

        base_config["pythonRemote"]["endpoints"].append(endpoint_configuration)

    return base_config


@app.command(help="Pull EF1 remote unix configurations into a spreadsheet.")
def pull(
    dt_url: Annotated[str, typer.Option(envvar="DT_URL")],
    dt_token: Annotated[str, typer.Option(envvar="DT_TOKEN")],
    output_file: Optional[str] = None or f"{EF1_EXTENSION_ID}.xlsx",
    index: Annotated[
        Optional[List[str]],
        typer.Option(
            help="Specify what property to group sheets by. Can be specified multipl times."
        ),
    ] = ["group"],
):
    dt = Dynatrace(dt_url, dt_token)
    configs = dt.extensions.list_instances(extension_id=EF1_EXTENSION_ID)
    full_configs = []

    for config in track(configs, description="Pulling EF1 configs"):
        config = config.get_full_configuration(EF1_EXTENSION_ID)
        full_config = config.json()
        properties = full_config.get("properties", {})
        for key in properties:
            if key in index or key == "username":
                full_config.update({key: properties[key]})
        full_config["properties"] = json.dumps(properties)
        full_configs.append(full_config)

    writer = pd.ExcelWriter(
        output_file,
        engine="xlsxwriter",
    )
    df = pd.DataFrame(full_configs)
    df_grouped = df.groupby(index)
    for key, group in df_grouped:
        key = [subgroup for subgroup in key if subgroup]
        group.to_excel(
            writer, sheet_name="-".join(key) or "Default", index=False, header=True
        )
    writer.close()
    print(f"Exported configurations available in '{output_file}'")


@app.command()
def push(
    dt_url: Annotated[str, typer.Option(envvar="DT_URL")],
    dt_token: Annotated[str, typer.Option(envvar="DT_TOKEN")],
    input_file: Annotated[
        str,
        typer.Option(
            help="The location of a previously pulled/exported list of EF1 endpoints"
        ),
    ],
    sheet: Annotated[
        str,
        typer.Option(
            help="The name of a sheet in a previously pulled/exported list of EF1 endpoints"
        ),
    ],
    ag_group: Annotated[str, typer.Option()],
    version: Annotated[
        str,
        typer.Option(
            help="The version of the EF2 extension you would look to create this configuration for"
        ),
    ],
    print_json: Annotated[
        bool, typer.Option(help="Print the configuration json that will be sent")
    ] = False,
    do_not_create: Annotated[
        bool,
        typer.Option(
            help="Does every step except for sending the configuration. Combine with '--print-json' to review the config that would be created"
        ),
    ] = False,
):
    """
    Convert and push the EF1 remote unix configurations to the EF2 extension.
    """
    xls = pd.ExcelFile(input_file)
    df = pd.read_excel(xls, sheet)

    config = build_ef2_config_from_ef1(version, sheet, False, df)
    if print_json:
        print(json.dumps(config))

    if not ag_group.startswith("ag_group-"):
        print(
            f"Appending 'ag_group-' to provided hostname. Result: 'ag_group-{ag_group}'"
        )
        ag_group = f"ag_group-{ag_group}"

    dt = Dynatrace(dt_url, dt_token, print_bodies=False)
    config = MonitoringConfigurationDto(ag_group, config)

    if not do_not_create:
        try:
            result = dt.extensions_v2.post_monitoring_configurations(
                EF2_EXTENSION_ID, [config]
            )[0]
            print(f"Configs created successfully. Response: {result['code']}")
            base_url = dt_url if not dt_url.endswith("/") else dt_url[:-1]
            print(
                f"Link to monitoring configuration: {base_url}/ui/hub/ext/listing/registered/{EF2_EXTENSION_ID}/{result['objectId']}/edit"
            )
        except Exception as e:
            print(f"[bold red]{e}[/bold red]")


if __name__ == "__main__":
    app()
