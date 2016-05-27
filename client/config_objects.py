import os
import getpass
from pathlib import Path

import multiconf
from multiconf.decorators import named_as, nested_repeatables


ef = multiconf.envs.EnvFactory()
my_env = ef.Env('my_env')


@nested_repeatables('backup_rules')
class BackupConf(multiconf.ConfigRoot):
    """By default we don't use the env feature of multiconf, so just provide dummy values"""
    def __init__(self, ssh_key, passphrase, exclude_from_files, borg='borg', selected_env=my_env, env_factory=ef):
        super(BackupConf, self).__init__(selected_env=selected_env, env_factory=env_factory)
        self.ssh_key = Path(ssh_key) if ssh_key else None
        self.passphrase = passphrase
        self.exclude_from_files = exclude_from_files
        self.borg = borg

    def mc_init(self):
        _home_dir = os.path.expanduser('~')  # Path.home() requires 3.5
        self.ssh_key = Path(_home_dir, '.ssh', self.ssh_key) if self.ssh_key else None
        if self.ssh_key:
            assert self.ssh_key.exists()
        self.log_file = Path(_home_dir, '.log/backup/backup.log')
        self.prefix = getpass.getuser()


@named_as('backup_rules')
class BackupRule(multiconf.RepeatableConfigItem):
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
