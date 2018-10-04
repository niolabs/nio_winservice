## Install nio as Windows Service

### Requirements:
- [pywin32](https://pypi.org/project/pywin32/) (should have been installed with nio)
- `nio_winservice.py` from this repo
- A nio project

### Install:
By default Windows will install the new service to be run by the `Local System` account, which requires that Python and niod be in the path for that account. Launch `regedit` and navigate to `Computer > HKEY_LOCAL_MACHINE > SYSTEM > CurrentControlSet > Control > Session Manager > Environment`. Modify `Path` and, using semicolons as seperators, add the aboslute path to Python and niod directories at the end. For help finding these paths, run `where python` and `where niod`, truncating the `exe` name from the returned path. If you are using a [virtual environment](https://docs.n.io/deployment/best-practices/) (highly recommended) make sure it is active when running `where` commands.
- Open `nio_winservice.py` with a text editor and enter the abosulte path to your nio project for the value of `project_path` near the top of the `NIOWinService` class, for example `project_path = C:\\Users\\<user>\\nio\\projects\\<project>` **Note the double backslashes!**
- Run `python nio_winservice --startup auto install`. If the service is going to be run as a user other than `Local System`, include `--username <user>` and `--password <pass>` args before `install`.
- `nio_<project>` has been installed and will start automatically in the future.

### Use:
- Control the service manually from the command line with `net start|stop nio_<project>`
- Or, Open Control Panel > System and Security > Adminstrative Tools > Services

### Remove:
- Run `python nio_winservice remove`
