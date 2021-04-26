"""
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Kareem Iskander, DevNet Developer Advocate"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

from dnacentersdk import DNACenterAPI
from dnacentersdk.exceptions import ApiError
import json
from rich import print
from rich.console import Console
from rich.table import Table
import random
from configparser import ConfigParser
from time import sleep

console = Console()
table = Table(show_header=True, header_style="bold magenta")
ip_address_range = "10.10.20.80-10.10.20.84"
global_creds_id = ["3eaff876-cf7e-4226-9af0-3901a5772334", "d34baa08-36ab-4b2b-8944-b8fae1af4669"]



"""
Programmatically create new site from JSON files in ./sites folder
"""
def render_site_info():
    console.print("[bold red] Building New Site...")
    with open('sites/area.json', 'r') as outfile:
        area = json.load(outfile)
        create_new_site(area)
        sleep(5)
        console.print("[bold cyan] {} Created! :thumbs_up:".format(area['site']['area']['name']))
    with open('sites/bldg.json', 'r') as outfile:
        bldg = json.load(outfile)
        create_new_site(bldg)
        sleep(5)
        console.print("[bold cyan] {} Building Added! :thumbs_up:".format(bldg['site']['building']['name']))
    with open('sites/floor.json', 'r') as outfile:
        floor = json.load(outfile)
        create_new_site(floor)
        sleep(5)
        console.print("[bold cyan] {} Added!".format(floor['site']['floor']['name']))
    """
    Kick off Site Discovery
    """
    init_discovery()  # Start Device Discovery


def create_new_site(site):
    global site_id
    try:
        resp = dnac.sites.create_site(payload=site)
        if site['type'] == "floor": # Capture site ID to be used to add discovered devices to it and set SITE_ID
            site_id = get_site_info(site['site']['floor']['parentName'] + "/" + site['site']['floor']['name'])
    except ApiError as e:
        print(e)
    else:
        return resp.response


def get_site_info(site_name):
    site_info = dnac.sites.get_site(name=site_name)
    return site_info['response'][0]['id']


"""
Kick off a new Auto Discovery job
"""
def init_discovery():
    discovery = dnac.network_discovery.start_discovery(
        discoveryType="Range", preferredMgmtIPMethod="UseLoopBack", ipAddressList=ip_address_range,
        protocolOrder="ssh,telnet", globalCredentialIdList=global_creds_id,
        name="Discovery-{}".format(random.randint(0, 1000))
    )
    task_info = dnac.task.get_task_by_id(discovery.response.taskId)
    task_progress = task_info.response.progress
    """
    Keep checking the Discovery job progress to make sure it has kicked off
    DNAC takes a couple of seconds to initiate Discovery
    """
    with console.status("[bold green]Kicking off Auto-Discovery...") as status:
        sleep(10)
        while task_progress == "Inventory service initiating discovery.":
            task_progress = dnac.task.get_task_by_id(discovery.response.taskId).response.progress
    console.print("[bold blue] Discovery Initiated! :thumbs_up:")
    """ 
    At this point Discovery Job is initiated. let's grab the Discovery ID and Fetch status of discovery 
    """
    get_discovery_status()


"""
Return the latest Discovery job info by asking for 1 record back starting from 1st Index
"""
def get_discovery_status():
    disco = dnac.network_discovery.get_discoveries_by_range(records_to_return=1,start_index=1)
    disco_id = disco.response[0].id # the discovery API call will only return 1 item in list
    disco_status = disco.response[0].discoveryStatus
    with console.status("[bold blue]Discovering Devices {}...".format(disco_status)) as status:
        while disco_status == "Active":
            disco_status= dnac.network_discovery.get_discoveries_by_range(records_to_return=1, start_index=1).response[0].discoveryStatus
            sleep(5)
    console.print("[bold blue] Discovery Completed!  :thumbs_up:")
    disco = dnac.network_discovery.get_discovery_by_id(id=disco_id)
    """
    Add Devices to a list
    """
    devices_list = disco.response.deviceIds.split(",")
    get_device_details(devices_list)


"""
Param: List of discovered devices 
Function to gather info based on discovered UUID and print finding in a table
"""
def get_device_details(discovered_devices_list):
    generate_table_hdr()
    for device in discovered_devices_list:
        device = dnac.devices.get_device_by_id(id=device)
        add_device_to_site(str(device.response.managementIpAddress), device.response.hostname)
        table.add_row(
          device.response.hostname,
          device.response.macAddress,
          device.response.serialNumber,
          device.response.softwareType,
          device.response.type,
          device.response.managementIpAddress,
          device.response.family,
          device.response.platformId
                        )
    console.print(table)


def add_device_to_site(ip, hostname):
    device_to_add = {"device": [{"ip": ip}]}
    console.print("[bold yellow] Assigning Discovered Device {} to site".format(hostname))
    info = dnac.sites.assign_device_to_site(site_id=site_id,payload=device_to_add)


def generate_table_hdr():
    table.add_column("Hostname")
    table.add_column("MacAdd")
    table.add_column("Serial Number")
    table.add_column("Software Type")
    table.add_column("type")
    table.add_column("IP Address")
    table.add_column("Family")
    table.add_column("Device")
    return table


if __name__ == '__main__':
    """
    Read config.ini file
    config.ini sits in the same directory as this project and looks something like this:
    [DNAC]
    username = your username
    password = your password
    server = DNAC url
    """

    dnac_creds = ConfigParser()
    dnac_creds.read("config.ini")

    dnac = DNACenterAPI(username=dnac_creds['DNAC']['username'], password=dnac_creds['DNAC']['password'], base_url=dnac_creds['DNAC']['server'])
    render_site_info()
    # dnac.network_discovery.delete_all_discovery()