import pandas as pd
import numpy as np
import os
from env import user, password, hostname, get_db_url

def get_connection(db, user=user, host=hostname, password=password):
    '''
    Establishes connection to SQL server
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
    
    
def acquire_zillow():
    # Saves import as CSV
    filename = "zillow.csv"
    # Filename kept simple
    if os.path.isfile(filename):
        # If there is a local copy, read it
        return pd.read_csv(filename)
    else:
        # If the file doesn't exist, fetch data from the database
        zillow_data = get_zillow_data()
        return zillow_data

def get_zillow_data():
    # All data required by the project scope
    sql_query = """SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount 
                   FROM properties_2017
                """
    # The land use type represents if it is registered as a single family home
    df = pd.read_sql(sql_query, get_connection('zillow'))
    return df


