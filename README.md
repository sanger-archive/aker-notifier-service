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
## Useful links
[This](https://gist.github.com/jriguera/f3191528b7676bd60af5) gist was very helpful.

## Messages
[This](https://ssg-confluence.internal.sanger.ac.uk/display/PSDPUB/Messages) confluence link has a list of messages to test the notifier with.
