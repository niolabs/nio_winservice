"""

    NIO Windows Service

"""
from signal import CTRL_BREAK_EVENT
import subprocess
import win32service
import win32event
import win32api
import win32console
import win32serviceutil


class NIOWinService(win32serviceutil.ServiceFramework):

    project_path = None
    name = 'nio_{}'.format(project_path.split('\\')[-1])
    _svc_display_name_ = name
    _svc_name_ = name
    _svc_description_ = project_path

    def __init__(self, *args):
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def log(self, msg):
        import servicemanager
        servicemanager.LogInfoMsg(str(msg))

    def error(self, msg):
        import servicemanager
        servicemanager.LogErrorMsg(str(msg))

    def SvcDoRun(self):
        self.log('Triggered ...')
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.log('Starting ...')
            self.start()
            win32event.WaitForSingleObject(self.hWaitStop,
                                           win32event.INFINITE)
            self.log('Exit')
        except Exception as x:
            self.error('Exception : %s' % str(x))
            self.SvcStop()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log('Stopping ....')
        self.stop()
        self.log('Stopped')
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def start(self):
        self.log('Launching nio Daemon')
        win32console.AllocConsole()
        self.process = subprocess.Popen(
            ['niod'],
            cwd=self.project_path,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

    def stop(self):
        try:
            self.log('Stopping nio Daemon')
            if self.process:
                win32api.GenerateConsoleCtrlEvent(CTRL_BREAK_EVENT,
                                                  self.process.pid)
                self.log('Signal sent to stop nio')
        except Exception as x:
            self.error('Exception stopping: %s' % str(x))

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(NIOWinService)
