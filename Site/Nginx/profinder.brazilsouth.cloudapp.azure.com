server {
    listen 443 ssl;
    server_name profinder.brazilsouth.cloudapp.azure.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        include proxy_params;
    }

    location ~ /images/ {
        proxy_pass http://127.0.0.1:5100;
        include proxy_params;
    }

    location ~ /profinder_api/ {
        proxy_pass http://127.0.0.1:5050;
        include proxy_params;
    }

    location ~ /db_admin/ {
        proxy_pass http://127.0.0.1:8080;
        include proxy_params;
    }
}

server {
    listen 80;
    server_name profinder.brazilsouth.cloudapp.azure.com;
    location ~ /.well-known {
        root /home/azureuser/Profinder/Site/Certificates;
    }
}