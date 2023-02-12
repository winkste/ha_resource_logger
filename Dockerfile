#FROM python:3.10.9-alpine3.17
FROM python:latest

#RUN apk add --no-cache --update \
#    python3 python3-dev gcc \
#    gfortran musl-dev \
#    libffi-dev openssl-dev 

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY /src/app.py /bin/app.py
COPY /src/cls_screen.py /bin/cls_screen.py
COPY /src/cmd_main.py /bin/cmd_main.py
COPY /src/data_handler.py /bin/data_handler.py
COPY /src/mqtt_ctrl.py /bin/mqtt_ctrl.py
COPY /src/mqtt_secrets.py /bin/mqtt_secrets.py
COPY /src/parameter.py /bin/parameter.py
COPY /src/plotter.py /bin/plotter.py
COPY /src/resource_mgr.py /bin/resource_mgr.py
COPY /src/templates/actuals.html /bin/templates/actuals.html
COPY /src/templates/base.html /bin/templates/base.html
COPY /src/templates/datasets.html /bin/templates/datasets.html
COPY /src/templates/history.html /bin/templates/history.html
COPY /src/templates/login.html /bin/templates/login.html
COPY /src/templates/logout.html /bin/templates/logout.html
COPY /src/templates/power.html /bin/templates/power.html
COPY /src/static/img/logo.png /bin/static/img/logo.png
COPY /src/static/styles/style.css /bin/static/styles/style.css
COPY /bin/actuals.csv /bin/actuals.csv
COPY /bin/history.csv /bin/history.csv
RUN chmod +x /bin/app.py
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python3", "/bin/app.py"]


# docker build --tag pyth-ha-rec .
# docker run --publish 5000:5000 pyth-ha-rec
