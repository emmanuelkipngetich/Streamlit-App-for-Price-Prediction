# Importing Packages
import streamlit as st
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

DIRPATH = os.path.dirpath(os.path.realpath(___file___))
ml_core_fp = os.path.join(DIRPATH,"Assets","Sales_Pred_model.pkl")

# Execution
ml_components_dict = load_ml_components(fp=ml_core_fp)




st.title("Sales Forecast App for Corporation Favorita")
st.write("""Welcome to Corporation Favorita Sales Prediction app!
         This app allows you to predict the Sales for a specific 
         product in a chosen store at Corporation Favorita
     """)

date = st.date_input("Date")
Promotion = st.selectbox("On promotion,0 for No and 1 for Yes", [0, 1])
transactions = st.number_input("Enter the number of transactions for the product")
dcoilwtico = st.number_input("Enter the oil price (dcoilwtico)")

products = st.selectbox('products', ['AUTOMOTIVE', 'CLEANING', 'BEAUTY', 'FOODS', 'STATIONERY',
                                     'CELEBRATION', 'GROCERY', 'HARDWARE', 'HOME', 'LADIESWEAR',
                                     'LAWN AND GARDEN', 'CLOTHING', 'LIQUOR,WINE,BEER', 'PET SUPPLIES'])
state = st.selectbox('state', ['Pichincha', 'Cotopaxi', 'Chimborazo', 'Imbabura',
                               'Santo Domingo de los Tsachilas', 'Bolivar', 'Pastaza',
                               'Tungurahua', 'Guayas', 'Santa Elena', 'Los Rios', 'Azuay', 'Loja',
                               'El Oro', 'Esmeraldas', 'Manabi'])
city = st.selectbox('city',['Salinas', 'Machala', 'Libertad'])
weeklysales = st.number_input("weekly Sales,0=Sun and 6=Sat", step=1)
sales_lag_1 = st.number_input("Sales lag1,0=Sun and 6=Sat", step=1)
sales_lag_7 = st.number_input("Sales lag7,0=Sun and 6=Sat", step=1)
weekly_lag1 = st.number_input("weekly lag1,0=Sun and 6=Sat", step=1)
sales_rolling_avg = st.number_input("sales_rolling_avg,0=Sun and 6=Sat", step=1)

month = st.slider("month", 1, 12)
day = st.slider("day", 1, 31)

# Prediction
if st.button("predict"):
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
        "sales_lag_1":[sales_lag_1],
        "sales_lag_7":[sales_lag_7],
        "weekly_lag_1":[weekly_lag1],
        "sales_rolling_avg":[sales_rolling_avg]
    })

    # Data Preprocessing
    
    # Feature Engineering
    #New features for the year, month and days
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data['day_of_month'] = data['date'].dt.day
    data['day_of_year'] = data['date'].dt.dayofyear
    data['Week'] = data['date'].dt.isocalendar().week
    data['day_of_week'] = data['date'].dt.dayofweek

    
    # Calculate rolling averages for and 'transactions'
    window = 7  # With a window size of 7
    data['transactions_rolling_avg'] = data['transactions'].rolling(window=window).mean()
    
    # Dividing numerical and categorical columns
    num_columns = data.select_dtypes(include=['int64', 'float64', 'int32', 'UInt32', 'int8']).columns
    cat_columns = data.select_dtypes(include=['object']).columns


    # Taking a look at the encoded dataset
    print(f"[info] Input data as dataframe :\n{df_encoded.to_markdown()}")
