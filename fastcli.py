import click
from nafc.api.interfaces import cli_interfaces
from nafc.api.show import cli_get
from nafc.api.ospf import cli_ospf
from nafc.api.eigrp import cli_eigrp
from nafc.api.rip import cli_rip


@click.group()
def cli():
    """Command line tool to interact with CISCO SDWAN vManage.
    """
    pass


cli.add_command(cli_interfaces)
cli.add_command(cli_get)
cli.add_command(cli_ospf)
cli.add_command(cli_eigrp)
cli.add_command(cli_rip)


if __name__ == "__main__":
    cli()
