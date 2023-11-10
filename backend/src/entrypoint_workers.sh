#!/bin/sh

set -e

. /venv/bin/activate

taskiq worker broker_init:broker
