def split_zillow(df):
    #df = train_validate_test(df)
    #stratify is used for categorical data we are using fips(Ventura, Orange Cty and Los Angelos)
    train_validate, test = train_test_split(df, test_size=0.2, random_state=123, stratify=df.fips)
    train, validate = train_test_split(train_validate, test_size=0.25, random_state=123, stratify=train_validate.fips)
    return train, validate, test

def x_y_split(train, validate, test):
    x_train, y_train = train.select_dtypes('float').drop(columns='home_value'), train.home_value
    x_validate, y_validate = validate.select_dtypes('float').drop(columns='hom_value'),validate.home_value
    x_test, y_test = test.select_dtypes('float').drop(columns='home_value'), test.home_value
    return x_train, y_train,x_validate,y_validate,x_test,y_test


