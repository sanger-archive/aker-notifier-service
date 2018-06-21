import os
from notifier import consts
from notifier import Config

# Get the config for this environment
config_file_path = '{!s}/{!s}/{!s}.cfg'.format(os.getcwd(), consts.PATH_CONFIG, 'test')

# Get the config
config = Config(config_file_path)
