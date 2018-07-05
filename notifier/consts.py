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
PATH_SUBMISSION = 'reception/material_submissions'
PATH_WORK_ORDER_BEGIN = 'work/work_plans'
PATH_WORK_ORDER_END = 'build/dispatch'

# Events
EVENT_MAN_CREATED = 'aker.events.manifest.created'
EVENT_MAN_RECEIVED = 'aker.events.manifest.received'
EVENT_WO_DISPATCHED = 'aker.events.work_order.dispatched'
EVENT_WO_CONCLUDED = 'aker.events.work_order.concluded'
EVENT_CAT_NEW = 'aker.events.catalogue.new'
EVENT_CAT_PROCESSED = 'aker.events.catalogue.processed'
EVENT_CAT_REJECTED = 'aker.events.catalogue.rejected'

# Email subjects
SBJ_MAN_CREATED = 'Aker | Manifest Created'
SBJ_MAN_CREATED_HMDMC = 'Aker | Manifest Created with HMDMC'
SBJ_MAN_RECEIVED = 'Aker | Material Received'
SBJ_CAT_REJECTED = 'Aker | Catalogue Rejected'
SBJ_MSG_FAILED = 'Aker | Notification Failure'
SBJ_NACK_FAILED = 'Aker | NACK Failure'
SBJ_CAT_NEW = 'Aker | New Catalogue Available'
SBJ_CAT_PROCESSED = 'Aker | Catalogue Processed'
SBJ_PREFIX_WO = 'Aker | Work Order'
