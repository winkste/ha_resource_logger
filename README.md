# Resource Logging

Home resource logger for water gas and electricity.
This project gives you two simple user interface ways to track manually your used resources:
- command line based
- web page based

The web page based interface is also available in a docker container image.
<img width="633" alt="login" src="https://user-images.githubusercontent.com/9803344/158521520-496c97f5-c0b3-4f60-9067-e4a052c8178a.png">


The values are stored in a python file as dictionary.

Additional the actual year consumption is calculated giving the year end reading in the secrets file. 

These actual consumptions are populated to a mqtt broker.

```
test
```

