FROM python:3.11.0a1-alpine3.14

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
COPY /src/templates/index.html /bin/templates/index.html
RUN chmod +x /bin/app.py
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python3", "/bin/app.py"]


# docker build --tag pyth-ha-rec .
# docker run --publish 5000:5000 pyth-ha-rec
