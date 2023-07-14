import sys
import unittest
import pandas as pd 
from src.logs import log 
from src.exception import CustomException



# Set a logger File 
logger = log(path="Log_File/", file= "tests.logs")

class TestDataLoader(unittest.TestCase):

     
    try:
        def test_train_data(self):
                
                df = pd.read_csv('data/raw_data/train.csv')
                message = "Shape of train data and defined value are same"
                self.assertEqual(df.shape, (800, 22), message)

    except Exception as e:
          raise CustomException(e, sys)

                


if __name__ == '__main__':
        unittest.main()
