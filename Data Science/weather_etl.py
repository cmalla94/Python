#!/usr/bin/env python
# coding: utf-8

import sys
from pyspark.sql import SparkSession, functions, types

# boilerplate code
spark = SparkSession.builder.appName('weather ETL').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

# define the schema for when the data is imported
observation_schema = types.StructType([
    types.StructField('station', types.StringType()),
    types.StructField('date', types.StringType()),
    types.StructField('observation', types.StringType()),
    types.StructField('value', types.IntegerType()),
    types.StructField('mflag', types.StringType()),
    types.StructField('qflag', types.StringType()),
    types.StructField('sflag', types.StringType()),
    types.StructField('obstime', types.StringType()),
])

# main function 
def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]

    weather = spark.read.csv(in_directory, schema=observation_schema)

    # TODO: finish here.
    # DONE
    cleaned_data = weather.filter(weather.qflag.isNull())        .filter(weather.station.startswith('CA'))        .filter(weather.observation.startswith('TMAX'))        .select(weather['station'], weather['date'], (weather.value/10).alias('tmax'))
#     cleaned_data.show()

    cleaned_data.write.json(out_directory, compression='gzip', mode='overwrite')


if __name__ == '__main__':
    main()

