"""Handles the "search" command."""

import time
from typing import Dict, List

import click
from requests.models import Response
from tabulate import tabulate

import spyctl.config.configs as cfg
import spyctl.spyctl_lib as lib
from spyctl import api, cli


@click.command("search", cls=lib.CustomCommand, epilog=lib.SUB_EPILOG)
@click.argument("schema", required=False, type=str)
@click.argument("query", required=False, type=str)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "-l",
    "--list-schemas",
    is_flag=True,
    help="",
)
@click.option(
    "-d",
    "--describe",
    is_flag=True,
    help="",
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(
        [
            lib.OUTPUT_YAML,
            lib.OUTPUT_JSON,
            lib.OUTPUT_NDJSON,
            lib.OUTPUT_DEFAULT,
        ]
    ),
    default=lib.OUTPUT_DEFAULT,
    help="Output format.",
)
@click.option(
    "-t",
    "--start-time",
    "st",
    help="Start time of the query. Default is 24 hours ago.",
    default="24h",
    type=lib.time_inp,
)
@click.option(
    "-e",
    "--end-time",
    "et",
    help="End time of the query. Default is now.",
    default=time.time(),
    type=lib.time_inp,
)
def search(schema, query, output, st, et, **kwargs):
    """Search for objects in the given schema."""
    handle_search(schema, query, output, st, et, **kwargs)


def handle_search(schema, query, output, st, et, **kwargs):
    """Handle the 'search' command."""
    list_schemas = kwargs.get("list_schemas")
    describe = kwargs.get("describe")
    if list_schemas or describe or not any([schema, query]):
        handle_search_schema(output, schema)
        return
    if not query:
        lib.err_exit(
            "Use --describe to view available search fields, or provide a query."  # noqa
        )
    if output == lib.OUTPUT_DEFAULT:
        output = lib.OUTPUT_NDJSON
    ctx = cfg.get_current_context()
    results = api.search_athena(
        *ctx.get_api_data(), schema, query, start_time=st, end_time=et
    )
    for result in results:
        cli.show(result, output=output)


def handle_search_schema(output: str, schema: str = None):
    """Handle the 'search-schema' command."""
    ctx = cfg.get_current_context()
    api_url, api_key, org_uid = ctx.get_api_data()
    url = f"{api_url}/api/v1/org/{org_uid}/search/schema/"
    response = api.get(url, api_key)
    if schema:
        handle_specific_schema(output, schema, response)
        return
    schemas = list(response.json())
    schemas.sort()
    if lib.OUTPUT_DEFAULT:
        output = lib.OUTPUT_RAW
        lines = ["Available Schemas:"]
        lines.extend(["  " + s for s in schemas])
        schemas = "\n".join(lines)
    cli.show(schemas, output=output)


def handle_specific_schema(output: str, schema, response: Response):
    """Handle the 'search-schema' command for a specific schema."""
    data = response.json()
    schema_data = data.get(schema)
    if not schema_data:
        available = "\n" + "\n".join(["  " + s for s in data])
        cli.err_exit(
            f"{schema} is not a valid schema for athena search."
            f" Available schemas are:{available}"
        )
    if lib.OUTPUT_DEFAULT:
        output = lib.OUTPUT_RAW
        lines = [schema]
        lines.append("  Fields:")
        lines.extend(__create_description_table(schema_data))
        if "joins" in schema_data:
            lines.append("  Joins:")
            lines.extend(__create_join_table(schema_data))
        schema_data = "\n".join(lines)
    else:
        schema_data = {schema: schema_data}
    cli.show(schema_data, output=output)


def __create_description_table(schema_data: Dict) -> List[str]:
    """Create a table of the schema description"""
    headers = ["Field", "Type", "Description"]
    data = []
    for field, desc_data in sorted(schema_data["descriptions"].items()):
        s_type = schema_data["projection"].get(field)
        if s_type:
            data.append(
                [
                    field,
                    f"({s_type}):",
                    desc_data["desc"],
                ]
            )
    rv = tabulate(data, headers=headers, tablefmt="plain").splitlines()
    rv = [f"    {line}" for line in rv[2:]]
    return rv


def __create_join_table(schema_data: Dict) -> List[str]:
    """Create a table of the schema joins"""
    headers = ["Field", "New Schema"]
    data = []
    for field, join_data in sorted(schema_data["joins"].items()):
        data.append([f"{field}:", join_data["new_schema"]])
    rv = tabulate(data, headers=headers, tablefmt="plain").splitlines()
    rv = [f"    {line}" for line in rv[2:]]
    return rv
