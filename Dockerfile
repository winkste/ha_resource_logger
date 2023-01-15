FROM python:3.10.9-alpine3.17

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY /src/cls_screen.py /bin/cls_screen.py
COPY /src/cmd_main.py /bin/cmd_main.py
COPY /src/energy_log.py /bin/energy_log.py
COPY /src/log.py /bin/log.py
COPY /src/mqtt_ctrl.py /bin/mqtt_ctrl.py
COPY /src/my_secrets.py /bin/my_secrets.py
COPY /src/app.py /bin/app.py
COPY /src/templates/base.html /bin/templates/base.html
COPY /src/templates/history.html /bin/templates/history.html
COPY /src/templates/login.html /bin/templates/login.html
COPY /src/templates/logout.html /bin/templates/logout.html
COPY /src/templates/power.html /bin/templates/power.html
COPY /src/static/img/logo.png /bin/static/img/logo.png
COPY /src/static/styles/style.css /bin/static/styles/style.css
RUN chmod +x /bin/app.py
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python3", "/bin/app.py"]


# docker build --tag pyth-ha-rec .
# docker run --publish 5000:5000 pyth-ha-rec
