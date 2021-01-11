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
import json
from configparser import ConfigParser

"""
This function handles getting device list
"""
def get_device_list():
    devices = dnac.devices.get_device_list()
    devicesuid_list = []
    for device in devices.response:
        if device.family == 'Switches and Hubs':
            devicesuid_list.append(device.id)
    print("Device Management IP {} ".format(device.managementIpAddress))
    cmd_run(devicesuid_list)


"""
This function handles command runner execution
"""
def cmd_run(device_list):
    for device in device_list:
        print("Executing Command on {}".format(device))
        run_cmd = dnac.command_runner.run_read_only_commands_on_devices(commands=["show run"], deviceUuids=[device])
        print("Task started! Task ID is {}".format(run_cmd.response.taskId))
        task_info = dnac.task.get_task_by_id(run_cmd.response.taskId)
        task_progress = task_info.response.progress
        print("Task Status : {}".format(task_progress))
        while task_progress == 'CLI Runner request creation':
            task_progress = dnac.task.get_task_by_id(run_cmd.response.taskId).response.progress
        task_progress= json.loads(task_progress)
        cmd_output = dnac.file.download_a_file_by_fileid(task_progress['fileId'], dirpath='file.json')
        print("Saving config for device ... \n")


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
    print("Auth Token: ", dnac.access_token)
    print("Gathering Device Info ... \n")
    get_device_list()

