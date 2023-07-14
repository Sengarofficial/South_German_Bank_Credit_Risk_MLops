import sys
import os 
import joblib
import pickle
import json
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from src.logs import log 
from src.exception import CustomException
from src.utils.config_utils import read_params
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from imblearn.over_sampling import ADASYN
from sklearn.model_selection import  cross_val_score
from sklearn.metrics import accuracy_score,  confusion_matrix ,precision_score, recall_score, f1_score, roc_auc_score



"""
[funtion for splitting dataset for training ]
Arguments:
    config_path {string}  -- Path to directory defined at params.yaml 

Return: 
    [None] 

"""




# Set a logger File 
logger = log(path="Log_File/", file= "split_data.logs")


def eval_metrics(actual, pred):

    try:

        accu = accuracy_score(actual, pred)
        ps = precision_score(actual, pred)
        rs = recall_score(actual, pred)
        fs = f1_score(actual, pred)
        ruc = roc_auc_score(actual, pred)
        logger.info("model metrics calculated..!!")
        return accu, ps, rs, fs, ruc
    
    except Exception as e:
        raise CustomException(e, sys) 

def split_and_saved_data(config_path: str):

    # read the config_path 
    logger.info("Reading Configuration Through read_params method...")

    try:

        config = read_params(config_path)
        logger.info("Reading YAML Configuration...")

        raw_data_path = config["processed_data"]["processed_train"]
        split_ratio = config["base"]["test_size"]
        random_state = config["base"]["random_state"]
        target = config["base"]["target_col"]
        n_estimators = config["estimators"]["XGBClassifier"]["params"]["n_estimators"]
        max_depth = config["estimators"]["XGBClassifier"]["params"]["max_depth"]
        learning_rate = config["estimators"]["XGBClassifier"]["params"]["learning_rate"]
        booster = config["estimators"]["XGBClassifier"]["params"]["booster"]

        logger.info("Reading Dataframe...")
        df = pd.read_csv(raw_data_path, sep=",", encoding='utf-8')
        #print(df.columns)
        #print(target)
        df = df.drop(['id'], axis = 1)
        X_final = df.drop(target, axis = 1)
        y_final = df[target]
        print(X_final.columns)
        #print(y_final)

        logger.info("Splitting Dataset...")
        X_train, X_test, y_train, y_test = train_test_split(X_final, y_final,
                                                            test_size=split_ratio, 
                                                            random_state = random_state)
        
        print(X_train.head())
        print(y_train.head())

        #Scaling 

        scaler=StandardScaler()

        X_train = scaler.fit_transform(X_train)

        logger.info("train scaling done..!!")

        print(X_test)
        print(X_test.columns)

        X_test =scaler.transform(X_test)

        logger.info("test data transform done...!!")


        with open("saved_models/scale_models/scaling.pkl", "wb") as f:
            pickle.dump(scaler, f)

        logger.info("Scaling.pkl file saved successfully...!!")

        ada = ADASYN(sampling_strategy='minority',random_state=42,n_neighbors=7)
        X_res,y_res = ada.fit_resample(X_train,y_train)
        

        xgb_clf =  XGBClassifier(n_estimators=n_estimators,max_depth=max_depth,
                                random_state=random_state,learning_rate=learning_rate,
                            booster=booster)
        
        logger.info("classifier defined...!!")


        xgb_clf.fit(X_res,y_res)

        y_pred = xgb_clf.predict(X_test)
        logger.info("prediction on test dataset completed..!!")


        accu, ps, rs, fs, ruc = eval_metrics(y_test, y_pred)

        print('Accuracy XGBoost...{}'.format(accu))
        print('Precision XGBoost...{}'.format(ps))
        print('Recall XGBoost...{}'.format(rs))
        print('F1 XGBoost...{}'.format(fs))
        print('roc_auc_score XGBoost...{}'.format(ruc))
        print('XGBoost_Confusion Matrix')
        print(confusion_matrix(y_test, y_pred))


        f1 = cross_val_score(xgb_clf, X_train, y_train, cv=5, scoring='f1')
        print('\nFinal F1 score of the model:', round(f1.mean(),2)) 


        ###########################################################################

        scores_file = config["reports"]["scores"]
        params_file = config["reports"]["params"]


        with open(scores_file, "w") as f:
            scores = {
                "accuracy": accu,
                "precision score": ps,
                "recall score": rs,
                "F1_Score": fs,
                "RUC": ruc
            }
            json.dump(scores, f, indent=4)

        with open(params_file, "w") as f:
            params = {
                "n_estimators": n_estimators,
                "max_depth": max_depth,
                "random_state": random_state,
                "learning_rate": learning_rate,
                "booster": booster,
                "random_state": random_state

            }
            json.dump(params, f, indent=4) 


            #################################################################################

            model_dir = config["saved_models"]["classifier"]
            model_path = os.path.join(model_dir, "xgb_clf.joblib")

            joblib.dump(xgb_clf, model_path)

    except Exception as e:
        raise CustomException(e, sys) 
        



if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    split_and_saved_data(config_path=parsed_args.config)
