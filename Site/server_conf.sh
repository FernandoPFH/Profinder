cd /home/azureuser

sudo apt update
sudo apt install nginx

sudo ufw allow 'Nginx Full'

sudo ln -s /home/azureuser/Profinder/Site/Nginx/profinder.brazilsouth.cloudapp.azure.com /etc/nginx/sites-available/

sudo ln -s /home/azureuser/Profinder/Site/Nginx/profinder.brazilsouth.cloudapp.azure.com /etc/nginx/sites-enabled/

sudo nano /etc/nginx/nginx.conf

sudo nginx -t

sudo systemctl restart nginx

sudo certbot --nginx -d profinder.brazilsouth.cloudapp.azure.com -d profinder.brazilsouth.cloudapp.azure.com

sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

cd ./Profinder/Site

sudo nano docker-compose.yml

sudo docker-compose up -d --build

#cd ../Servidor

#sudo nano docker-compose.yml

#sudo docker-compose up -d --build