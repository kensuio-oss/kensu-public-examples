# What's up doc 🥕

This is the support for the instructor to prepare the Virtual Lab, but also can be used during the lab to follow the step altogether with the attendees.

## "What am I going to learn?"

By the end of this lab, you'll:

- see what kind of issues happen in data pipelines
- know why you must not let your users detect them
- how to make a data pipeline data observable and,
    - how to create a rule in Kensu manually
    - how to use data observations within the pipeline to
        - create rules programmatically
        - introduce circuit breakers to avoid issues propagation (data cascades)

➡️ You'll be ready to take your team to the next step: [**start observing one of your data pipeline**](https://docs.kensu.io/recipe-observe-your-first-pipeline)

## "What am I going to do?"

This lab will consider a pipeline creating a report of some stock market information.

This report is used by the business to take business decisions, but also to highlight risks important to comply with financial regulations.

The data pipeline is composed of two steps, uses only CSV for the simplicity of the lab, and runs once per month. Here are the steps:
1. ingest and model stock information from CSV file in the data lake (dumped from the operational sources previsously)
2. create a reports for each of the two stocks being heavily used by stakeholders.

Then the data is loaded in a Business Intelligence platform by the stakeholders to take decisions in a timely manner.

Here is an overview of the pipeline:
![](images/0%20-%20Pipeline%20Applications.png).

Where the two applications are connected because the `Reporting` spark application reads the data produced by the `Data Ingestion` pandas application. 

The `Data Ingestion` reads stock files and merge them in a consolidated stock file:
![](images/1%20-%20Pipeline%20Data%20Ingestion.png).

The `Reporting` produces the reports that include an additional business KPI:
![](images/2%20-%20Pipeline%20Reporting.png)

The pipeline at the data level, therefore, looks like this:
![](images/3%20-%20Pipeline%20Data%20Level.png)

# Set up

## Prerequisites

You must have:
- A terminal
    - Ideally also `wget` or `curl`.
- Python3
    - With `virtualenv` module
- Java 11.0+
    - Protip: I use `sdkman` and `jenv` to help me with this and have a safe environment locally

## Working Directory

To simpify the set up, we will do everything from a dedicated working directory that you'll create wherever your want on your machine.

This folder will be referred as `VirtualLab` in the following.

In a terminal, move to whichever folder you like (e.g., `~/src`, `~/Documents`, ...) and create the folder:

```sh
mkdir VirtualLab
cd VirtualLab
```

## Create the environment

We'll make sure you have a local environment for python and java, for this run these commands:

Create a dedicate python env using `virtualenv` -- this will create a `kensu_env` folder where the needed python libraries will be downloaded:

```sh
python3 -m venv kensu_env
source kensu_env/bin/activate
```

(If needed) Set the java variables to point to the java version you want to use (here 11.0) using `jenv`, this will create a `.java-version` file:

```sh
jenv 11.0
```

## Get the materials and tools

# Lab's data pipeline

The pipeline code is distributed in a Kensu OSS GitHub repository that you can clone using the following:

```sh
git clone git@github.com:kensuio-oss/kensu-public-examples.git
git checkout VirtualLab
```

> Note: we checkout the `VirtualLab` branch where this lab is available, as a stripped version of the public examples.

Then we'll install all dependencies declared in `requirements.txt`:

```sh
cd Financial_Data_Report
pip install -r requirements.txt
cd ..
```
> ⚠️ This can take some time to download the below libraries and dependencies:
> - pandas: to work with data
> - pyspark: to work with data leveraging distributed computing
> - kensu: the open source data observability agent

## Metabase (BI)

The Metabase BI tool is simply a jar that you can download in your VirtualLab folder, but to make it cleaner, we'll do it in a dedicated folder:

```sh
mkdir metabase
cd metabase
```

To download the `jar` in this folder you can follow one of the followin:
- `wget https://downloads.metabase.com/v0.44.2/metabase.jar`.
- `curl https://downloads.metabase.com/v0.44.2/metabase.jar > metabase.jar`.
- Download it manually navigating [this link](https://downloads.metabase.com/v0.44.2/metabase.jar) and move it to this `metabase` folder.

Also in this lab, we'll use `csv` files to reduce the complexity of the setup, however, metabase needs a [plugin](https://github.com/Markenson/csv-metabase-driver) to load those.

Here are the instructions to install it The plugin is another `jar`, we'll use `wget` only but the instructions above are still valid here:

```sh
mkdir plugins
cd plugins
wget https://github.com/Markenson/csv-metabase-driver/releases/download/v1.3.1/csv.metabase-driver.jar
cd ..
```

Then you can start Metabase as follow on port `3000` (but you can change it):

```sh
MB_JETTY_PORT=3000 java -jar metabase.jar > /dev/null 2>&1 &
```

> Note: the last part is to keep it silent on Linux, you can also remove it. If so, open a new terminal, even if running the script in the background as it will generate ~~noise~~ logs.

# Lab Script

The pipeline will be executed from the `Financial_Data_Report/src`, where you'll see three versions of the pipeline in dedicated folder:
- `_yolo`: basically, what we do for the last decade -- few logs, no observations
- `with_do`: what you'll do `by default` after this lab
- `with_rules`: what you'll aim to do over time by embracing `new best practices`

So let's move on and go through each of them, but first make sure you're in the `src` folder:

```sh
cd Financial_Data_Report
cd src
```

## YOLO

This first version is the pipeline, as it is generally deployed, with no data observability capability.

SO let's run it for a couple of months and figure what happens.

### November

The first run is generating the reports for November 2021.

#### Run

```sh
python3 _yolo/data_ingestion.py nov 2021 ; python3 _yolo/reporting_spark.py nov 2021
```

#### Analyze

In this section, we're going to use Metabase for the first time to load the `Buzzfeed` report.

For this, navigate to [Metabase on https://localhost:3000](https://localhost:3000) and go through the first steps until you have to create the first dataset.

When on the first data set creation, select `CSV` for the type, and fill out the information such as the path to the `report/buzzfeed.csv` file. Also use `utf-8` for the _encoding_, and importantly, enter `&suppressHeaders=true` in the _advanced_ field.

When done, you can click on `Browse data` in the left menu, and pick the dataset you've created.

In order to use it appropriately, you'll need to configure the CSV set in the `admin settings` panel, in the `Data Model` menu. There you will set the column names and type (e.g., mainly `Creation Date` and `Quantity`).

Then you can go back to the data by `Exiting` from the Admin settings and browse the data again.

What can be done is creating a dashboard with
- a `scatter` plot Date x Delta
- a computed which is the std of Delta: as this is a business KPI that represents a notion of risk

The stakeholder are happy 🤩.

### December

Now that the process is deployed, it will run automatically for the December data, this is what we'll simulate here.

#### Run

```sh
python3 _yolo/data_ingestion.py dec 2021 ; python3 _yolo/reporting_spark.py dec 2021
```

This has overriden the data and the report with current months information.

#### Analyze

We need to refresh the dataset to scan it again, this is done in the `Settings > Databases` then click on your data and click on `Re-scan field values now`.

So we can refresh the dashboard.

### Troubleshooting: a (painful) story 🥺

💥... There are only 3 values in the report. 

The users are pissed now 😡.

They cannot work, the data is nothing but ridiculous.

You lost their trust 😩.

They come at you, asking question, potentially yelling. You don't know what is going on. You want information, so you ask them and yourself:

- What is the problem?
- Which report?
- Can I see it?
- What did you expect?
- Where is the data?
- Can I have access to it (in production)?
- What does it look like?
- What did it looked like? What is so different? ⚠️
- What is the application?
- Where is the code?

> Most of the questions will be left without answers, will be negative, or will take a huge amount of time -- the users are still pissed, the trust is broken.

Eventually, after some time you get the information that the stakeholders were expecting more data because there must be an entry for each open day.

You start looking at:
- the report file, it has 3 values
- the spark code, you see the filter and the data being used
- the monthly csv file, you compute the values for buzzfeed based on the filter
- the pandas code, you see the merge and the files read
- you go check the buzzfeed csv file... and you see something `weird`, visually, the `Symbol`.

We were lucky:
- we have access to the data
- we know where are the application
- we understand the code
- the logic is quite fresh in our mind
- we don't have much data which helped us identifying the change with our 👀 only

But we are not sure this is an issue.

So we ask time from stakeholders to understand it: the stock has changed, now we need to track BZFD. 

So basically, the quality of the report produced is sensitive to the number of `Symbol`!

Here is the situation we have discovered
![](images/4%20-%20Pipeline%20Data%20Stock%20Split.png).

What we have learned, the hard way, two things:
- The amount of data cannot variate too much between two months (working days)
- The number of `Symbol`s too

## Introduce Data Observability (at the Source) 
Add information aboyt data, lineage, and historical behavior.

### Configure Data Observability Agent


> Review code in `with_do`

To run it, we need the configuration file to be provided as ENV
Let's copy the default file locally and set the variable:

```sh
cp ../conf.ini ../.conf.ini
export CONF_FILE=../.conf.ini
vim ../.conf.ini
```

And fill in the `token` and `PAT`, then save with `<ESC>:wq`.
### November

```sh
python3 with_do/data_ingestion.py nov 2021 ; python3 with_do/reporting_spark.py nov 2021
```

#### Add rule in Kensu Data Observability Platform

Go add the business rule => Delta => expresses the risk taken

### December
```sh
python3 with_do/data_ingestion.py dec 2021 ; python3 with_do/reporting_spark.py dec 2021
```

### Troubleshooting: like a boss 😎
> error! but what if no error... we see the value exploding. An automated observer can too...



## Data Observability with Rules

> what if we knew some business rules.. or simply we anticipated the error (like in tests)? 
> => rule programmatically

### January


```sh
python3 with_rules/data_ingestion.py jan 2022 ; python3 with_rules/reporting_spark.py jan 2022
```