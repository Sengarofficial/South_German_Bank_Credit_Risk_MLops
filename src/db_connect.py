# Database Connection and Building class for fetching data 
from dotenv import load_dotenv
from cassandra.cluster import Cluster 
from cassandra.auth import PlainTextAuthProvider 
import csv 
import os

load_dotenv()
secret_id = os.getenv("client_id")
secret_key = os.getenv("client_secret")
secure_bundle = os.getenv("secure_bundle")
#print(secret_id)
#print(secret_key)
#print(secure_bundle)




class Database:

    """
    [Class to connect database and for fetching records]

    """

    def __init__(self, keyspace: str, table_name: str):

        self.keyspace = keyspace 
        self.table_name = table_name
        
        self.client_id = secret_id
        self.client_secret = secret_key


        self.secure_bundle = secure_bundle



    def connect_db(self):

        """
        [method for connnecting to the cluster/node of the database]

            Instance Variables:
                    self.client_id {strings} -- id given by database provider
                    self.client_secret {string} -- secret id given by databse provider 
                    self.secure_bundle {string} -- key:value pairs for connecting to the node/cluster 

             Returns: 
                    [IPAdress] -- [unsigned integer : status for cluster connection]

        """

        try:
           
            cloud_config= {
        'secure_connect_bundle': self.secure_bundle
            }
            auth_provider = PlainTextAuthProvider(self.client_id, self.client_secret)
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            self.session = cluster.connect()


            row = self.session.execute("select release_version from system.local").one()
            if row:
                print(row[0])
            else:
                print("An error occurred.")


        except Exception as e:
                    raise e 
        

    def fetch_records(self,  source_folder: str):


        """
        [method for fetching record from cluster/node of the database]

            Arguements:
                    self.keyspace {strings} -- schema for table
                    self.table_name {string} -- table name for saving fetched csv file
                    self.source_folder {string} -- path for saving fetched csv file

             Returns: 
                    [file] -- [readable comma separated value file]

        """


        self.connect_db()
        try:
           # Execute a SELECT statement * {all rows/columns} to retrieve the complete table
            query = f"SELECT * FROM {self.keyspace}.{self.table_name} ;"
            rows = self.session.execute(query)


            # Export the table to a CSV file
            with open(f"{source_folder}/{self.table_name}.csv", 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([column_name for column_name in rows.column_names])
                for row in rows:
                    writer.writerow(row)

            self.session.shutdown()
            self.cluster.shutdown()
                
        except Exception as e:
            return e 
        



db = Database('south_german', 'train')
tb = Database('south_german', 'test')

db.connect_db()
tb.connect_db()

db.fetch_records('data/raw_datasets')
tb.fetch_records('data/raw_datasets')
