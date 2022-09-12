import datetime
import pickle

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder

st.set_page_config(
    page_title='Canonical Assignment',
    layout='wide'
)

st.subheader('Q3: Given the size, location and date, can you predict the cause of a wildfire?')

# transformer functions
class DateParser(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self,df):
        return self
    
    def transform(self,df):
        if 'discovery_date' in df.columns:
            try:
                df['discovery_date'] = pd.to_datetime(df['discovery_date'] - pd.Timestamp(0).to_julian_date(), unit='D')
            except:
                df['discovery_date'] = pd.to_datetime(df['discovery_date'])
            
            df['year'] = df['discovery_date'].dt.year
            df['day'] = df['discovery_date'].dt.day
            df['month'] = df['discovery_date'].dt.month
            df['day_of_week'] = df['discovery_date'].dt.day_name()
            
            df.drop(columns=['discovery_date'], inplace=True)
            return df
        else:
            print("One or more features are not in the dataframe")
            return df

class CategoricalEncoder(BaseEstimator,TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self,df):
        return self
    
    def transform(self,df):
        cat_cols = df.select_dtypes(include='object').columns
        ordinal_enc = OrdinalEncoder()
        df[cat_cols] = ordinal_enc.fit_transform(df[cat_cols])
        return df

class LabelMinimizer(BaseEstimator,TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self,df):
        return self
    
    def bin_label(self, cause):
        natural = ['Lightning']
        accidental = ['Structure','Fireworks','Powerline','Railroad','Smoking','Children','Campfire','Equipment Use','Debris Burning']
        malicious = ['Arson']
        other = ['Missing/Undefined','Miscellaneous']
        if cause in natural:
            return 1
        elif cause in accidental:
            return 2
        elif cause in malicious:
            return 3
        else:
            return 4
    
    def transform(self,df):
        df['label'] = df['stat_cause_descr'].apply(self.bin_label)
        df.drop('stat_cause_descr', axis=1, inplace=True)
        return df

class OutlierRemover(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.cols = ['fire_size']
    
    def fit(self,df):
        return self
    
    def transform(self,df):
        # 25% quantile
        Q1 = df[self.cols].quantile(.25)
        # 75% quantile
        Q3 = df[self.cols].quantile(.75)
        IQR = Q3 - Q1
        # keep the data within 3 IQR
        df = df[~((df[self.cols] < (Q1 - 3 * IQR)) |(df[self.cols] > (Q3 + 3 * IQR))).any(axis=1)]
        return df

#loading necessary assets
with open('assets/random_forest.pickle', 'rb') as f:
    model = pickle.load(f)

with open('assets/transformer.pickle', 'rb') as f:
    preprocessor = pickle.load(f)

with open('assets/state_to_int.pickle', 'rb') as f:
    state_to_int = pickle.load(f)

weekday_to_int = {
    'Wednesday': 6,
    'Monday': 1,
    'Thursday': 4,
    'Tuesday': 5,
    'Friday': 0,
    'Sunday': 3,
    'Saturday': 2
}

# define necessary functions
def return_weekday_int(weekday):
    return weekday_to_int[weekday]

def return_state_int(state):
    return state_to_int[state]

def preprocess(data):
    data = pd.DataFrame(
        data, columns=['fire_size', 'state', 'latitude', 'longitude', 'discovery_date']
    )
    processed_row = preprocessor[0].transform(data)
    processed_row['state'] = processed_row['state'].apply(return_state_int)
    processed_row['day_of_week'] = processed_row['day_of_week'].apply(return_weekday_int)
    return processed_row

def get_prediction(data):
    return model.predict(data)[0]

def get_cause(label):
    label_to_cause = {
        1: 'natural (lightning)',
        2: 'accidental',
        3: 'malicious (arson)',
        4: 'other (undefined/miscellaneous)'
    }

    return label_to_cause[label]

# streamlit widgets
states = state_to_int.keys()
state = st.selectbox(label='Choose state', options=states)

fire_size = st.slider(
     'Specify fire size',
     min_value=0.0, max_value=12.5, step=0.5, value=0.10)

longitude = st.slider(
     'Specify longitude',
     min_value=-173.3, max_value=-65.2, step=0.25, value=-120.4)

latitude = st.slider(
     'Specify latitude',
     min_value=17.9, max_value=70.3, step=0.25, value=38.9)

date = st.date_input(
     'Specify date',
     datetime.date(2005, 2, 2))

test_row = np.expand_dims(np.array([fire_size, state, latitude, longitude, date]), axis=0)

if st.button('Run inference'):
    processed_row = preprocess(test_row)
    prediction = get_prediction(processed_row)

    st.write(f'Predicted class: {get_cause(prediction)}')
