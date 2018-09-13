import os
import getpass
from pathlib import Path

from appdirs import AppDirs
from multiconf import McConfigRoot, RepeatableConfigItem, MC_REQUIRED
from multiconf.decorators import named_as, nested_repeatables


app_dirs = AppDirs("bbmt", "Hupfeldt_IT")
config_dir = app_dirs.user_config_dir


@nested_repeatables('backup_rules')
class BackupConf(McConfigRoot):
    """Top level object for configuration.

    Args:
        ssh_key_file_name (str): Filename or path to ssh key file. It will be interpreted as relative to HOME/.ssh if not absolute.
        passphrase (str): Passphrase for ssh_key.
        exclude_from_files (list[str]): A list of file names with exclude patterns. Will be interpreted relative to 'config_dir'.
        borg (str): borg command, default is 'borg'. Specify path if 'borg' is not in the PATH.
    """

    def __init__(self, ssh_key_file_name, passphrase, exclude_from_file_names, borg='borg'):
        super(BackupConf, self).__init__()
        self.ssh_key_file_name = ssh_key_file_name
        self.passphrase = passphrase
        self.exclude_from_file_names = exclude_from_file_names
        self.borg = borg
        self.prefix = getpass.getuser()

        self.ssh_key = MC_REQUIRED
        self.log_file = MC_REQUIRED
        self.exclude_from_files = MC_REQUIRED

    def mc_init(self):
        # Path.home() requires 3.5, so use expanduser('~') instead
        self.ssh_key = Path(os.path.expanduser('~'), '.ssh', self.ssh_key_file_name) if self.ssh_key_file_name else None
        self.log_file = Path(app_dirs.user_log_dir, '.backup.log')
        self.exclude_from_files = [Path(config_dir, fn) for fn in self.exclude_from_file_names]


@named_as('backup_rules')
class BackupRule(RepeatableConfigItem):
    def __init__(self, from_dir, target_user, target_host,
                 keep_within='2d',
                 keep_hourly=48, keep_daily=30, keep_weekly=26, keep_monthly=24, keep_yearly=10):
        super(BackupRule, self).__init__(mc_key=(from_dir, target_user, target_host))
        self.from_dir = from_dir
        self.target_user = target_user
        self.target_host = target_host
        self.keep_within = keep_within
        self.keep_hourly = keep_hourly
        self.keep_daily = keep_daily
        self.keep_weekly = keep_weekly
        self.keep_monthly = keep_monthly
        self.keep_yearly = keep_yearly

    @property
    def prefix(self):
        return self.contained_in.prefix
