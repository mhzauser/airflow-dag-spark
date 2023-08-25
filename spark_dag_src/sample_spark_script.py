from pyspark.sql import SparkSession
import sys
spark = SparkSession.builder.appName('sample_pyspark_script').master(str(sys.argv[1])).getOrCreate()
try:
    data = [("Finance",10), \
        ("Marketing",20), \
        ("Sales",30), \
        ("IT",40) \
    ]
    columns = ["name","id"]
    df = spark.createDataFrame(data=data, schema = columns)
    df.printSchema()
    df.show(truncate=False)

    dataCollect = df.collect()

    print(dataCollect)

    dataCollect2 = df.select("dept_name").collect()
    print(dataCollect2)

    for row in dataCollect:
        print(row['name'] + "," +str(row['id']))
except Exception as e:
    print(e)