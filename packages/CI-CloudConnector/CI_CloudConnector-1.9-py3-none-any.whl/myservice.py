import os
import sys
import time

import psutil
import win32api
import win32con
import win32serviceutil
import win32service
import win32event
import subprocess

import logic
import main

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CloudConnectorService"
    _svc_display_name_ = "CloudConnectorService"
    _svc_failure_actions_ = "restart/10000"  # Restart the service after 1 minute if it fails

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        try:
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
                logic.ci_print('observer.stop()')
                observer.stop()
                observer.join()
                logic.ci_print("Observer has been stopped.")
        except Exception as e:
            # Log or handle any exceptions
            logic.ci_print(f"Exception in SvcDoRun: {e}")

        # Wait for the stop event
        wait_result = win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
        if wait_result == win32event.WAIT_OBJECT_0:
            # Stop event has been signaled
            return

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

        main.serviceStop()
        time.sleep(2)  # Allow some time for the service to stop gracefully

        logic.ci_print('Service stop requested.')
        win32event.SetEvent(self.stop_event)

        # Exit the service process with code -1
        #raise RuntimeError("stop the service with error")



        #time.sleep(20)
        #self.SvcTerminate()

    def ServiceUpdated(self):




        logic.ci_print('Service updated, stopping service...')

        main.serviceStop()
        time.sleep(2)
        os._exit(1)

        self.SvcStop()




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
        except Exception as e:
            print(f"Exception in TerminateProcess: {e}")


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
