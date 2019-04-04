## Install nio as Windows Service

### Requirements:
- Command Prompt with administrator privileges
- [pywin32](https://pypi.org/project/pywin32/) (should have been installed with nio)
- `nio_winservice.py` from this repo
- A nio project

### Install:
- Open `nio_winservice.py` with a text editor, and near the top of the `NIOWinService` class:
  - Enter the abosulte path to your nio project for the value of `project_path` , for example: `project_path = "C:\\Users\\<user>\\nio\\projects\\my_project"`
  - Enter the absolute path to the installed `niod` executable. If you are using a [virtual environment](https://docs.n.io/deployment/best-practices/) (highly recommended) it will be inside the environment's directory, for example: `niod_path = "C:\\Users\\<user>\\nio\\env\\Scripts\\niod.exe"`
  - **Note the double backslashes!**
- In a (Administrator) Command Prompt:
  - Run `python3 nio_winservice.py --startup auto install`, or
  - If the service is going to be run as a user other than `Local System`, `python3 nio_winservice.py --startup auto --username <user> --password <pass> install`
- `nio_<project>` has been installed, but not started. It will start automatically in the future.

### Use:
- Control the service manually from the command line with `net start|stop nio_<project>`
- Or, Open `Control Panel > System and Security > Adminstrative Tools > Services`

### Remove:
- Run `python3 nio_winservice remove`
