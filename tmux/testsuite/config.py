from .helpers import TestTmux
from tmux.util import ConfigExpand
import os
import shutil
import kaptan
import unittest


TMUXWRAPPER_DIR = os.path.join(os.path.dirname(__file__), '.tmuxwrapper')

sampleconfigdict = {
    'session_name': 'sampleconfig',
    'start_directory': '~',
    'windows': [{
        'window_name': 'editor',
        'panes': [
            {
                'start_directory': '~', 'shell_command': ['vim'],
                },  {
                'shell_command': ['cowsay "hey"']
            },
        ],
        'layout': 'main-verticle'},
        {
            'window_name': 'logging',
            'panes': [
                {'shell_command': ['tail -F /var/log/syslog'],
                 'start_directory':'/var/log'}
            ]
        },
        {
            'automatic_rename': True,
            'panes': [
                {'shell_command': ['htop']}
            ]
        }]
}


class ConfigTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # run parent
        # setUpClass
        if not os.path.exists(TMUXWRAPPER_DIR):
            os.makedirs(
                TMUXWRAPPER_DIR)
            # super(ConfigTest, cls).setUpClass()

    def test_export_json(self):
        json_config_file = os.path.join(TMUXWRAPPER_DIR, 'config.json')

        config = kaptan.Kaptan()
        config.import_config(sampleconfigdict)

        json_config_data = config.export('json', indent=2)

        buf = open(json_config_file, 'w')
        buf.write(json_config_data)
        buf.close()

        new_config = kaptan.Kaptan()
        new_config_data = new_config.import_config(json_config_file).get()
        self.assertDictEqual(sampleconfigdict, new_config_data)

    def test_export_yaml(self):
        yaml_config_file = os.path.join(TMUXWRAPPER_DIR, 'config.yaml')

        config = kaptan.Kaptan()
        config.import_config(sampleconfigdict)

        yaml_config_data = config.export('yaml', indent=2)

        buf = open(yaml_config_file, 'w')
        buf.write(yaml_config_data)
        buf.close()

        new_config = kaptan.Kaptan()
        new_config_data = new_config.import_config(yaml_config_file).get()
        self.assertDictEqual(sampleconfigdict, new_config_data)

    def test_scan_config(self):
        configs = []

        garbage_file = os.path.join(TMUXWRAPPER_DIR, 'config.psd')
        buf = open(garbage_file, 'w')
        buf.write('wat')
        buf.close()

        if os.path.exists(TMUXWRAPPER_DIR):
            for r, d, f in os.walk(TMUXWRAPPER_DIR):
                for filela in (x for x in f if x.endswith(('.json', '.ini', 'yaml'))):
                    configs.append(os.path.join(
                        TMUXWRAPPER_DIR, filela))

        files = 0
        if os.path.exists(os.path.join(TMUXWRAPPER_DIR, 'config.json')):
            files += 1
            self.assertIn(os.path.join(
                TMUXWRAPPER_DIR, 'config.json'), configs)

        if os.path.exists(os.path.join(TMUXWRAPPER_DIR, 'config.yaml')):
            files += 1
            self.assertIn(os.path.join(
                TMUXWRAPPER_DIR, 'config.yaml'), configs)

        if os.path.exists(os.path.join(TMUXWRAPPER_DIR, 'config.ini')):
            files += 1
            self.assertIn(os.path.join(TMUXWRAPPER_DIR, 'config.ini'), configs)

        self.assertEqual(len(configs), files)

    @classmethod
    def tearDownClass(cls):
        if os.path.isdir(TMUXWRAPPER_DIR):
            shutil.rmtree(TMUXWRAPPER_DIR)


class ConfigExpandTestCase(unittest.TestCase):

    '''
    assumes the configuration has been imported into a python dict correctly.
    '''

    before_config = {
        'session_name': 'sampleconfig',
        'start_directory': '~',
        'windows': [{
            'shell_command': 'top',
            'window_name': 'editor',
            'panes': [
                {
                    'start_directory': '~', 'shell_command': ['vim'],
                    },  {
                    'shell_command': 'cowsay "hey"'
                },
            ],
            'layout': 'main-verticle'},
            {
                'window_name': 'logging',
                'panes': [
                    {'shell_command': ['tail -F /var/log/syslog'],
                     'start_directory':'/var/log'}
                ]
            },
            {
                'automatic_rename': True,
                'panes': [
                    {'shell_command': 'htop'}
                ]
            }]
    }

    after_config = {
        'session_name': 'sampleconfig',
        'start_directory': '~',
        'windows': [{
            'shell_command': ['top'],
            'window_name': 'editor',
            'panes': [
                {
                    'start_directory': '~', 'shell_command': ['vim'],
                    },  {
                    'shell_command': ['cowsay "hey"']
                },
            ],
            'layout': 'main-verticle'},
            {
                'window_name': 'logging',
                'panes': [
                    {'shell_command': ['tail -F /var/log/syslog'],
                     'start_directory':'/var/log'}
                ]
            },
            {
                'automatic_rename': True,
                'panes': [
                    {'shell_command': ['htop']}
                ]
            }]
    }

    def test_expand_shell_commands(self):
        '''
        expands shell commands from string to list
        '''
        config = ConfigExpand(self.before_config).expand()
        self.assertDictEqual(config, self.after_config)


class ConfigInheritance(unittest.TestCase):
    sampleconfigdict = {
        'session_name': 'sampleconfig',
        'start_directory': '~',
        'windows': [{
            'window_name': 'editor',
            'panes': [
                {
                    'start_directory': '~', 'shell_command': ['vim'],
                    },  {
                    'shell_command': ['cowsay "hey"']
                },
            ],
            'layout': 'main-verticle'},
            {
                'window_name': 'logging',
                'panes': [
                    {'shell_command': ['tail -F /var/log/syslog'],
                        'start_directory':'/var/log'}
                ]
            },
            {
                'automatic_rename': True,
                'panes': [
                    {'shell_command': ['htop']}
                ]
            }]
    }


    '''
    test inheritence casses

    format for tests will be

    test_{session/window/pane}_{config_option}_subject
    '''
    def test_session_start_directory(self):

        pass

    def test_window_start_directory(self):
        config = self.sampleconfigdict

        if 'start_directory' in config:
            session_start_directory = config['start_directory']

        for windowconfitem in config['windows']:
            window_start_directory = None
            if 'start_directory' in windowconfitem:
                window_start_directory = windowconfitem['start_directory']

            for paneconfitem in windowconfitem['panes']:
                if 'start_directory' in paneconfitem:
                    pane_start_directory = paneconfitem['start_directory']


        pass

    def test_session_window_pane_start_directory(self):
        '''
        test a complex case where there is a top session 'start_directory',
        with 3 windows, 1-3 panes, but one of the panes overrides.
        '''
        pass

if __name__ == '__main__':
    unittest.main()
