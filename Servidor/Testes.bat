@echo off

ECHO =================Reiniciando os containers do Docker=================

docker-compose -f testes-docker-compose.yml down

for /f "tokens=3" %%i in ('docker images') do (
    docker rmi -f %%i
)

docker-compose  -f testes-docker-compose.yml up -d --build