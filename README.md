# Resource Logging

Home resource logger for water gas and electricity.
This project gives you two simple user interface ways to track manually your used resources:
- command line based
- web page based

To execute the web page based interface I prepared also a docker container image.

### Command Line Interface
The command line interface shows the counter ID and the last entered data set. With the different options you can update the individual values and at the end using (s) save it and publish it to the MQTT broker.
--PICTURE CMD--

### Web Interface
The software is using flask and bootstrap to build a simple web application. It is using login mechanism controlled by a user dictionary in the my_secrets.py file.
The dialogs are:
- Login
- Zählerstände (Entry of current counter values)
- Historie (Plot all collected data)
- Logout (redirects to login)

<img width="633" alt="login" src="https://user-images.githubusercontent.com/9803344/158521520-496c97f5-c0b3-4f60-9067-e4a052c8178a.png">


The values are stored in a python file as dictionary.

Additional the actual year consumption is calculated giving the year end reading in the secrets file. 

These actual consumptions are populated to a mqtt broker.

###Build the program and execute
####Secrets configuration

```
my_secrets.py:

hostname = ""
port = 1883
client_id = ""
auth = {'username':"user", 'password':"pwd"}

gas_nr = "gas id"
power_nr = "power id"
water_nr = "water id"

gas_last_year = 0
power_last_year = 0
water_last_year = 0

users = {"user": "pwd"}
```
#### Build and activate Virtual environment
````
source python3 -m venv ha_rec_log_env

pip install -r requirements.txt 

source ha_rec_log_env/bin/activate
````
#### Run the application
````
web interface:
python src/app.py  

command line interface:
python src/cmd_main.py 
````
#### Build and deploy the Docker container
