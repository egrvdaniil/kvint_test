#!/bin/sh

set -e

. /venv/bin/activate

uvicorn main:app --host 0.0.0.0
