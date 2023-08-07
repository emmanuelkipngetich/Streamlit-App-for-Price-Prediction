# Importing Packages
import streamlit as st
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
import os
import pickle

# Function to load machine learning components
def load_components_func(fp):
    #To load the machine learning components saved to re-use in the app
    with open(fp,"rb") as f:
        object = pickle.load(f)
    return object


# Loading the machine learning components
DIRPATH = os.path.dirname(os.path.realpath(__file__))
ml_core_fp = os.path.join(DIRPATH,"Assets","Sales_Pred_model.pkl")
ml_components_dict = load_components_func(fp=ml_core_fp)



# Getting the encoder,scaler and model from the components dictionary

encoder = ml_components_dict['encoder']
imputer =ml_components_dict['imputer']
scaler = ml_components_dict['scaler']
model = ml_components_dict['model']

# Streamlit App
st.set_page_config(layout="centered")

st.title("Sales Forecast App for Corporation Favorita")
st.write("""Welcome to Corporation Favorita Sales Prediction app!
         This app allows you to predict the Sales for a specific 
         product in a chosen store at Corporation Favorita
     """)

#Image
st.image("https://images.startups.co.uk/wp-content/uploads/2023/05/sales-forecast.jpg?width=709&height=460&fit=crop")
with st.form(key="information",clear_on_submit=True):
    date = st.date_input("Date")
    Promotion = st.selectbox("On promotion,0 for No and 1 for Yes", [0, 1])
    transactions = st.number_input("Enter the number of transactions for the product")
    dcoilwtico = st.number_input("Enter the oil price (dcoilwtico)")

    products = st.selectbox('products', ['AUTOMOTIVE', 'BABY CARE', 'BEAUTY', 'BEVERAGES', 'BOOKS',
        'BREAD/BAKERY', 'CELEBRATION', 'CLEANING', 'DAIRY', 'DELI', 'EGGS',
        'FROZEN FOODS', 'GROCERY I', 'GROCERY II', 'HARDWARE',
        'HOME AND KITCHEN I', 'HOME AND KITCHEN II', 'HOME APPLIANCES',
        'HOME CARE', 'LADIESWEAR', 'LAWN AND GARDEN', 'LINGERIE',
        'LIQUOR,WINE,BEER', 'MAGAZINES', 'MEATS', 'PERSONAL CARE',
        'PET SUPPLIES', 'PLAYERS AND ELECTRONICS', 'POULTRY',
        'PREPARED FOODS', 'PRODUCE', 'SCHOOL AND OFFICE SUPPLIES',
        'SEAFOOD'])
    state = st.selectbox('state', ['Santa Elena', 'El Oro', 'Guayas'])
    city = st.selectbox('city',['Salinas', 'Machala', 'Libertad'])
    weeklysales = st.number_input("weekly Sales,0=Sun and 6=Sat", step=1)


    # Prediction
    if st.form_submit_button("predict"):
        # Dataframe Creation
        data = pd.DataFrame({
            "onpromotion": [Promotion],
            "transactions": [transactions],
            "dcoilwtico": [dcoilwtico],
            "date": [date],
            "family": [products],
            "state": [state],
            "weekly_sales": [weeklysales],
            "city": [city],

        })

        # Data Preprocessing
        
        # Converting date into datetime type
        data['date'] = pd.to_datetime(data['date'])
        
        
        # Feature Engineering
        #New features for the year, month and days
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.month
        data['day_of_month'] = data['date'].dt.day
        data['day_of_year'] = data['date'].dt.dayofyear
        data['Week'] = data['date'].dt.isocalendar().week
        data['day_of_week'] = data['date'].dt.dayofweek
        window = 7  
        data['transactions_rolling_avg'] = data['transactions'].rolling(window=window).mean()
        
        # Dropping the date column
        data = data.drop("date",axis=1)
    
        # Dividing numerical and categorical columns
        num_columns = data.select_dtypes(include=['int64', 'float64', 'int32', 'UInt32', 'int8']).columns
        cat_columns = data.select_dtypes(include=['object']).columns

        # Encoding Categorical columns
        encoded_data = encoder.transform(data[cat_columns])

        # Concatenate the encoded dataframe with the original dataframe
        df_encoded = pd.concat([data[num_columns], encoded_data], axis=1)
        df_encoded = df_encoded.reindex(columns=ml_components_dict['columns'])

        #Imputing the missing values
        data_imputed = imputer.transform(df_encoded)
            # Ensure columns are in the correct order
        data_scaled = data_imputed.copy()

        # Scale the numerical columns
        columns_to_scale = ['dcoilwtico', 'transactions', 'year', 'month', 'day_of_month',
                            'day_of_year', 'Week', 'day_of_week', 'transactions_rolling_avg']
        data_scaled[columns_to_scale] = scaler.transform(data_scaled[columns_to_scale])

        # Make prediction using the model
        predictions = model.predict(data_scaled)

        # Display the predictions
        st.balloons()
        # Display the predictions with custom styling
        st.success(f"Predicted Sales: {predictions[0]:,.2f}",icon="✅")
