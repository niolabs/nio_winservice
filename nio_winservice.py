""" NIO Windows Service

    When run, this file creates an interface between a Windows operating
    system and an installed nio instance. The installed Windows service will
    start automatically.

    See below for required configuration at the top of NIOWinService class.

"""

from signal import CTRL_BREAK_EVENT
import servicemanager
import subprocess
import win32service
import win32event
import win32api
import win32console
import win32serviceutil


class NIOWinService(win32serviceutil.ServiceFramework):

    """ Configure the path to your nio project and `niod` executable.

        Running `where niod` in a command prompt will return the path to the
        installed exectuable, making sure that any virtual environment is
        activated.

    """

    # CONFIGURATION
    # Must include quotes and double backslashes
    project_path = "C:\\Users\\<user>\\nio\\projects\\my_project"
    niod_path = "C:\\Users\\<user>\\nio\\env\\Scripts\\niod.exe"
    # END CONFIGURATION
    # Do not edit anything below this line

    name = 'nio_{}'.format(project_path.split('\\')[-1])
    _svc_display_name_ = name
    _svc_name_ = name
    _svc_description_ = project_path

    def __init__(self, *args):
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def log(self, msg):
        servicemanager.LogInfoMsg(str(msg))

    def error(self, msg):
        servicemanager.LogErrorMsg(str(msg))

    def SvcDoRun(self):
        self.log('Triggered ...')
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.log('Starting ...')
            self.start()
            win32event.WaitForSingleObject(
                self.hWaitStop,
                win32event.INFINITE)
            self.log('Exit')
        except Exception as e:
            self.error('Exception starting: {}'.format(e))
            self.SvcStop()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log('Stopping ...')
        self.stop()
        self.log('Stopped.')
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def start(self):
        self.log('Launching nio process')
        win32console.AllocConsole()
        self.process = subprocess.Popen(
            [self.niod_path],
            cwd=self.project_path,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

    def stop(self):
        try:
            self.log('Stopping nio process')
            if self.process:
                win32api.GenerateConsoleCtrlEvent(
                    CTRL_BREAK_EVENT,
                    self.process.pid)
                self.log('CTRL_BREAK_EVENT sent')
        except Exception as e:
            self.error('Exception stopping: {}'.format(e))


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(NIOWinService)
