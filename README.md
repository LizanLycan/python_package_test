# Python Packages Test

## Description

1. The first test is divided into 2 steps, the first step tries to get to have the information shown in that link https://api.tidex.com/api/3/ticker/eth_btc,
   before they are shown at the public level.
   That means analyzing the data package to find the path of the data flow and the structure with which it is generated.
   The second step is to save the information in a database (public infos and infos between the packages) and graph it to see the differences.

2. The second test tries to find a solution of how to save GB of data and can read and process them in the fastest possible, seconds and milliseconds (logical solution).
   And create an interface where you can add different pairs per line that in real time shows bid (buy), ask (sell) and volume (vol) and an input field.
   And when the result of ask - bid is <= valr in the input the line is marked green. (That has to change in real time). (practical solution)

## Development

1. The first test is written in Python 3 with the support of packages to handle the hypertext protocol `requests`, handling non-SQL databases `pymongo` and libraries to graph the data `matplotlib`.

2. The second test is carried out with the help of the main python web framework Django in version 2.2, with SQL database management for the conceptualization of data handling quickly and efficiently (debatable according to the use and final maintenance that you are expected to give). In addition, the concept of websockets was used and applied for real time, in general it is developed for a web environment.

## Installation

### Environments to consider during tests:

1. For the first test, have installed and correctly configured [MongoDB](https://www.mongodb.com/download-center/community)

2. For the second it is required to have configured and running the `Redis` server in its default port`6379`. If you are in a Windows environment this will help: [Redis Installation and Deployment](https://github.com/microsoftarchive/redis)

In general to run both applications you must have installed and correctly configured Python 3 and the package manager `pip`. We proceed to create the virtual environment in the source root:

```bash
python -m venv .test
```

Activate the virtual environment:

```bash
.test/Scripts/activate
```

or

```bash
source .test/bin/activate
```

Install all package requirements:

```bash
pip install -r requirements.txt
```

## Start-up of the tests:

1. To start the first test:

```bash
cd test1
```

```bash
python main_process.py
```

2. To start the second test:

```bash
cd test2
```

2.1. Migrate database models:

```bash
python manage.py migrate
```

2.2. Run the server

```bash
python manage.py runserver
```

2.3. Open the test view in the browser to start the desired pair in:
`localhost:8000/pair_ticker/`
