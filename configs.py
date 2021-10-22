#!/usr/bin/env python3

'''
plan1:
    - should read everything into memory
    - use 3d array to store the [filename][section][key]=value
    # with this plan, multiple instances will not be required
'''

import os
import configparser

class CustomConfigParser:
    class NoDefaultFile(Exception):
        def __init__(self, default_env_file):
            super().__init__(f'Failed to read file: {default_env_file}')

    class ConfigFileNotFound(Exception):
        def __init__(self, path_cfg_file):
            super().__init__(f'Failed to read file: {path_cfg_file}')

    class ConfigFileNotInList(Exception):
        def __init__(self, path_cfg_file):
            super().__init__(f'File not in list of config files: {path_cfg_file}')

    @classmethod
    def __init__(cls, default_env_dir="."):
        ''' Using a precise env file format to know of the configs to be read '''
        cls.default_env_file='.ccp.txt'
        cls.default_env_dir = default_env_dir

        ''' check if default file is present
        if not through an exception
        '''
        full_path_default_env_file = os.path.abspath(default_env_dir) + "/" + cls.default_env_file
        if not os.path.isfile(full_path_default_env_file):
            raise cls.NoDefaultFile(full_path_default_env_file)

        cls.cfg_files=[]
        with open(cls.default_env_file, 'r') as fd_default_env_file:
            cls.cfg_files = fd_default_env_file.read().split('\n')
        
    @classmethod
    def read(cls, cfg_file=None):
        ''' files should be relative to the .custom_config_parser.txt '''
        cfg_files=[]
        if cfg_file is not None and cfg_file not in cls.cfg_files:
            raise ConfigFileNotInList(cfg_file)
        elif cfg_file is not None:
            path_cfg_file = os.path.abspath(cls.default_env_dir) + "/" + cfg_file
            configreader=configparser.ConfigParser()
            configreader.read(path_cfg_file)
            return configreader
        else:
            read_object={}
            for path_cfg_file in cls.cfg_files:
                if path_cfg_file == '':
                    continue
                ''' should be relative to the file running the configparser '''
                path_cfg_file = os.path.abspath(cls.default_env_dir) + "/" + path_cfg_file
                print("* reading:", path_cfg_file)
                ''' config would return empty if file does not exist'''
                if len(configparser.ConfigParser().read(path_cfg_file)) < 1:
                    raise cls.ConfigFileNotFound(path_cfg_file)

                configreader=configparser.ConfigParser()
                configreader.read(path_cfg_file)
                read_object[path_cfg_file] = configreader

            return read_object

if __name__ == "__main__":
    ''' advice for usage: 
    - Have .ccp in the root of the project
    '''
    import traceback
    try:
        # CustomConfigParser('/home/sherlock/test_dir')
        config=CustomConfigParser()
        config=config.read()
        print(config)
    except CustomConfigParser.NoDefaultFile as error:
        print(traceback.format_exc())
    except CustomConfigParser.ConfigFileNotFound as error:
        ''' with this implementation, it stops at the first exception - intended?? '''
        # print(traceback.format_exc())
        print(error)
    except CustomConfigParser.ConfigFileNotInList as error:
        print(error)
