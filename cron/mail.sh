#!/bin/bash

PROJECT_ROOT=/home/skyl/pinax-trunk/mycogia

# activate virtual environment
source /home/skyl/pinax-trunk/pinax-env/bin/activate

cd /home/skyl/pinax-trunk/mycogia
python manage.py send_mail >> $PROJECT_ROOT/logs/cron_mail.log 2>&1
python manage.py emit_notices
python manage.py retry_deferred
