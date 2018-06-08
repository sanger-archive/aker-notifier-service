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
EVENT_SUB_CREATED = 'aker.events.submission.created'
EVENT_SUB_RECEIVED = 'aker.events.submission.received'
EVENT_WO_SUBMITTED = 'aker.events.work_order.submitted'
EVENT_WO_COMPLETED = 'aker.events.work_order.concluded'
EVENT_CAT_NEW = 'aker.events.catalogue.new'
EVENT_CAT_PROCESSED = 'aker.events.catalogue.processed'
EVENT_CAT_REJECTED = 'aker.events.catalogue.rejected'

# Email subjects
SBJ_SUB_CREATED = 'Aker - Submission Created'
SBJ_SUB_CREATED_HMDMC = 'Aker - Submission created with HMDMC required'
SBJ_SUB_RECEIVED = 'Aker - Submission Received'
SBJ_WO_SUBMITTED = 'Aker - Work Order Submitted'
SBJ_WO_COMPLETED = 'Aker - Work Order Completed'
SBJ_CAT_REJECTED = 'Aker - Catalogue Rejected'
SBJ_MSG_FAILED = 'Aker - Notification failure'
SBJ_NACK_FAILED = 'Aker - NACK failure'
SBJ_CAT_NEW = 'Aker - New catalogue available'
SBJ_CAT_PROCESSED = 'Aker - Catalogue processed'
