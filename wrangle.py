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
    Used for scaling ex. This function takes in the zillow df
    then the data is cleaned and returned
    '''
    df = df.drop('propertylandusetypeid', axis=1)
    #change column names to be more readable
    df = df.rename(columns={'bedroomcnt':'bedrooms','bathroomcnt':'bathrooms', 'calculatedfinishedsquarefeet':'sqft', 'taxvaluedollarcnt':'home_value', 'taxamount':'sale_tax', 'yearbuilt':'year_built'})

    #drop null values- at most there were 9000 nulls (this is only 0.5% of 2.1M)
    df = df.dropna()

    #drop duplicates
    df.drop_duplicates(inplace=True)
   
    return df

def drop_propertylandusetypeid(df):
    df = df.drop('propertylandusetypeid', axis=1)
    return df

def drop_nulls(df):
    df = df.dropna()
    return df

def drop_nobed_nobath(df):
    df = df[(df.bedroomcnt != 0) & (df.bathroomcnt != 0) & (df.calculatedfinishedsquarefeet >= 70)]
    return df

def squish_outliers(df):
    #take out outliers
    df = df[df.bathroomcnt <= 6]
    df = df[df.bedroomcnt <= 6]
    df = df[df.taxvaluedollarcnt < 2_000_000]
    return df

def wrangled_zillow(df):
    # df = drop_propertylandusetypeid(df)

    df = drop_nulls(df)
    df = drop_nobed_nobath(df)
    df = squish_outliers(df)
    df.to_csv("zillow.csv", index=False)
    return df

def split_zillow(df):
    #df = train_validate_test(df)
    train_validate, test = train_test_split(df, test_size=0.2, random_state=123, stratify=df.fips)
    #stratify is used for categorical data
    train, validate = train_test_split(train_validate, test_size=0.25, random_state=123, stratify=train_validate.fips)
    #Stratified by county for an even distribution on the train validate test data sets
    return train, validate, test
    #go back and stratify properly on fips
    
    
   #SCALER VISUALIZATION
def visualize_scaler(scaler, df, columns_to_scale, bins=10):
    #Create subsets 
    to_scale = ['bedrooms','bathrooms','sqft','year_built','sale_tax']
    #create subplot structure
    fig, axs = plt.subplots(len(columns_to_scale), 2, figsize=(12,12))

    #copy the df for scaling
    df_scaled = df.copy()
    
    #fit and transform the df
    df_scaled[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

    #plot the pre-scaled data next to the post-scaled data in one row of a subplot
    for (ax1, ax2), col in zip(axs, columns_to_scale):
        ax1.hist(df[col], bins=bins)
        ax1.set(title=f'{col} before scaling', xlabel=col, ylabel='count')
        ax2.hist(df_scaled[col], bins=bins)
        ax2.set(title=f'{col} after scaling with {scaler.__class__.__name__}', xlabel=col, ylabel='count')
    plt.tight_layout()
# call function with MinMaxScaler(), StandardScaler, RobustScaler(), QuantileTransformer(output_distribution='normal') and QuantileTransformer()  for graphs
# visualize_scaler(scaler=MinMaxScaler(), 
#                  df=train, 
#                  columns_to_scale=to_scale, 
#                  bins=50)