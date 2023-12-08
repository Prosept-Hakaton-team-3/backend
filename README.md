![Prosept workflow](https://github.com/Prosept-Hakaton-team-3/backend/actions/workflows/backend_CI.yml/badge.svg)

`Python` `Django` `Django REST Framework` `Nginx` `Gunicorn`  `PostgreSQL` `Docker` `CI/CD`
# Prosept Application

**Ссылка на [сайт](http://81.31.246.159)**

**Ссылка на [документацию](http://81.31.246.159/api/swagger/)**

### Инструкция по развертыванию
Создайте файл `.env`, в котором перечислите все переменные окружения, пример находится в файле `.env.example`
#### Локальное развертывание
- Клонируйте репозиторий
```shell
git clone https://github.com/Prosept-Hakaton-team-3/backend.git
cd backend
```
- Создайте и активируйте виртуальное окружение, установите зависимости
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- Запустите миграции и загрузите данные в базу, затем запустите сервер
```shell
python manage.py migrate
python manage.py load_csv
python manage.py runserver
```
Теперь можно перейти по адресу http://127.0.0.1:8000
***
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
sudo docker image build -t prosept/backend .
```
```shell
sudo docker run -d prosept/backend
sudo docker exec <container> python manage.py migrate
sudo docker exec <container> python manage.py load_csv
```

#### Проект готов к использованию!
***
### Над проектом работали:
**[Антон Земцов](https://github.com/antonata-c)** 

**[Баринов Максим](https://github.com/CraftyPlonkton)**