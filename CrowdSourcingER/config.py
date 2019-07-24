import os

#Lista datasets presenti nel database
DATASETS =[

]

#lista di dataset da aggiungere
ADD_DATASETS = [
    {"name": "anhai",
     "path": "parsing_dataset/datasets/triplicate_labeled.csv",
     "vertical" : "movies"}
]

PATHS = {
    "jedai_gt":os.path.join(".","classifiers","jedai","training_files","jd_input_gt.csv"),
    "jedai_page_titles": os.path.join(".","classifiers","jedai","training_files","jd_page_titles.csv"),
    "deepmatcher_training_folder": os.path.join('.', 'classifiers','deepmatcher','training_files'),
    "deepmatcher_model":os.path.join('.', 'classifiers','deepmatcher','training_files','hybrid_model.pth'),
    "deepmatcher_predictions" : os.path.join(".","classifiers","deepmatcher","prediction_files","prediction.csv"),
    "jedai_predictions" : os.path.join(".","classifiers","jedai","prediction_files","prediction.csv"),
    "magellan_predictions": os.path.join(".","classifiers","magellan","prediction_files","prediction.csv"),
    "deepmatcher_unlabeled":os.path.join(".","classifiers","deepmatcher","prediction_files","unlabeled.csv"),
    "union":os.path.join(".","classifiers","deepmatcher","prediction_files","union.csv"),
    "oracle_input" : os.path.join(".","oracolo","oracle_input.csv"),
    "entities_gt":os.path.join(".","ground_truth","entities.json"),
    "json_files":os.path.join(".","ground_truth","json_files.json")
}

VERTICAL = "cameras"

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_URI = "mongodb://"+MONGO_HOST+":"+str(MONGO_PORT)+"/"
