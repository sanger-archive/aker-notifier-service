import logging

from .consts import *
from .notify import Notify

logger = logging.getLogger(__name__)


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
        elif self._message.event_type in [EVENT_WO_DISPATCHED, EVENT_WO_CONCLUDED]:
            self._on_work_order_event()
        elif self._message.event_type == EVENT_CAT_NEW:
            self._on_catalogue_new()
        elif self._message.event_type == EVENT_CAT_PROCESSED:
            self._on_catalogue_processed()
        elif self._message.event_type == EVENT_CAT_REJECTED:
            self._on_catalogue_rejected()
        else:
            pass

    def _on_submission_create(self):
        """Notify once a submission has been created."""
        logger.debug("_on_submission_create triggered")
        to, data = self._common_submission()
        data['user_identifier'] = self._message.user_identifier
        # Send a submission created email
        self._notify.send_email(subject=SBJ_SUB_CREATED,
                                from_address=self._config.email.from_address,
                                to=to,
                                template='submission_created',
                                data=data)
        # Send an email to the ethics officer
        if self._message.metadata.get('hmdmc'):
            data['hmdmc_list'] = self._message.metadata['hmdmc']
            # Use the same link we have already created for the submission
            self._notify.send_email(subject=SBJ_SUB_CREATED_HMDMC,
                                    from_address=self._config.email.from_address,
                                    to=[self._config.contact.email_hmdmc_verify],
                                    template='submission_created_hmdmc',
                                    data=data)

    def _on_submission_received(self):
        """Notify once a submission has been received."""
        logger.debug("_on_submission_received triggered")
        to, data = self._common_submission()
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

    def _on_work_order_event(self):
        """Notify once a work order has been submitted."""
        logger.debug("_on_work_order_event triggered")
        try:
            to, data = self._common_work_order()
        except ValueError as error:
            logger.error(error.message)
        data['user_identifier'] = self._message.user_identifier
        data['work_order_status'] = self._message.event_type.split('.')[-1]
        self._notify.send_email(
            subject="{0} {1} [Data release: {2}]".format(
                SBJ_PREFIX_WO,
                data['work_order_status'].capitalize(),
                self._message.notifier_info['drs_study_code']),
            from_address=self._config.email.from_address,
            to=to,
            template='wo_event',
            data=data)

    def _on_catalogue_new(self):
        """Send a notification if a new catalogue is available."""
        logger.debug("_on_catalogue_new triggered")
        to = self._common_catalogue()
        self._notify.send_email(subject=SBJ_CAT_NEW,
                                from_address=self._config.email.from_address,
                                to=to,
                                template='catalogue_new',
                                data={})

    def _on_catalogue_processed(self):
        """Send a notification if the catalogue received has been processed."""
        logger.debug("_on_catalogue_processed triggered")
        to = self._common_catalogue()
        self._notify.send_email(subject=SBJ_CAT_PROCESSED,
                                from_address=self._config.email.from_address,
                                to=to,
                                template='catalogue_processed',
                                data={})

    def _on_catalogue_rejected(self):
        """Notify when a catalogue has been rejected."""
        logger.debug("_on_catalogue_rejected triggered")
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
        data = {}
        to = [self._message.user_identifier]
        # Check if we can create a link
        if self._message.metadata.get('submission_id'):
            data['submission_id'] = self._message.metadata['submission_id']
            data['link'] = self._generate_link(PATH_SUBMISSION,
                                               self._message.metadata['submission_id'])
        # Add the sample custodian to the to list
        if self._message.metadata.get('sample_custodian'):
            to.append(self._message.metadata['sample_custodian'])
        if self._message.metadata.get('deputies'):
            for dep in self._message.metadata['deputies']:
                to.append(dep)
        return to, data

    def _common_work_order(self):
        """Extract the common info for work order events."""
        data = {}
        to = [self._message.user_identifier]
        # Check if we can create a link
        if self._message.metadata.get('work_order_id'):
            data['work_order_id'] = self._message.metadata['work_order_id']
            # We want the work plan id for the link
            data['link'] = self._generate_wo_link(self._message.notifier_info['work_plan_id'])
        else:
            raise ValueError("Work Order ID not found in metadata dictionary")
        return to, data

    def _common_catalogue(self):
        """Extract the common info for catalogue events - currently just dev team email address."""
        return [self._config.contact.email_dev_team]

    def _generate_link(self, path, id):
        """Generate a link to the specific entity in the app provided by path."""
        return '{}://{}:{}/{}/{}'.format(self._config.link.protocol,
                                         self._config.link.root,
                                         self._config.link.port,
                                         path,
                                         id)

    def _generate_wo_link(self, work_plan_id):
        """Generate a link to the specific entity in the work orders app."""
        return '{}://{}:{}/{}/{}/{}'.format(self._config.link.protocol,
                                            self._config.link.root,
                                            self._config.link.port,
                                            PATH_WORK_ORDER_BEGIN,
                                            work_plan_id,
                                            PATH_WORK_ORDER_END)
