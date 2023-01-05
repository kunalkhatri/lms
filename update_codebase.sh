set -x
git pull
source venv/bin/activate
cd lms_django
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart lms-gunicorn
sudo systemctl restart nginx