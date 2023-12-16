#FROM python:3.10.9-alpine3.17
FROM python:3.11.6


#RUN apk add --no-cache --update \
#    python3 python3-dev gcc \
#    gfortran musl-dev \
#    libffi-dev openssl-dev 

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY /src/about.py /bin/about.py
COPY /src/app.py /bin/app.py
COPY /src/data_analysis.py /bin/data_analysis.py
COPY /src/database_hdl.py /bin/database_hdl.py
COPY /src/mqtt_ctrl.py /bin/mqtt_ctrl.py
COPY /src/my_secrets.py /bin/my_secrets.py
COPY /src/parameter.py /bin/parameter.py
COPY /src/plotter.py /bin/plotter.py
COPY /src/templates/about.html /bin/templates/about.html
COPY /src/templates/base.html /bin/templates/base.html
COPY /src/templates/history.html /bin/templates/history.html
COPY /src/templates/login.html /bin/templates/login.html
COPY /src/templates/logout.html /bin/templates/logout.html
COPY /src/templates/new_data.html /bin/templates/new_data.html
COPY /src/templates/view_history.html /bin/templates/view_history.html
COPY /src/templates/view_stats.html /bin/templates/view_stats.html
COPY /src/templates/downloads.html /bin/templates/downloads.html
COPY /src/static/img/logo.png /bin/static/img/logo.png
COPY /src/static/styles/style.css /bin/static/styles/style.css
COPY /bin/counters.csv /bin/counters.csv
COPY /bin/consumes.csv /bin/consumes.csv

RUN chmod +x /bin/app.py
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python3", "/bin/app.py"]


# docker build --tag pyth-ha-rec .
# docker run --publish 5000:5000 pyth-ha-rec
