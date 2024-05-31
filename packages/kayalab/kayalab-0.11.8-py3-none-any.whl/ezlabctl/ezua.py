import json
import logging
from typing import Annotated
import typer

from ezlab.ezmeral import ezua
from ezlab.parameters import UA

app = typer.Typer(add_completion=True, no_args_is_help=True)

logger = logging.getLogger()
ch = logging.StreamHandler()
ch.setFormatter(
    logging.Formatter(
        "%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d: %(message)s",
        datefmt="%H:%M:%S",
    )
)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


@app.command(no_args_is_help=True)
def install(
    conf: Annotated[str, typer.Option("--settings", "-s")],
):
    """Create UA cluster

    Args:
        conf (str): path to settings json
    """

    with open(conf, "r") as f:
        config = json.load(f)

    print(
        f"Starting {config[UA]['clustername']} deployment with o: {config[UA]['orchestrator']}, c: {config[UA]['controller']}, w: {config[UA]['workers']}"
    )

    if ezua.precheck(config) and ezua.install(config) and ezua.deploy(config):
        print(f"{config[UA]['clustername']} is ready")
