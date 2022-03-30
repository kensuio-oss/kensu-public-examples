# Kensu Sandbox Use case: Financial reporting

This repo contains the materials linked to the Kensu Sandbox use case.


## Content of the Repository

- `conf.ini`: the configuration file needed to init Kensu

- `datasources/`: csv files

- `python_code/`: the scripts used in the tutorial

- `requirements.txt`: to install the dependencies of the scripts


## Installation

### On a python environment

1. Clone the repo with `git clone git@github.com:kensuio-oss/kensu-public-examples.git`
2. Create a python virtual environment: `python3 -m venv kensu_env`
3. Activate the environment: `source kensu_env/bin/activate`
4. Install the requirements : `pip install -r requirements.txt`

### As a docker image

Please make sure to modify the `conf.ini` file before building the image, follow the steps on https://docs.kensu.io/installation-and-configuration