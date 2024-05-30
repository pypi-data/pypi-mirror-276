"""
This is the network_builder module. 
It contains classes and functions to load device and task data from files and handle exceptions.
"""

import yaml
import argparse
import netmiko

class UnimplementedDeviceType(Exception):
    """Exception raised when the device system type is not implemented.

    Attributes:
        message -- explanation of the error
    """
    pass

class FileLoader:
    """Class for loading device and task data from files.

    Attributes:
        device_file_path -- path to the device data file
        tasks_file_path -- path to the tasks data file
        device_data -- data loaded from the device data file
        tasks_data -- data loaded from the tasks data file
    """
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.device_data = None
        self.tasks_data = None

    def load_config_file(self):
        with open(self.config_file_path, 'r') as config_file:
            self.device_data = yaml.safe_load(config_file)
            return self.device_data

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.device_data = None
        self.tasks_data = None

    def load_config_file(self):
        with open(self.config_file_path, 'r') as config_file:
            self.device_data = yaml.safe_load(config_file)
            return self.device_data

class TaskManager:
    """Class for managing tasks.

    Attributes:
        taskname -- name of the task
        taskdescription -- description of the task
        target -- target of the task
        command -- command of the task
        arguments -- arguments of the task
    """
    def __init__(self, taskname, taskdescription, target, command):
        self.taskname = taskname
        self.taskdescription = taskdescription
        self.target = target
        self.command = command

class CommandManager:
    """
    The CommandManager class is responsible for managing and executing commands on network devices.

    Attributes:
        name (str): The name of the network device.
        ip (str): The IP address of the network device.
        port (int): The port number to connect to on the network device.
        device_type (str): The type of the network device (e.g., 'ciscoios').
        username (str): The username to use when connecting to the network device.
        password (str): The password to use when connecting to the network device.

    Methods:
        send_command(str): Sends a command to the network device and returns the output.
        send_config(list): Sends a list of configuration commands to the network device.
    """
    def __init__(self, name, ip, port, device_type, username, password):
        self.name = name
        self.ip = ip
        self.port = port
        self.device_type = device_type
        self.username = username
        self.password = password

    def send_command(self, command, username, password):
        try:
            if self.device_type == 'cisco_ios':
                connection = netmiko.ConnectHandler(
                    device_type=self.device_type,
                    ip=self.ip,
                    port=self.port,
                    username=username,
                    password=password
                )
                output = connection.send_command(command)
                print(output)
                connection.disconnect()
            else:
                raise UnimplementedDeviceType(f'{self.device_type} is not implemented')
        except Exception as e:
            print(f'Error: {e}')

    def send_config(self, config, username, password):
        try:
            if self.device_type == 'cisco_ios':
                connection = netmiko.ConnectHandler(
                    device_type=self.device_type,
                    ip=self.ip,
                    port=self.port,
                    username=username,
                    password=password
                )
                output = connection.send_config_set(config)
                print(output)
                connection.disconnect()
            else:
                raise UnimplementedDeviceType(f'{self.device_type} is not implemented')
        except Exception as e:
            print(f'Error: {e}')

def main(config_file):
    """
    The main function is the entry point of the network builder program.

    It loads a configuration file, creates a list of CommandManager objects (representing network devices) 
    and a list of TaskManager objects (representing tasks to be performed on the devices). 

    For each task in the tasks list, it finds the corresponding device in the devices list and executes 
    the task's command on the device. If the task has additional arguments, it sends those as well.

    If a task's target device is not found in the devices list, or if the username or password is incorrect, 
    it prints an error message and continues to the next task.

    Parameters:
    config_file (str): The path to the configuration file.
    """
    file_loader = FileLoader(config_file_path=config_file)
    config_file = file_loader.load_config_file()

    device_list = []
    tasks_list = []

    devices = config_file['devices']
    for device in devices:
        name = device['name']
        ip = device['ip']
        port = device['port']
        device_type = device['type']
        password = device['password']
        username = device['username']

        network_device = CommandManager(name, ip, port, device_type, username, password)
        device_list.append(network_device)

    tasks = config_file['tasks']
    for task in tasks:
        name = task['name']
        description = task['description']
        target = task['device']
        commands = task['commands']

        for command in commands:
            task = TaskManager(name, description, target, command)
            tasks_list.append(task)

    for task in tasks_list:
        for device in device_list:
            if device.name == task.target:
                dev = CommandManager(device.name, device.ip, device.port, device.device_type, device.username, device.password)
                dev.send_command(task.command, device.username, device.password)
                if hasattr(task, 'arguments'):
                    dev.send_command(f'{task.command} {task.arguments}')
            else:
                print(f'Device {task.target} not found, or username: {device.username} or password: {device.password} is incorrect.')
                pass
