"""Constants used throughout the app."""
# Environmental variables
ENV_VAR_APP = 'aker_events_notifier_env'

# Environments
ENV_DEV = 'development'
ENV_TEST = 'testing'
ENV_STAGING = 'staging'
ENV_PROD = 'production'

# Paths
PATH_CONFIG = 'config'
PATH_SUBMISSION = 'material_submission'

# Events
EVENT_SUB_CREATED = 'aker.events.submission.created'
EVENT_SUB_RECEIVED = 'aker.events.submission.received'

# Email subjects
SBJ_SUB_CREATED = 'Aker - Submission created'
SBJ_SUB_CREATED_HMDMC = 'Aker - Submission created with HMDMC required'
SBJ_SUB_RECEIVED = 'Aker - Submission received'
SBJ_MSG_FAILED = 'Aker - Notification failure'
SBJ_NACK_FAILED = 'Aker - NACK failure'
