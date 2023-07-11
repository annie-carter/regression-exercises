def split_zillow(df):
    #df = train_validate_test(df)
    #stratify is used for categorical data we are using fips(Ventura, Orange Cty and Los Angelos)
    train_validate, test = train_test_split(df, test_size=0.2, random_state=123, stratify=df.fips)
    train, validate = train_test_split(train_validate, test_size=0.25, random_state=123, stratify=train_validate.fips)
    return train, validate, test

def x_y_split(zillow_train,zillow_validate,zillow_test):
    x_train, y_train = zillow_train.select_dtypes('float').drop(columns='taxvalue'),zillow_train.taxvalue
    x_validate, y_validate = zillow_validate.select_dtypes('float').drop(columns='taxvalue'),zillow_validate.taxvalue
    x_test, y_test = zillow_test.select_dtypes('float').drop(columns='taxvalue'),zillow_test.taxvalue
    return x_train, y_train,x_validate,y_validate,x_test,y_test
def models(y_train):
    models= pd.DataFrame(