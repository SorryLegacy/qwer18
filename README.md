1 - Flask
===============
Для работы с проектом склонируйте его себе с помощью:<br>
<code>git clone https://github.com/SorryLegacy/qwer18.git</code>

После этого зайдите в виртуальное окружение и установить все зависимости с помощью:<br>
<code>pip3 install -r requirements.txt</code>
После этого настройте ваше подключение к бд.
Создайте файл <strong>.env</storng> с переменными:
<ul>
<li>
USER_DATABASE
</li>
<li>
USER_PASSWORD
</li>
<li>
NAME_DATABASE
</li>
</ul>
И запустите приложение с помощью:
<code>flask run</code>

2 - Настройка Gunicorn  
===============
Сначала стоит проверить сможет ли наше приложение работать с Gunicorn.<br>
Для этого нужно только передать <strong>wsgi:app</strong> для точки входа <br>
<code>
(venv)sorrylegacy@sorrylegacy-MS-7996:~/project/djangoProject/flaskProject$ gunicorn --bind 0.0.0.0:5000 wsgi:app<br></code>

<h3>Результат примерно выглядеть так</h3>
<code>
[2022-09-29 15:31:31 +0300] [27994] [INFO] Starting gunicorn 20.1.0 <br>
[2022-09-29 15:31:31 +0300] [27994] [INFO] Listening at: http://0.0.0.0:5000 (27994) <br>
[2022-09-29 15:31:31 +0300] [27994] [INFO] Using worker: sync <br>
[2022-09-29 15:31:31 +0300] [27995] [INFO] Booting worker with pid: 27995
 </code>

<h3>Откройте браузер и пройдите по адресу серверного ip с 5000 портом:<br></h3>
<p><code>http://server_ip:5000</code></p>
И вы увидите результат приложения. 

<p>После того как вы убедитесь в нормальной работе приложения, можно остановить приложение нажав  <strong>CTRL+C</strong>.</p>

<p>Далее создадим файл для служебных элементов.<br>
<code>sudo nano /etc/systemd/system/ <strong>yourproject</strong>.service</code></p>
Этот файл нам нужен для чтобы Ubuntu автоматически запускать Gunicorn и работать с Flask при загрузке сервера<br>
Внутри файла нужно прописать данную конфигурацию:
<p>
<code>
[Unit]<br>
Description=Gunicorn instance to serve flaskProject<br>
After=network.target <br>
[Service]<br>
User=<strong>yourname</strong><br>
Group=www-data<br>
WorkingDirectory=/home/<strong>yourname</strong>/<strong>yourproject</strong><br>
Environment="PATH=/home/<strong>yourname</strong>/<strong>yourproject</strong>/<strong>yourenv</strong>/bin"<br>
ExecStart=/home/<strong>yourname</strong>/<strong>yourproject</strong>/<strong>yourenv</strong>/bin/gunicorn --workers 5 --bind unix:yourproject.sock -m 007 wsgi:app<br>
[Install]<br>
WantedBy=multi-user.target<br>
</code>
</p>
Шаблон сервиса хранится в файле <strong>gunicorn.service </strong>

<p>
Далее сохраните и закройте файл и в вашем терминале напишет данные команды:<br>
<code>sudo systemctl start <strong>yourproject</strong></code><br>
<code>sudo systemctl enable  <strong>yourproject</strong></code>
</p>
После этих команд проверим состояние. Сделать это можно с помощью команды:<br>
<code>sudo systemctl status <strong>yourproject</strong></code><br>
Ответ должен выглядеть примерно следующим образом:<br>
<img src="media/gunicorn.png" alt="result gunicorn"/>

3 - Настройка Nginx
===============
Для начала работы с <strong>Nginx</strong> стоит проверить есть ли он у вас. Для этого в терминале напишите<br>
<code> nginx -v </code><br>
Если вам показал версию, то он установлен<br>
<code>nginx version: nginx/1.18.0 (Ubuntu)</code><br>
Для начала нам нужно создать файл конфигурации:<br>
<code>sudo nano /etc/nginx/sites-available/<strong>yourproject</strong></code>
Код в нем должен выглядеть таким образом:<br>
<p>
<code>
server {<br>
   listen 80;<br>
   server_name <strong>yourdomain</strong>;<br> 
   location / {<br>
        include proxy_params;<br>
        proxy_pass http://unix:/home/<strong>yourname</strong>/<strong>yourproject</strong>/<strong>yourproject.sock</strong>;<br>
    }<br>
}<br>
</code>
</p>

Сохраните и закройте файл. Осталось активировать данную конфигурацию.
Для этого стоит прописать в терминал:<br>
<code>sudo ln -s /etc/nginx/sites-available/<strong>yourproject</strong> /etc/nginx/sites-enabled</code>
После этого перегрузите Nginx с помощью команды:
<code>sudo systemctl restart nginx </code><br>
После этих манипуляций у вас должна была появиться возможность увидеть приложение в браузере