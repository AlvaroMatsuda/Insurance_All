import pickle
import pandas as pd
import numpy as np

class HealthInsurance(object):
    def __init__(self):
        self.home_path = '/home/kazu/Repos/pa004_health_insurance_cross_sell/'
        self.age_scaler = pickle.load(open(self.home_path + 'src/features/age_scaler.pkl', 'rb'))
        self.annual_premium_scaler = pickle.load(open(self.home_path + 'src/features/annual_premium_scaler.pkl', 'rb'))
        self.delta_premium_by_region_scaler = pickle.load(open(self.home_path + 'src/features/delta_premium_by_region_scaler.pkl', 'rb'))
        self.median_premium_by_region_scaler = pickle.load(open(self.home_path + 'src/features/median_premium_by_region_scaler.pkl', 'rb'))
        self.policy_sales_channel_scaler = pickle.load(open(self.home_path + 'src/features/policy_sales_channel_scaler.pkl', 'rb'))
        self.region_code_scaler = pickle.load(open(self.home_path + 'src/features/region_code_scaler.pkl', 'rb'))
        self.vehicle_damage_region_code_scaler = pickle.load(open(self.home_path + 'src/features/vehicle_damage_region_code_scaler.pkl', 'rb'))
        self.vintage_scaler = pickle.load(open(self.home_path + 'src/features/vintage_scaler.pkl', 'rb'))
        self.ohc_gender_scaler = pickle.load(open(self.home_path + 'src/features/ohc_gender_scaler.pkl', 'rb'))
        self.vehicle_age_scaler = pickle.load(open('src/features/ohc_vehicle_age_scaler.pkl', 'rb'))
        self.vehicle_damage_scaler = pickle.load(open('src/features/ohc_vehicle_damage_scaler.pkl', 'rb'))

        
    def rename_columns(self, data):
        cols_new = {'id': 'id',
                    'Gender': 'gender',
                    'Age': 'age',
                    'Driving_License': 'driving_license',
                    'Region_Code': 'region_code',
                    'Previously_Insured': 'previously_insured',
                    'Vehicle_Age': 'vehicle_age',
                    'Vehicle_Damage': 'vehicle_damage',
                    'Annual_Premium': 'annual_premium',
                    'Policy_Sales_Channel': 'policy_sales_channel',
                    'Vintage': 'vintage'}
        
        data.rename(columns=cols_new, inplace=True)
        
        return data
        
    def feature_engineering(self, data):
        # median_premium_by_region

        # Calculating Median Annual Premium by Region_code
        dict_region_code = data[['annual_premium', 'region_code']].groupby('region_code').median().to_dict(orient='dict')['annual_premium']

        # Mapping region code to input median premium by region_code
        data['median_premium_by_region'] = data['region_code'].map(dict_region_code)

        # delta_annual_premium_by_region
        data['delta_premium_by_region'] = data['annual_premium'] - data['median_premium_by_region']

        # vehicle_damage percentage by region_code

        # percentage of vehicle_damage==1 by region_code
        perc_region_code = {}
        for i in data['region_code'].unique():
            perc_region_code[i] = ((data['vehicle_damage'] == 'Yes') & (data['region_code'] == i)).sum() / (data['region_code'] == i).sum()

        # Mapping region code to input percentage of vehicle_damage == Yes
        data['vehicle_damage_region_code'] = data['region_code'].map(perc_region_code)


        # discretize age (adult 1, adult 2, )
        data['age_discretized'] = data['age'].apply(lambda x: 'adult 1' if x<=39 else 
                                                                'adult 2' if x<=59 else
                                                                'old')
            
        return data
        
    def data_preparation(self, data):
        # annual_premium - StandardScaler
        data['annual_premium'] = self.annual_premium_scaler.transform(data[['annual_premium']].values)

        # age - MinMaxScaler
        data['age'] = self.age_scaler.transform(data[['age']].values)

        # vintage - MinMaxScaler
        data['vintage'] = self.vintage_scaler.transform(data[['vintage']].values)

        # delta_premium_by_region - MinMaxScaler
        data['delta_premium_by_region'] = self.delta_premium_by_region_scaler.transform(data[['delta_premium_by_region']].values)

        # gender - **One Hot Encoding**
        data['gender_Female'] = self.ohc_gender_scaler.transform(data[['gender']]).toarray()[:,0]
        data['gender_Male'] = self.ohc_gender_scaler.transform(data[['gender']]).toarray()[:,1]
        data.drop(columns='gender', inplace=True)

        # driving_license - already encoded (0 /1)

        # region_code - Frequency Encoding or **Target Encoding**
        data['region_code'] = data['region_code'].map(self.region_code_scaler)

        # previously_insured - already encoded (0 /1)

        # vehicle_age - **One Hot Encoding** / Frequency Encoding / Order Encoding
        data['vehicle_age_1-2 Year'] = self.vehicle_age_scaler.transform(data[['vehicle_age']]).toarray()[:,0]
        data['vehicle_age_< 1 Year'] = self.vehicle_age_scaler.transform(data[['vehicle_age']]).toarray()[:,1]
        data['vehicle_age_> 2 Years'] = self.vehicle_age_scaler.transform(data[['vehicle_age']]).toarray()[:,2]
        data.drop(columns='vehicle_age', inplace=True)

        # vehicle_damage **One Hot Encoding** / Frequency Encoding / Order Encoding
        data['vehicle_damage_No'] =  self.vehicle_damage_scaler.transform(data[['vehicle_damage']]).toarray()[:,0]
        data['vehicle_damage_Yes'] =  self.vehicle_damage_scaler.transform(data[['vehicle_damage']]).toarray()[:,1]
        data.drop(columns='vehicle_damage', inplace=True)

        # policy_sales_channel - Target Encoding / **Frequency Encoding**
        data['policy_sales_channel'] = data['policy_sales_channel'].map(self.policy_sales_channel_scaler)
        data['policy_sales_channel'].fillna(data['policy_sales_channel'].min(), inplace=True)

        # median_premium_by_region - **Frequency Encoding** or Target Encoding
        data['median_premium_by_region'] = data['median_premium_by_region'].map(self.median_premium_by_region_scaler)

        # vehicle_damage_region_code - **Frequency Encoding** or Target Encoding
        data['vehicle_damage_region_code'] = data['vehicle_damage_region_code'].map(self.vehicle_damage_region_code_scaler)

        cols_selected = ['vintage', 'annual_premium', 'age', 'vehicle_damage_Yes', 'policy_sales_channel',
                             'previously_insured', 'region_code', 'vehicle_age_< 1 Year', 'gender_Male']

        return data[cols_selected]

    def get_prediction(self, model, original_data, test_data):
        # model prediction
        pred = model.predict_proba(test_data)
        
        # join prediction into original data
        original_data['score'] = pred[:, 1].tolist()
        
        return original_data.to_json(orient='records', date_format='iso')
