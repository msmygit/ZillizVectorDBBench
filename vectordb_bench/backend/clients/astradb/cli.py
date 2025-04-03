import os
from typing import Annotated, Unpack

import click
from pydantic import SecretStr

from vectordb_bench.backend.clients import DB
from vectordb_bench.cli.cli import (
    CommonTypedDict,
    cli,
    click_parameter_decorators_from_typed_dict,
    run,
)

class AstraDBTypedDict(CommonTypedDict):
    astra_db_id: Annotated[
        str,
        click.option("--astra-db-id", type=str, help="Astra DB UUID", required=True),
    ]
    astra_token: Annotated[
        str,
        click.option(
            "--astra-token",
            type=str,
            help="Astra DB application token",
            default=lambda: os.environ.get("ASTRA_DB_APPLICATION_TOKEN", ""),
            show_default="$ASTRA_DB_APPLICATION_TOKEN",
            required=True
        ),
    ]
    scb_path: Annotated[
        str,
        click.option("--scb-path", type=str, help="Astra DB cluster Secure Connect Bundle", required=False),
    ]
    astra_env: Annotated[
        str,
        click.option("--astra-env", type=str, help="Astra DB environment. Valid values: dev/test/prod", required=False),
    ]
    keyspace: Annotated[
        str,
        click.option("--keyspace", type=str, help="Astra DB cluster keyspace. Default is 'default_keyspace'", required=False),
    ]


@cli.command()
@click_parameter_decorators_from_typed_dict(AstraDBTypedDict)
def AstraDB(**parameters: Unpack[AstraDBTypedDict]):
    from .config import AstraDBConfig

    run(
        db=DB.AstraDB,
        db_config=AstraDBConfig(
            astra_db_id=parameters["astra_db_id"],
            astra_token=SecretStr(parameters["astra_token"]),
            scb_path=parameters["scb_path"],
            keyspace=parameters["keyspace"],
            astra_env=parameters["astra_env"],
        ),
        **parameters,
    )