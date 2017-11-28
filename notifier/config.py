from collections import namedtuple
from configparser import ConfigParser


class Config:
    """Extract the config from the provided config file path."""

    BrokerConfig = namedtuple('BrokerConfig',
                              'user password host port exchange exchange_type queue')
    EmailConfig = namedtuple('EmailConfig', '''from_address,
                                               smtp_host,
                                               smtp_port,
                                               smtp_username,
                                               smtp_password''')
    ProcessConfig = namedtuple('ProcessConfig', 'log_file error_log pidfile')
    ContactConfig = namedtuple('ContactConfig', 'email_dev_team email_hmdmc_verify')
    LinkConfig = namedtuple('LinkConfig', 'protocol root port')

    def __init__(self, config_file_path):
        """Init the class with the path of the config file and use the standard configparser."""
        config = ConfigParser()
        config.read(config_file_path)

        self._broker = self._broker_config(config, 'Broker')
        self._process = self._process_config(config, 'Process')
        self._email = self._email_config(config, 'Email')
        self._contact = self._contact_config(config, 'Contact')
        self._link = self._link_config(config, 'Link')

    @property
    def broker(self):
        return self._broker

    @property
    def process(self):
        return self._process

    @property
    def email(self):
        return self._email

    @property
    def contact(self):
        return self._contact

    @property
    def link(self):
        return self._link

    def _broker_config(self, config, section):
        """Extract the config for the message broker."""
        return self.BrokerConfig(
            config.get(section, 'user'),
            config.get(section, 'password'),
            config.get(section, 'host'),
            config.getint(section, 'port'),
            config.get(section, 'exchange'),
            config.get(section, 'exchange_type'),
            config.get(section, 'queue'),
        )

    def _email_config(self, config, section):
        """Extract the config for sending emails."""
        return self.EmailConfig(
            config.get(section, 'from_address'),
            config.get(section, 'smtp_host'),
            config.get(section, 'smtp_port'),
            config.get(section, 'smtp_username'),
            config.get(section, 'smtp_password'),
        )

    def _process_config(self, config, section):
        """Extract the config for logging and controlling the running process."""
        return self.ProcessConfig(
            config.get(section, 'log_file'),
            config.get(section, 'error_log'),
            config.get(section, 'pidfile'),
        )

    def _contact_config(self, config, section):
        """Extract the config for contacts available to the app."""
        return self.ContactConfig(
            config.get(section, 'email_dev_team'),
            config.get(section, 'email_hmdmc_verify'),
        )

    def _link_config(self, config, section):
        """Extract the config to create links."""
        return self.LinkConfig(
            config.get(section, 'protocol'),
            config.get(section, 'root'),
            config.get(section, 'port'),
        )
