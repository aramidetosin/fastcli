import click
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result

# from nornir_scrapli.tasks import send_configs as scrapli_send_configs
# from nornir_napalm.plugins.tasks import napalm_configure
from nornir_netmiko.tasks import netmiko_send_config
import ipaddress
from constants import config_file


def eigrp_config(task):
    eigrp_cms = []
    eigrp_advertised = task.host["eigrp_advertised"]
    for key, values in eigrp_advertised.items():
        cm = f"router eigrp {key}"
        eigrp_cms.append(cm)
        eigrp_cms.append("no auto")
        for v in values:
            nw = ipaddress.ip_network(v)
            cm = f"network {nw.network_address} {nw.hostmask}"
            eigrp_cms.append(cm)
    task.run(netmiko_send_config, config_commands=eigrp_cms)


@click.group(name="eigrp")
def cli_eigrp():
    """Command for EIGRP configuration"""
    pass


@cli_eigrp.command(
    name="configure", help="Configure EIGRP from the information defined in hosts.yaml"
)
@click.option("--device", help="Configure only the device", required=False)
@click.option(
    "--group",
    default="eigrp",
    show_default=True,
    help="Configure all devices belong to the group",
    required=False,
)
def run_eigrp_config(device, group):
    nr = InitNornir(config_file=f"{config_file}")
    if device:
        nr = nr.filter(name=f"{device}")
    if group:
        nr = nr.filter(F(groups__contains=f"{group}"))
    result = nr.run(task=eigrp_config)
    print_result(result)
