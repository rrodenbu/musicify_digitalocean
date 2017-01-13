

Connecting to server:

ssh root@192.241.176.138
'Enter password'
su - urban
source bin/activate
git pull
python manage.py collectstatic
python manage.py migrate
sudo supervisorctl restart webapps

Getting music

sign in as admin
go to: ../musicify/admin/get-songs

Website hosted at:
192.241.176.138

Tutorial used for digital ocean:
https://simpleisbetterthancomplex.com/tutorial/2016/10/14/how-to-deploy-to-digital-ocean.html
