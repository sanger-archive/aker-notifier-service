# Aker - events notifier
[![Build Status](https://travis-ci.org/pjvv/aker-events-notifier.svg?branch=devel)](https://travis-ci.org/pjvv/aker-events-notifier)

This application acts as a worker (or consumer) on the `aker.events.notifications` queue and sends
notifications (only emails at this time) upon receiving an event.

# Installation
To install all the required packages, execute `pip install -r requirements.txt`

# Testing
To run all the tests, execute `nosetests --rednose` from the root directory.
