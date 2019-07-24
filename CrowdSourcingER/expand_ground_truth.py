import pandas as pd
import os
from pyspark.sql import SparkSession
from storing import mongoDB as md

df = pd.read_csv(os.path.join(".","oracolo","true_predictions.csv"))

spark = SparkSession.builder.appName('bigData')\
                    .config("spark.mongodb.output.uri",config.MONGO_URI)\
                    .getOrCreate()

oracolo = spark.read.format("csv")\
  .option("sep", "\t")\
  .option("inferSchema", "true")\
  .option("header", "true")\
  .load("oracolo/true_predictions.csv")\
  .rdd

print("\n\nPRECISION:"+str(measures.precision(oracolo))+"%\n\n")

for index,row in df.iterrows():
    if row["response"]==1:
        md.expand_ground_truth(row['ltable_id'],row['rtable_id'],"cameras")
    if row["response"]==0:
        md.expand_ground_false(row['ltable_id'],row['rtable_id'],"cameras")
