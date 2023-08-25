from pyspark.sql import SparkSession
import sys
spark = SparkSession.builder.appName('sample_pyspark_script').master(str(sys.argv[1])).getOrCreate()
try:
    data = [(1231, 123), (123, 123), (3981, 123)]

    columns = ["employee_id","total_car_owners"]
    df = spark.createDataFrame(data=data, schema = columns)
    df.printSchema()
    df.show(truncate=False)

    dataCollect = df.collect()

    print(dataCollect)

    dataCollect2 = df.select("employee_id").collect()
    print(dataCollect2)

    for row in dataCollect:
        print(row['employee_id'] + "," +str(row['total_car_owners']))
except Exception as e:
    print(e)