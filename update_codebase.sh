set -x
git pull
source ../venv/bin/activate
cd simplydialproject/
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart nginx