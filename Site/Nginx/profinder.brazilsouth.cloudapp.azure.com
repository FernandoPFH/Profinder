server {
    listen 443 ssl;
    server_name profinder.brazilsouth.cloudapp.azure.com;

    location ~* ^/images/(.*) {
        proxy_pass http://127.0.0.1:5100/$1$is_args$args;
    }

    location ~* ^/api/(.*) {
        proxy_pass http://127.0.0.1:5050/$1$is_args$args;
        include proxy_params;
    }

    location ~* ^/db_admin/(.*) {
        proxy_pass http://127.0.0.1:8080/$1$is_args$args;
    }

    location / {
        proxy_pass http://127.0.0.1:5000;
        include proxy_params;
    }

    ssl_certificate /etc/letsencrypt/live/profinder.brazilsouth.cloudapp.azure.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/profinder.brazilsouth.cloudapp.azure.com/privkey.pem; # managed by Certbot
}

server {
    listen 80;
    server_name profinder.brazilsouth.cloudapp.azure.com;
    location ~ /.well-known {
        root /home/azureuser/Profinder/Site/Certificates;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}