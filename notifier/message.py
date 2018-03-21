import dateutil.parser
import json


class Message:
    """Represent a message sent from an Aker application or service."""

    def __init__(self, event_type, timestamp, user_identifier, metadata, notifier_info):
        """Init the message class.

        Args:
            event_type: name of the type of the event
            timestamp: time of the event
            user_identifier: the user performing this event
            metadata: metadata of the event
            notifier_info: info specifically for the notifier from an app
        """
        self._event_type = event_type
        self._timestamp = timestamp
        self._user_identifier = user_identifier
        self._metadata = metadata
        self._notifier_info = notifier_info

    @property
    def event_type(self):
        """The name of the event type."""
        return self._event_type

    @property
    def timestamp(self):
        """The time that the event happened."""
        return self._timestamp

    @property
    def metadata(self):
        """The metadata linked to this event."""
        return self._metadata

    @property
    def notifier_info(self):
        """The notifier_info for this event."""
        return self._notifier_info

    @property
    def user_identifier(self):
        """The user (email address) responsible for this event."""
        return self._user_identifier

    @classmethod
    def from_json(cls, message_as_json):
        """Parse the JSON given and use the result to create a new Message object.

        Args:
            message_as_json: JSON representation of the message

        Returns:
            A new Message built from the provided JSON.

        Raises:
            ValueError: if the JSON can not be parsed
        """
        data = json.loads(message_as_json)
        data['timestamp'] = dateutil.parser.parse(data['timestamp'])

        # Currently we don't care for all of the properties in the event
        data.pop('lims_id', None)
        data.pop('uuid', None)
        data.pop('roles', None)

        # Stub out notifier_info if we have not received any
        if not data.get('notifier_info'):
            data['notifier_info'] = ''

        return cls(**data)

    def __repr__(self):
        """Represent an object using the class name and the event_type."""
        return 'Message({}) @ {!s}'.format(self.event_type, self.timestamp)
