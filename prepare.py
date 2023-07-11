import pandas as pd
import numpy as np
import os
from env import hostname, user, password
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
import warnings
warnings.filterwarnings("ignore")


def prep_zillow(df):
    #Remove property land axis"
    df = df.drop('propertylandusetypeid', axis=1)
    #Change column names to enhance readability
    df = df.rename(columns={'bedroomcnt':'bedrooms','bathroomcnt':'bathrooms', 'calculatedfinishedsquarefeet':'sqft', 'taxvaluedollarcnt':'home_value', 'taxamount':'sale_tax', 'yearbuilt':'year_built'})
    #Drop nulls approx. 9000 nulls
    df = df.dropna()
    #Drop duplicates
    df.drop_duplicates(inplace=True)
    return df

def visualize_scaler(scaler, df, features_to_scale, bins=10):
    features = ['bedrooms','bathrooms','sqft','year_built','sale_tax']
    #Create subplot structure
    fig, axs = plt.subplots(len(features_to_scale), 2, figsize=(12,12))

    #copy the df for scaling
    df_scaled = df.copy()
    
    #Fit copy scale to 
    df_scaled[features_to_scale] = scaler.fit_transform(df[features_to_scale])

    #Plot pre-scaled data next to the post-scaled data in one row of a subplot
    for (ax1, ax2), col in zip(axs, columns_to_scale):
        ax1.hist(df[col], bins=bins)
        ax1.set(title=f'{col} before scaling', xlabel=col, ylabel='count')
        ax2.hist(df_scaled[col], bins=bins)
        ax2.set(title=f'{col} after scaling with {scaler.__class__.__name__}', xlabel=col, ylabel='count')
    plt.tight_layout()
    
    # USE - call function using QuantileTransformer can be replaced with MinMaxScaler, StandardScaler
visualize_scaler(scaler=QuantileTransformer(output_distribution='normal'), 
                 df=train,
                 columns_to_scale=to_scale, 
                 bins=50)