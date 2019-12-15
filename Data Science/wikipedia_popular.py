#!/usr/bin/env python
# coding: utf-8

# imports
import sys
from pyspark.sql import SparkSession, functions, types
import ntpath
import re

# boilerplate 
spark = SparkSession.builder.appName('reddit averages').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

# define schema
pages_schema = types.StructType([
    types.StructField('page', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('requests', types.IntegerType()),
    types.StructField('bytes', types.IntegerType())
])

def get_date(path):
    base = ntpath.basename(path)
    try:
        res = re.search('-(.+?-\d{1,2})[0]', base).group(1)
    except AttributeError:
        res = ''
    return res
def main():
    df = spark.read.csv(sys.argv[1], sep=' ', schema=pages_schema).withColumn('filename',\
        functions.input_file_name()).cache()
    df = df.filter((df.page == 'en') & (df.title != 'Main_Page') & (~df.title.startswith('Special:')))

    path_to_hour = functions.udf(get_date, returnType=types.StringType())

    df = df.withColumn('hour', path_to_hour('filename'))

    MaxHours = df.groupBy('hour').max('requests').withColumnRenamed('max(requests)', 'max')
    MaxHours = MaxHours.withColumnRenamed('hour', 'h')

    df = df.join(MaxHours, (df.hour == MaxHours.h) & (df.requests == MaxHours.max))

    df = df.drop('h', 'max').sort('hour', 'title')
    df = df.select('hour', 'title', 'requests')
    df.write.csv(sys.argv[2], mode='overwrite')


if __name__ == '__main__':
    main()