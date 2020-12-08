@echo off

ECHO =================Reiniciando os containers do Docker=================

docker-compose down

for /f "tokens=3" %%i in ('docker images') do (
    docker rmi -f %%i
)

docker-compose up -d