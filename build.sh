#!/usr/bin/env bash
# exit on error
set -o errexit

pip install requirements.txt

python manage.py collectstatic --no-input
<<<<<<< HEAD
python manage.py migrate
=======
python manage.py migrate
>>>>>>> 87b16737ecb8925af50d2e649dea2d69232916f1
