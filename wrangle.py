import pandas as pd
import numpy as np
import os
from env import hostname, user, password
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
import warnings
warnings.filterwarnings("ignore")

def get_connection(db, user=user, hostname =hostname, password=password):
    return f'mysql+pymysql://{user}:{password}@{hostname}/{db}'

def zillow_data():
    #Save before editing so that we still have the original on hand
    filename = "zillow.csv"
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        return get_zillow_data()

def get_zillow_data():
    #this sql code for answers 
    sql_query = """SELECT
    bedroomcnt,
    bathroomcnt,
    calculatedfinishedsquarefeet,
    taxvaluedollarcnt,
    yearbuilt,
    taxamount,
    fips,
    propertylandusetypeid
FROM
    properties_2017
        JOIN
    propertylandusetype USING (propertylandusetypeid)
WHERE
    propertylandusetypeid = 261
        OR propertylandusetypeid = 279;"""
    df = pd.read_sql(sql_query, get_connection('zillow'))
    return df

def prep_zillow(df):
    '''
    pulled from prepare.py
    '''
    df = df.drop('propertylandusetypeid', axis=1)
    #change column names to be more readable
    df = df.rename(columns={'bedroomcnt':'bedrooms','bathroomcnt':'bathrooms', 'calculatedfinishedsquarefeet':'sqft', 'taxvaluedollarcnt':'home_value', 'taxamount':'sale_tax', 'yearbuilt':'year_built'})
    #drop null values- at most there were 9000 nulls
    df = df.dropna()
    #drop duplicates
    df.drop_duplicates(inplace=True)
   
    return df

def drop_propertylandusetypeid(df):
    df = df.drop('propertylandusetypeid', axis=1)
    return df

def drop_nulls(df):
    df = df.dropna(df)
    return df

def remove_nobed_nobath(df):
    df = df[(df.bedrooms != 0) & (df.bathrooms != 0) & (df.sqft >= 70)]
    return df



def wrangled_zillow(df):
    df = remove_nobed_nobath(df)
    df = remove_outliers(df)
    df.to_csv("zillow.csv", index=False)
    return df


def dtype_zillow(df):
    # Convert bedrooms, bathrooms, and sqft columns to integers
    df['bedrooms'] = df['bedrooms'].astype(int)
    df['bathrooms'] = df['bathrooms'].astype(int)
    df['sqft'] = df['sqft'].astype(int)
    
    # Convert year_built and fips columns to integers and then to strings
    df['year_built'] = df['year_built'].astype(int).astype(str)
    df['fips'] = df['fips'].astype(int).astype(str)   
    return df

def remove_outliers(df):
    #eliminate outliers
    df = df[df.bathrooms <= 9]
    df = df[df.bedrooms <= 8]
    df = df[df.home_value < 2_000_000]
    return df   

def split_zillow(df):
    #df = train_validate_test(df)
    #stratify is used for categorical data we are using fips(Ventura, Orange Cty and Los Angelos)
    train_validate, test = train_test_split(df, test_size=0.2, random_state=123, stratify=df.fips)
    train, validate = train_test_split(train_validate, test_size=0.25, random_state=123, stratify=train_validate.fips)
    return train, validate, test

    
    