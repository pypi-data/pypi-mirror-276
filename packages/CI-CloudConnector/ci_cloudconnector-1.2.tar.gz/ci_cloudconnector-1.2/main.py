import signal
import threading

import win32serviceutil

import logic
import sys
import subprocess
import shutil
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer
from datetime import datetime

upgrade_counter = 0
server_version = ""
repeating_timer = None
service_stop = 0


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False



def update_and_run(script_path, package_name, package_version):
    try:
        logic.ci_print(f'package_version: {package_version}')

        current_script_dir = os.path.dirname(os.path.abspath(__file__))

        if package_version == '':
            # Upgrade the package
            command = ["pip", "install", "--upgrade", package_name]
        else:
            # Install or upgrade the package with specific version
            command = ["pip", "install", "--force-reinstall", f"{package_name}=={package_version}"]

        logic.ci_print(f"Running command: {' '.join(command)}")

        try:
            # Run the command
            result = subprocess.run(command, capture_output=True, text=True)
            logic.ci_print(f"Command output: {result.stdout}")
            logic.ci_print(f"Command error: {result.stderr}")

            if result.returncode != 0:
                logic.ci_print(f"Command failed with exit status {result.returncode}")
                return


        except subprocess.CalledProcessError as e:
            # Print error message
            logic.ci_print(f"Command failed with exit status {e.returncode}")
            logic.ci_print(f"stdout: {e.stdout}")
            logic.ci_print(f"stderr: {e.stderr}")
            return

        # Print success message
        logic.ci_print(f"Package {package_name}=={package_version} installed successfully")

        # Locate the installed package
        command2 = ["pip", "show", package_name]
        logic.ci_print(f"Running command2: {' '.join(command2)}")

        package_info = subprocess.check_output(command2).decode()
        package_location = None
        for line in package_info.splitlines():
            if line.startswith("Location:"):
                package_location = line.split(": ")[1]
                break



        if package_location is None:
            logic.ci_print("Could not determine the package location.")
            return

        # Construct the path to the installed package
        installed_package_path = package_location

        logic.ci_print('package_info: ' + package_info)
        logic.ci_print('installed_package_path: ' + installed_package_path)

        logic_source = os.path.join(installed_package_path, "logic.py")
        main_source = os.path.join(installed_package_path, "main.py")
        myservice_source = os.path.join(installed_package_path, "myservice.py")
        setup_source = os.path.join(installed_package_path, "setup.py")

        if not os.path.isfile(logic_source) or not os.path.isfile(main_source):
            print(f"logic.py or main.py not found in {installed_package_path}.")
            return

        # Copy files to the destination
        shutil.copy(logic_source, current_script_dir)
        shutil.copy(main_source, current_script_dir)
        shutil.copy(myservice_source, current_script_dir)
        shutil.copy(setup_source, current_script_dir)


        print(f"Copied logic.py and main.py to {current_script_dir}")


    except subprocess.CalledProcessError as e:
        logic.ci_print(f"An error occurred: {e}")


def upgrade_version(new_version="", current_version=""):
    try:
        update_and_run("main.py", "CI_CloudConnector", new_version)

    except Exception as ex:
        logic.handleError("Upgrade version Error: ", ex)


def MainLoopTimer():
    print(f"MainLoopTimer: {str(datetime.now())}")
    global repeating_timer

    if repeating_timer:
        repeating_timer.stop()

    logic.ci_print(f"VERSION: {logic.getLocalVersion()}")
    if service_stop == 1:
        repeating_timer = None
        return

    try:
        MainLoop()
    except Exception as e:
        logic.ci_print(f"MainLoopTimer::Error: {e}", "ERROR")

    if repeating_timer:
        repeating_timer.start()
    else:
        repeating_timer = RepeatedTimer(5, MainLoopTimer)


def MainLoop():
    global server_version
    global upgrade_counter

    try:
        # Get version and update if needed
        logic.get_cloud_version()
        local_ver = str(logic.getLocalVersion())
        update_to_ver = str(logic.getServerSugestedVersion())

        # To prevent upgrading too much in case of a problem, count upgrade attempts and stop when it's too big.
        # If the version changes, try again.
        if server_version != update_to_ver:
            server_version = update_to_ver
            upgrade_counter = 0

        if str(update_to_ver) == "None":
            update_to_ver = ""

        if (bool(update_to_ver != "") & bool(update_to_ver != local_ver) & bool(upgrade_counter < 10)):
            upgrade_counter += 1
            logic.ci_print(
                f"Starting auto upgrade from: {local_ver} to: {update_to_ver}, Upgrade count: {upgrade_counter}")
            upgrade_version(update_to_ver, local_ver)

        logic.Main()
    except Exception as inst:
        logic.ci_print(f"MainLoop::Error {inst}", "ERROR")


def StartMainLoop():
    global repeating_timer
    try:
        repeating_timer = RepeatedTimer(5, MainLoopTimer)
    except Exception as inst:
        logic.ci_print("StartMainLoop::Error " + str(inst))


def args(argv):
    if len(argv) > 1 and argv[1] == "Start":
        StartMainLoop()


class MainFileChangeHandler(FileSystemEventHandler):
    def __init__(self, main_file, service):
        super().__init__()
        self.main_file = main_file
        self.myService = service

    def on_modified(self, event):
        if event.src_path.endswith(self.main_file):
            logic.ci_print("Main file has been modified. Signaling service to restart...")


            # Stop the service
            self.myService.ServiceUpdated()
            logic.ci_print("Service stopped. You may restart it if necessary.")



def monitor_main_file(main_file, service):
    observer = Observer()

    event_handler = MainFileChangeHandler(os.path.basename(main_file), service)
    observer.schedule(event_handler, path=os.path.dirname(main_file), recursive=False)

    observer.start()
    return observer


def init():
    logic.create_directories_if_missing()
    logic.initialize_config()
    set_service_restart_delay("CloudConnectorService", 10000)



def serviceStop():
    global service_stop
    service_stop = 1
    logic.ci_print("Service stop requested.")



def set_service_restart_delay(service_name, delay_milliseconds):
    command = f'sc failure {service_name} reset= 0 actions= restart/{delay_milliseconds}'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Restart delay for service '{service_name}' set to {delay_milliseconds} milliseconds.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting restart delay for service '{service_name}': {e}")



if __name__ == '__main__':
    init()
    args(sys.argv)
    #args([0, 'Start'])
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(current_script_dir, "logic.py")
    monitor_main_file(main_file)