from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('AdvancedDataProcessing').getOrCreate()

# Read data
df = spark.read.csv('data.csv', header=True, inferSchema=True)

# Register DataFrame as a SQL temporary view
df.createOrReplaceTempView("data")

# Perform SQL queries
result = spark.sql("SELECT category, SUM(value) as total_value FROM data GROUP BY category")

# Show results
result.show()
