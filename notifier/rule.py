from .consts import *
from .messages import *
from .notify import Notify


class Rule:
    """Class containing the rules to be executed for each type of event."""

    def __init__(self, env, config, message):
        """Init the class with the environment, config and message (event) to be checked."""
        self._env = env
        self._config = config
        self._message = message
        self._notify = Notify(self._env, self._config)

    def check_rules(self):
        """Check all the rules for the current message (event)."""
        if self._message.event_type == EVENT_SUB_CREATED:
            self._on_submission_create()
        elif self._message.event_type == EVENT_SUB_RECEIVED:
            self._on_submission_received()
        else:
            pass

    def _on_submission_create(self):
        """Notify once a submission has been created."""
        link = ''
        data = {}
        # Check if we can create a link
        if 'submission_id' in self._message.metadata and self._message.metadata['submission_id']:
            data['submission_id'] = self._message.metadata['submission_id']
            link = self._generate_link(PATH_SUBMISSION, self._message.metadata['submission_id'])
            data['link'] = link
        to = [self._message.user_identifier]
        data['user_identifier'] = self._message.user_identifier
        # Add the sample custodian to the to list
        if ('sample_custodian' in self._message.metadata
                and self._message.metadata['sample_custodian']):
            to.append(self._message.metadata['sample_custodian'])
        # Add the deputies to the to list
        if ('deputies' in self._message.metadata
                and self._message.metadata['deputies']
                and len(self._message.metadata['deputies']) > 0):
            for dep in self._message.metadata['deputies']:
                to.append(dep)
        # Send a submission created email
        self._notify.send_email(subject=SBJ_SUB_CREATED,
                                from_address=self._config.email.from_address,
                                to=to,
                                template='submission_created',
                                data=data)
        # # Send an email to the ethics officer
        # if 'hmdmc_number' in self._message.metadata and self._message.metadata['hmdmc_number']:
        #     # Use the same link we have already created for the submission
        #     message = self._generate_html_email(BODY_SUB_CREATED_HMDMC, link)
        #     self._notify.send_email(subject=SBJ_SUB_CREATED_HMDMC,
        #                             from_address=self._config.email.from_address,
        #                             to=[self._config.contact.email_hmdmc_verify],
        #                             plain_message=message,
        #                             html_message=message)

    def _on_submission_received(self):
        """Notify once a submission has been received."""
        link = ''
        data = {}
        # Check if we can create a link
        if 'submission_id' in self._message.metadata and self._message.metadata['submission_id']:
            data['submission_id'] = self._message.metadata['submission_id']
            link = self._generate_link(PATH_SUBMISSION, self._message.metadata['submission_id'])
            data['link'] = link
        to = [self._message.user_identifier]
        if 'barcode' in self._message.metadata and self._message.metadata['barcode']:
            data['barcode'] = self._message.metadata['barcode']
        if 'created_at' in self._message.metadata and self._message.metadata['created_at']:
            data['created_at'] = self._message.metadata['created_at']
        if 'all_received' in self._message.metadata and self._message.metadata['all_received']:
            data['all_received'] = self._message.metadata['all_received']
        if ('sample_custodian' in self._message.metadata
                and self._message.metadata['sample_custodian']):
            to.append(self._message.metadata['sample_custodian'])
        if ('deputies' in self._message.metadata and self._message.metadata['deputies']
                and len(self._message.metadata['deputies']) > 0):
            for dep in self._message.metadata['deputies']:
                to.append(dep)
        self._notify.send_email(subject=SBJ_SUB_RECEIVED,
                                from_address=self._config.email.from_address,
                                to=to,
                                template='submission_received',
                                data=data)

    def _generate_link(self, path, id):
        return '{}://{}:{}/{}/{}'.format(self._config.link.protocol,
                                         self._config.link.root,
                                         self._config.link.port,
                                         path,
                                         id)
