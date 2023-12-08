![Prosept workflow](https://github.com/Prosept-Hakaton-team-3/backend/actions/workflows/backend_CI.yml/badge.svg)

`Python` `Django` `Django REST Framework` `Nginx` `Gunicorn`  `PostgreSQL` `Docker` `CI/CD`
# Prosept Application

**Ссылка на [сайт](http://81.31.246.159)**

**Ссылка на [документацию](http://81.31.246.159/api/swagger/)**

### Инструкция по развертыванию

#### Развертывание в контейнере

- Установите докер и клонируйте репозиторий
```shell
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```
```shell
git clone https://github.com/Prosept-Hakaton-team-3/backend.git
cd backend
```
- Выполните команды для сборки Docker-образа и запуска контейнера
```shell
sudo docker image build -f Dockerfile_dev -t prosept/backend .
```
```shell
sudo docker run -p 8000:8080 prosept/backend
```

#### Проект готов к использованию!
http://127.0.0.1:8000/api/v1/
***
### Над проектом работали:
**[Антон Земцов](https://github.com/antonata-c)** 

**[Баринов Максим](https://github.com/CraftyPlonkton)**