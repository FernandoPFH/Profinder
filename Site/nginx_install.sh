sudo apt update
sudo apt install nginx

sudo ufw allow 'Nginx Full'

sudo ln -s /home/azureuser/Profinder/Site/Nginx/profinder.brazilsouth.cloudapp.azure.com /etc/nginx/sites-available/

sudo ln -s /home/azureuser/Profinder/Site/Nginx/profinder.brazilsouth.cloudapp.azure.com /etc/nginx/sites-enabled/

sudo nano /etc/nginx/nginx.conf