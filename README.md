# Aker - Notifier service
[![Build Status](https://travis-ci.org/sanger/aker-notifier-service.svg?branch=devel)](https://travis-ci.org/sanger/aker-notifier-service)
[![Maintainability](https://api.codeclimate.com/v1/badges/3e2445822b8551dfd40e/maintainability)](https://codeclimate.com/github/sanger/aker-notifier-service/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/3e2445822b8551dfd40e/test_coverage)](https://codeclimate.com/github/sanger/aker-notifier-service/test_coverage)

This application acts as a worker (or consumer) on the `aker.events.notifications` queue and sends
notifications (only emails at this time) upon receiving an event.

# Installation
To install all the required packages, execute `pip install -r requirements.txt`

# Testing
To run all the tests, execute `nosetests --rednose` from the root directory.

# Misc.
Below are a few messages which can be manipulated and used during testing:
## aker.events.submission.created
```json
{
  "event_type": "aker.events.submission.created",
  "lims_id": "aker",
  "uuid": "815fd996-9e6e-440e-8fe1-1e5f8be135d1",
  "timestamp": "2018-02-05T16:39:59Z",
  "user_identifier": "pj5@sanger.ac.uk",
  "roles": [{
    "role_type": "submission",
    "subject_type": "submission",
    "subject_friendly_name": "Submission 603",
    "subject_uuid": "80776952-73be-4ccd-a996-9bed6d4d4b8a"
  }],
  "metadata": {
    "submission_id": 603,
    "hmdmc_list": null,
    "confirmed_no_hmdmc": null,
    "sample_custodian": "pj5@sanger.ac.uk",
    "total_samples": 1,
    "zipkin_trace_id": "d22a1a7add737fda",
    "deputies": ["hc6@sanger.ac.uk"]
  }
}
```

## aker.events.work_order.submitted
```json
{
  "event_type": "aker.events.work_order.submitted",
  "lims_id": "aker",
  "uuid": "815fd996-9e6e-440e-8fe1-1e5f8be135d1",
  "timestamp": "2018-02-05T16:39:59Z",
  "user_identifier": "pj5@sanger.ac.uk",
  "roles": [{
    "role_type": "submission",
    "subject_type": "submission",
    "subject_friendly_name": "Submission 603",
    "subject_uuid": "80776952-73be-4ccd-a996-9bed6d4d4b8a"
  }],
  "metadata": {
    "work_order_id": 603,
    "comment": "comment",
    "zipkin_trace_id": "d22a1a7add737fda"
  },
  "notifier_info": {
    "work_plan_id": 1
  }
}
```
