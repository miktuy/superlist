sudo apt-get update
sudo apt-get install nginx
sudo systemctl start nginx
export SITENAME=www.miktuy-stage.ru
mkdir -p ~/sites/$SITENAME/database
mkdir -p ~/sites/$SITENAME/static
mkdir -p ~/sites/$SITENAME/venv
git clone https://github.com/miktuy/superlist.git ~/sites/$SITENAME/source
../venv/bin/python manage.py migrate --noinput


# when systemd settings are created
sudo systemctl daemon-reload
sudo systemctl enable www.miktuy-stage.ru
sudo systemctl start www.miktuy-stage.ru