from pymongo import MongoClient
import pymongo_spark
import config


client = MongoClient(config.MONGO_HOST, config.MONGO_PORT)

def store_datasets(datasets):
    pymongo_spark.activate()
    mongo_url = config.MONGO_URI
    for (json_files,entities,vertical) in datasets:
        json_files.saveToMongoDB(mongo_url+"ground_truth.json_files_" + vertical)
        entities.saveToMongoDB(mongo_url+"ground_truth.entities_" + vertical)


def store_ground_truth(ground_truth,vertical):
    entities,json_files = ground_truth
    try:
    	entities.write.format("com.mongodb.spark.sql.DefaultSource")\
                        .option("uri",config.MONGO_URI+"ground_truth.entities_"+vertical)\
                           .save()
    	json_files.write.format("com.mongodb.spark.sql.DefaultSource")\
                        .option("uri",config.MONGO_URI+"ground_truth.json_files_"+vertical)\
			   .save()
    except:
        print("\nGROUND_TRUTH GIA CREATA\n")

def get_ground_truth(spark,vertical):
    return (spark.read.format("com.mongodb.spark.sql.DefaultSource")\
            .option("uri",config.MONGO_URI+"ground_truth.entities_"+vertical)\
            .load(),\
            spark.read.format("com.mongodb.spark.sql.DefaultSource")\
                    .option("uri",config.MONGO_URI+"ground_truth.json_files_"+vertical)\
                    .load())

def expand_ground_truth(new_instance,old_instance,vertical):
    db = client.ground_truth
    db["entities_"+vertical].update_one({'instances':{'$elemMatch':{'$eq':old_instance}}},\
                                    {'$addToSet':{'instances':new_instance}})

def expand_ground_false(ljson_id,rjson_id,vertical):
    db = client.ground_false
    db["false_pair_"+vertical].insert_one({'left':ljson_id,'right':rjson_id})

def get_ground_false(spark,vertical):
    return spark.read.format("com.mongodb.spark.sql.DefaultSource")\
            .option("uri",config.MONGO_URI + "ground_false.false_pair_"+vertical)\
            .load()
