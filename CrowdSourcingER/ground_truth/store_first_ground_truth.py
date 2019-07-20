import parse_ground_truth as gt
from pyspark.sql import SparkSession
from storing import mongoDB as md

spark = SparkSession.builder.appName('bigData')\
                    .config("spark.mongodb.output.uri","mongodb://enit.inf.uniroma3.it:8080/test.MyCollection")\
                    .getOrCreate()

entities_df = gt.parse_entites(spark)
json_files_df = gt.parse_json_files(spark)

md.store_ground_truth((entities_df,json_files_df),"cameras")
