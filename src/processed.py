import os
import sys
import yaml
import pandas as pd
import numpy as np 
import argparse
from src.logs import log 
from src.exception import CustomException
from src.utils.config_utils import read_params

"""
[funtion for reading train and test data ]
Arguments:
    config_path {string}  -- Path to directory defined at params.yaml 

Return: 
    [df] { DataFrame }  -- Pandas DataFrame 

"""

# Set a logger File 
logger = log(path="Log_File/", file= "load_data.logs")

try:
    def process_data(config_path: str) -> pd.DataFrame:

        # read the config_path 
        logger.info("Reading Configuration Through read_params method...")

        config = read_params(config_path)
        # print(config)

        # defining data path for reading data 
        data_path_train = config["data_source"]["cassandra_source_train"]
        data_path_test = config["data_source"]["cassandra_source_test"]
        df_train = pd.read_csv(data_path_train, sep=",", encoding='utf-8')
        df_test = pd.read_csv(data_path_test, sep=",", encoding='utf-8')
        logger.info("Read Train/Test Dataset Successfully...")


        df_train = df_train.rename(mapper={'Id': 'id', 'laufkont': 'status', 'laufzeit': 'duration', 'moral': 'credit_history', 'verw': 'purpose',
                                'hoehe': 'amount', 'sparkont': 'savings', 'beszeit': 'employment_duration', 'rate': 'installment_rate', 
                                   'famges': 'personal_status_sex', 'buerge': 'other_debtors',
                                   'wohnzeit': 'present_residence', 'verm': 'property', 'alter': 'age', 
                                   'weitkred': 'other_installment_plans', 'wohn': 'housing', 'bishkred': 'number_credits', 
                                   'beruf': 'job', 'pers':  'people_liable', 'telef': 'telephone',
                                   'gastarb': 'foreign_worker', 'kredit': 'credit_risk'},  axis= 1) # axis = 1 , belongs to columns 
        
        logger.info("Changing Train columns name from german to english")

        df_test = df_test.rename(mapper={'Id': 'id', 'laufkont': 'status', 'laufzeit': 'duration', 'moral': 'credit_history', 'verw': 'purpose',
                                'hoehe': 'amount', 'sparkont': 'savings', 'beszeit': 'employment_duration', 'rate': 'installment_rate', 
                                   'famges': 'personal_status_sex', 'buerge': 'other_debtors',
                                   'wohnzeit': 'present_residence', 'verm': 'property', 'alter': 'age', 
                                   'weitkred': 'other_installment_plans', 'wohn': 'housing', 'bishkred': 'number_credits', 
                                   'beruf': 'job', 'pers':  'people_liable', 'telef': 'telephone',
                                   'gastarb': 'foreign_worker', 'kredit': 'credit_risk'},  axis= 1) # axis = 1 , belongs to columns
        
        logger.info("Changing Test columns name from german to english ")

        
        data_path_process_train = config["processed_data"]["processed_train"]
        data_path_process_test = config["processed_data"]["processed_test"]

        logger.info("Applying log to amount, age and duration column")

        df_train['log_amount'] = round(np.log(df_train['amount']),2)
        df_test['log_amount'] = round(np.log(df_test['amount']),2)
    

        df_train['log_age'] = round(np.log(df_train['age']),2)
        df_test['log_age'] = round(np.log(df_test['age']),2)

        df_train['log_duration'] = round(np.log(df_train['duration']),2)
        df_test['log_duration'] = round(np.log(df_test['duration']),2)

        logger.info("Deleting unnecesary columns from the dataset...")

        df_train = df_train.drop(["present_residence", "housing","other_installment_plans", "installment_rate","people_liable", "number_credits", "telephone", "job", "amount", "age", "duration"], axis = 1)
        df_test = df_test.drop(["present_residence", "housing","other_installment_plans", "installment_rate","people_liable", "number_credits", "telephone", "job", "amount", "age", "duration"], axis = 1)

        #print(df_train)
        #print(df_test)

        df_train.to_csv(data_path_process_train, sep=",", index=False, encoding="utf-8")
        df_test.to_csv(data_path_process_test, sep=",", index=False, encoding="utf-8")

        
    
except Exception as e:
    raise CustomException(e, sys)



"""
Entrance point for this project....

"""



if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    process_data(config_path=parsed_args.config)
