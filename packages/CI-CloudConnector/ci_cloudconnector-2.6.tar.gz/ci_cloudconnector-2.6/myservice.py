import logging
import os
import time
import subprocess
import win32api
import win32con
import win32serviceutil
import win32service
import win32event
import main
from logging.handlers import RotatingFileHandler

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CloudConnectorService"
    _svc_display_name_ = "CloudConnectorService"
    _svc_failure_actions_ = "restart/10000"  # Restart the service after 1 minute if it fails

    def __init__(self, args):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(funcName)s - (%(lineno)d) - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        rotating_handler = RotatingFileHandler(
            filename='CloudConnectorService.log',
            mode="a",
            maxBytes=5 * 1024 * 1024,
            backupCount=10,
            encoding=None,
            delay=0,
        )

        rotating_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(funcName)s - (%(lineno)d) - %(levelname)s - %(message)s')
        rotating_handler.setFormatter(formatter)

        logging.getLogger().addHandler(rotating_handler)

        # Now initialize other attributes
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.logger = logging.getLogger(__name__)


    def SvcDoRun(self):
        self.logger.info("Service is starting.")
        try:
            # Activate the virtual environment
            venv_path = 'venv'  # Adjust the path to your virtual environment
            activate_script = os.path.join(venv_path, 'Scripts', 'activate')  # On Windows

            # Run the activation script in a new subprocess
            subprocess.run([activate_script], check=True, shell=True)

            self.logger.info("Virtual environment activated.")

            main.init()
            main.args([0, 'Start'])

            current_script_dir = os.path.dirname(os.path.abspath(__file__))
            logic_file = os.path.join(current_script_dir, "logic.py")
            observer = main.monitor_main_file(logic_file, self)

            try:
                while main.service_stop == 0:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            finally:
                observer.stop()
                observer.join()
                self.logger.info("Observer has been stopped.")

        except Exception as e:
            self.logger.error(f"Exception in SvcDoRun: {e}")

        # Wait for the stop event
        wait_result = win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
        if wait_result == win32event.WAIT_OBJECT_0:
            self.logger.info("Stop event signaled. Service is stopping.")
            return

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

        main.serviceStop()
        time.sleep(2)  # Allow some time for the service to stop gracefully

        self.logger.info('Service stop requested.')
        win32event.SetEvent(self.stop_event)

    def ServiceUpdated(self):
        self.logger.info('Service updated, stopping service...')
        self.SvcStop()
        os._exit(1)

    def SvcTerminate(self):
        time.sleep(1)  # Adjust the delay time as needed
        pid = self.GetPID()
        self.TerminateProcess(pid)
        win32event.SetEvent(self.stop_event)

    def GetPID(self):
        return win32api.GetCurrentProcessId()

    def TerminateProcess(self, pid):
        try:
            hProcess = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid)
            win32api.TerminateProcess(hProcess, 0)
            win32api.CloseHandle(hProcess)

            self.logger.info(f"Process {pid} terminated successfully.")

        except Exception as e:
            self.logger.error(f"Exception in TerminateProcess: {e}")

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
