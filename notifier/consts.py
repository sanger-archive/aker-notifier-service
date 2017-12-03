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
PATH_WORK_ORDER = 'work_orders'

# Events
EVENT_SUB_CREATED = 'aker.events.submission.created'
EVENT_SUB_RECEIVED = 'aker.events.submission.received'
EVENT_WO_SUBMITTED = 'aker.events.work_order.submitted'

# Email subjects
SBJ_SUB_CREATED = 'Aker - Submission created'
SBJ_SUB_CREATED_HMDMC = 'Aker - Submission created with HMDMC required'
SBJ_SUB_RECEIVED = 'Aker - Submission received'
SBJ_WO_SUBMITTED = 'Aker - Work order submitted'
SBJ_MSG_FAILED = 'Aker - Notification failure'
SBJ_NACK_FAILED = 'Aker - NACK failure'
