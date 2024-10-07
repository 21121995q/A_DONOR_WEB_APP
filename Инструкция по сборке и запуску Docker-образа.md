\# Запустите docker, откройте командную строку и перейдите в директорию проекта:

\```
cd path\to\your\A_donor_web_app
\```

\# Соберите Docker-образ с помощью команды:

\```
docker build -t a_donor_web_app .
\```

\# Запустите Docker-контейнер с помощью команды:

\```
docker run -p 5000:5000 a_donor_web_app
\```

\# Откройте браузер и перейдите по адресу:

\```
http://localhost:5000
\```

\# Остановить и удалить контейнер:

\```
docker stop $(docker ps -q --filter ancestor=a_donor_web_app)
docker rm $(docker ps -aq --filter ancestor=a_donor_web_app)
\```