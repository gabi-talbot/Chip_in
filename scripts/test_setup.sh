#!/bin/sh
export FLASK_APP="test_app.py"
flask db upgrade
python -m unittest Chip_in/tests/test_app.py