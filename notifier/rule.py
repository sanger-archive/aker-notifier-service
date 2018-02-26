from .consts import *
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
        elif self._message.event_type == EVENT_WO_SUBMITTED:
            self._on_work_order_submitted()
        elif self._message.event_type == EVENT_WO_COMPLETED:
            self._on_work_order_completed()
        elif self._message.event_type == EVENT_CAT_REJECTED:
            self._on_catalogue_rejected()
        else:
            pass

    def _on_submission_create(self):
        """Notify once a submission has been created."""
        to, data, link = self._common_submission()
        data['user_identifier'] = self._message.user_identifier
        # Send a submission created email
        self._notify.send_email(subject=SBJ_SUB_CREATED,
                                from_address=self._config.email.from_address,
                                to=to,
                                template='submission_created',
                                data=data)
        # Send an email to the ethics officer
        if 'hmdmc_list' in self._message.metadata and self._message.metadata['hmdmc_list']:
            data['hmdmc_list'] = self._message.metadata['hmdmc_list']
            # Use the same link we have already created for the submission
            self._notify.send_email(subject=SBJ_SUB_CREATED_HMDMC,
                                    from_address=self._config.email.from_address,
                                    to=[self._config.contact.email_hmdmc_verify],
                                    template='submission_created_hmdmc',
                                    data=data)

    def _on_submission_received(self):
        """Notify once a submission has been received."""
        to, data, link = self._common_submission()
        if self._message.metadata.get('barcode'):
            data['barcode'] = self._message.metadata['barcode']
        if self._message.metadata.get('created_at'):
            data['created_at'] = self._message.metadata['created_at']
        if self._message.metadata.get('all_received'):
            data['all_received'] = self._message.metadata['all_received']
        self._notify.send_email(subject=SBJ_SUB_RECEIVED,
                                from_address=self._config.email.from_address,
                                to=to,
                                template='submission_received',
                                data=data)

    def _on_work_order_submitted(self):
        """Notify once a work order has been submitted."""
        to, data, link = self._common_work_order()
        data['user_identifier'] = self._message.user_identifier
        self._notify.send_email(subject=SBJ_WO_SUBMITTED,
                                from_address=self._config.email.from_address,
                                to=to,
                                template='wo_submitted',
                                data=data)

    def _on_work_order_completed(self):
        """Notify once a work order has been completed."""
        to, data, link = self._common_work_order()
        data['user_identifier'] = self._message.user_identifier
        self._notify.send_email(subject=SBJ_WO_COMPLETED,
                                from_address=self._config.email.from_address,
                                to=to,
                                template='wo_completed',
                                data=data)

    def _on_catalogue_rejected(self):
        """Notify when a catalogue has been rejected."""
        data = {}
        if self._message.metadata.get('error'):
            data['error'] = self._message.metadata['error']
            data['timestamp'] = self._message.timestamp
        self._notify.send_email(subject=SBJ_CAT_REJECTED,
                                from_address=self._config.email.from_address,
                                to=[self._config.contact.email_dev_team],
                                template='catalogue_rejected',
                                data=data)

    def _common_submission(self):
        """Extract the common info for submission events."""
        link = ''
        data = {}
        to = [self._message.user_identifier]
        # Check if we can create a link
        if self._message.metadata.get('submission_id'):
            data['submission_id'] = self._message.metadata['submission_id']
            link = self._generate_link(PATH_SUBMISSION, self._message.metadata['submission_id'])
            data['link'] = link
        # Add the sample custodian to the to list
        if self._message.metadata.get('sample_custodian'):
            to.append(self._message.metadata['sample_custodian'])
        if 'deputies' in self._message.metadata and self._message.metadata['deputies']:
            for dep in self._message.metadata['deputies']:
                to.append(dep)
        return to, data, link

    def _common_work_order(self):
        """Extract the common info for work order events."""
        link = ''
        data = {}
        to = [self._message.user_identifier]
        # Check if we can create a link
        if self._message.metadata.get('work_order_id'):
            data['work_order_id'] = self._message.metadata['work_order_id']
            link = self._generate_link(PATH_WORK_ORDER, self._message.metadata['work_order_id'])
            data['link'] = link
        return to, data, link

    def _generate_link(self, path, id):
        """Generate a link to the specific entity in the app provided by path."""
        return '{}://{}:{}/{}/{}'.format(self._config.link.protocol,
                                         self._config.link.root,
                                         self._config.link.port,
                                         path,
                                         id)
