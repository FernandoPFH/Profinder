read -p "DNS: " DNS


cd /home/azureuser

mv /home/azureuser/Profinder/Site/Nginx/nginx.conf /home/azureuser/Profinder/Site/Nginx/profinder.brazilsouth.cloudapp.azure.com

openssl dhparam -out /home/azureuser/Profinder/Site/Certificates/dhparam.pem 4096

sudo apt update
printf "y" | sudo apt install nginx

sudo ufw allow 'Nginx Full'

sudo ln -s /home/azureuser/Profinder/Site/Nginx/profinder.brazilsouth.cloudapp.azure.com /etc/nginx/sites-available/

sudo ln -s /home/azureuser/Profinder/Site/Nginx/profinder.brazilsouth.cloudapp.azure.com /etc/nginx/sites-enabled/

sed -i 's/# server_names_hash_bucket_size 64/server_names_hash_bucket_size 64/g' /etc/nginx/nginx.conf

sudo nginx -t

sudo systemctl restart nginx

printf "y" | sudo apt install certbot python3-certbot-nginx 

sudo certbot --nginx -d profinder.brazilsouth.cloudapp.azure.com -d profinder.brazilsouth.cloudapp.azure.com --non-interactive --agree-tos -m 19.00499-0@maua.br

sudo apt-get update
printf "y" | sudo apt-get install \
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

printf "y" | sudo apt-get install docker-ce docker-ce-cli containerd.io

sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

cd ./Profinder/Site

sed -i `s/localhost/$DNS/g` docker-compose.yml
sed -i `s/true/false/g` docker-compose.yml

sudo docker-compose up -d --build

cd ../Servidor

sed -i `s/localhost/$DNS/g` docker-compose.yml

sudo docker-compose up -d --build