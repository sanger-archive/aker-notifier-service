import dateutil.parser
import json


class Message:
    """Represent a message sent from an Aker application or service."""

    def __init__(self, event_type, timestamp, user_identifier, metadata):
        """Init the message class.

        Args:
            event_type: name of the type of the event
            timestamp: time of the event
            user_identifier: the user performing this event
            metadata: metadata of the event
        """
        self._event_type = event_type
        self._timestamp = timestamp
        self._user_identifier = user_identifier
        self._metadata = metadata

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

        return cls(**data)

    def __repr__(self):
        """Represent an object using the class name and the event_type."""
        return 'Message({}) @ {!s}'.format(self.event_type, self.timestamp)
