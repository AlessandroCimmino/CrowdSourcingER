from storing import mongoDB as md
from pyspark.sql import SparkSession
from adapter.deepmatcher import gt_to_train as ad
from adapter.deepmatcher import gt_to_predict as pd
from classifiers.deepmatcher import dpm as dm
from classifiers import predictions_union as pu
from adapter.jedai import gt_to_train as jd
import os
import pandas
import config
import measures

spark = SparkSession.builder.appName('bigData')\
                    .config("spark.mongodb.output.uri",config.MONGO_URI)\
                    .getOrCreate()

##########################PREPARAZIONE DATI DI TRAINING###################

#Retrieve dei file di entità e json_files da mongoDB
entities,json_files = md.get_ground_truth(spark,config.VERTICAL)

#Preparazione dataframe per training deepmatcher
training_df = ad.to_train((entities,json_files),spark)

#Preparazione csv per training jedai
jd.to_train(entities,json_files)

##########################ADDESTRAMENTO MODELLI##########################

#addestramento modello deepmatcher
model = dm.dm_train(training_df)

##############PREPARAZIONE UNLABELED E CALCOLO PREVISIONI#################

#Creazione del csv con le istanze da predire per deepmatcher
pd.to_predict((entities,json_files),spark)

#Calcolo delle predizioni con deepmatcher
predictions = dm.dm_prediction(model)

predictions.to_csv(config.PATHS['deepmatcher_predictions'],",",index=False)

#FITTIZI
predictions.to_csv(config.PATHS['jedai_predictions'],",",index=False)
predictions.to_csv(config.PATHS['magellan_predictions'],",",index=False)


####################UNIONE DELLE PREDIZIONI#############################

#Retrieve delle coppie di istanze negative secondo l'oracolo
fpairs = md.get_ground_false(spark,config.VERTICAL)

#Unione delle predizioni da sottomettere all'oracolo
union = pu.union(spark,fpairs,spark.read\
         .format("csv")\
         .option("header", "true")\
         .load(config.PATHS['deepmatcher_predictions']),\
         spark.read\
        .format("csv")\
        .option("header", "true")\
        .load(config.PATHS['jedai_predictions']),\
         spark.read\
        .format("csv")\
        .option("header", "true")\
        .load(config.PATHS['magellan_predictions']))


union.to_csv(config.PATHS['union'],index=False)

to_filter = pandas.read_csv(config.PATHS['union'])

#Diamo all'oracolo solo le coppie con match_score alto per ogni black box
filtered = to_filter[(to_filter['deepmatcher_score'] >= 0.9)\
                        & (to_filter['magellan_score'] >=0.9)\
                        & (to_filter['jedai_score'] >=0.9)]

filtered.to_csv(config.PATHS['oracle_input'],index=False)

oracolo = spark.read.format("csv")\
  .option("sep", "\t")\
  .option("inferSchema", "true")\
  .option("header", "true")\
  .load("oracolo/true_predictions.csv")\
  .rdd

print("\n\nPRECISION:"+str(measures.precision(oracolo))+"%\n\n")
