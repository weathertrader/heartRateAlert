

#!/bin/bash

JARS=/usr/local/spark/lib/aws-java-sdk-1.7.4.jar
JARS=$JARS,/usr/local/spark/lib/hadoop-aws-2.7.1.jar
JARS=$JARS,/usr/local/spark/lib/postgresql-42.2.5.jar

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Project Directory: $PROJECT_DIR"

# Environment variables for spark application
export PYSPARK_PYTHON=/usr/bin/python3


SPARK_MASTER=spark://10.0.0.5:7077
SPARK_SUBMIT=/usr/local/spark/bin/spark-submit
PY_SPARK=$PROJECT_DIR/clean_airbnb.py

if [ -z "$1" ]; then
    echo "No process specified. Please specify the process (e.g. process_incidents.py)"
    exit 1
fi

$SPARK_SUBMIT --master "$SPARK_MASTER" --jars "$JARS" "$PROJECT_DIR/$1"