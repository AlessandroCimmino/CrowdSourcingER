import parse_ground_truth as gt
from pyspark.sql import SparkSession
from storing import mongoDB as md
import config

spark = SparkSession.builder.appName('bigData')\
                    .config("spark.mongodb.output.uri",config.MONGO_URI)\
                    .getOrCreate()

entities_df = gt.parse_entites(spark)
json_files_df = gt.parse_json_files(spark)

md.store_ground_truth((entities_df,json_files_df),"cameras")
