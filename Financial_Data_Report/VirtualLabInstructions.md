# Work on the pipeline

>  set Java version for Spark

```sh
jenv local 11.0
```

> go in `src` folder

```sh
cd src
```

then start the apps

```sh
python3 _yolo/data_ingestion.py nov 2021 ; python3 _yolo/reporting_spark.py nov 2021
```

Go add the business rule => Delta => expresses the risk taken



> launch Metabase and load the reports
+ https://github.com/Markenson/csv-metabase-driver
in `plugins`

Configure CSV file + `advanced` -> `&suppressHeaders=true` 
=> this says that the first line is not a header

Configure the model with column names and types

Show `scatter` plot Time x Delta

compute also the std of Delta


```sh
java -jar metabase.jar
```


```sh
python3 _yolo/data_ingestion.py dec 2021 ; python3 _yolo/reporting_spark.py dec 2021
```

load the reports again

BOOM... only 3 values. The user is pissed

Argument => check the data, the code, the input data, etc.

=> don't understand what is happening (we have the right number of inputs apparently => checked with previous data `in`) 
=> discusion with user (knowledge)
=> discover the stock split => implement fix for next run
=> add rule to control number of categories


> => we're lucky: we have access to data, its history, and it's huge




CLEAN DATA!!!????



# Make the pipeline data observable

Add information aboyt data, lineage, and historical behavior.

> Review code in `with_do`

To run it, we need the configuration file to be provided as ENV
Let's copy the default file locally and set the variable:

```sh
cp ../conf.ini ../.conf.ini
export CONF_FILE=../.conf.ini
vim ../.conf.ini
```

And fill in the `token` and `PAT`, then save with `<ESC>:wq`.

Now let's run the app with DO in:

```sh
python3 with_do/data_ingestion.py nov 2021 ; python3 with_do/reporting_spark.py nov 2021
```

Run the second month

```sh
python3 with_do/data_ingestion.py dec 2021 ; python3 with_do/reporting_spark.py dec 2021
```

> error! but what if no error... we see the valeu exploding. An automated observer can too...

> what if we knew... or simply we anticipated the error? rule prog

run third month

```sh
python3 with_rules/data_ingestion.py jan 2022 ; python3 with_rules/reporting_spark.py jan 2022
```
