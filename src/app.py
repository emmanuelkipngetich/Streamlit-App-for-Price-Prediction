# Importing Packages
import streamlit as st
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder


st.title("Sales Forecast App for Corporation Favorita")
st.write("""Welcome to Corporation Favorita Sales Prediction app!
         This app allows you to predict the Sales for a specific 
         product in a chosen store at Corporation Favorita
     """)

Promotion = st.selectbox("On promotion,0 for No and 1 for Yes", [0, 1])
transactions = st.number_input("Enter the number of transactions for the product")
dcoilwtico = st.number_input("Enter the oil price (dcoilwtico)")
year = st.number_input("year", step=1)

products = st.selectbox('products', ['AUTOMOTIVE', 'CLEANING', 'BEAUTY', 'FOODS', 'STATIONERY',
                                     'CELEBRATION', 'GROCERY', 'HARDWARE', 'HOME', 'LADIESWEAR',
                                     'LAWN AND GARDEN', 'CLOTHING', 'LIQUOR,WINE,BEER', 'PET SUPPLIES'])
state = st.selectbox('state', ['Pichincha', 'Cotopaxi', 'Chimborazo', 'Imbabura',
                               'Santo Domingo de los Tsachilas', 'Bolivar', 'Pastaza',
                               'Tungurahua', 'Guayas', 'Santa Elena', 'Los Rios', 'Azuay', 'Loja',
                               'El Oro', 'Esmeraldas', 'Manabi'])
dayofweek = st.number_input("dayofweek,0=Sun and 6=Sat", step=1)
month = st.slider("month", 1, 12)
day = st.slider("day", 1, 31)

# Prediction
if st.button("predict"):
    # Dataframe Creation
    df = pd.DataFrame({
        "Promotion_1": [Promotion],
        "transactions": [transactions],
        "dcoilwtico": [dcoilwtico],
        "year": [year],
        "products": [products],
        "state": [state],
        "dayofweek": [dayofweek],
        "month": [month],
        "day": [day]
    })

    # Data Preprocessing
    # Dividing numerical and categorical columns
    num_columns = df.select_dtypes(include=['int64', 'float64', 'int32', 'UInt32', 'int8']).columns
    cat_columns = df.select_dtypes(include=['object']).columns

    # Imputing the numerical columns using mean
    numerical_imputer = SimpleImputer(strategy='mean')
    df[num_columns] = numerical_imputer.fit_transform(df[num_columns])

    # Imputing missing values for categorical columns
    categorical_imputer = SimpleImputer(strategy='most_frequent')
    df[cat_columns] = categorical_imputer.fit_transform(df[cat_columns])

    # Encoding Categorical columns
    encoder = OneHotEncoder(sparse=False, drop='first', handle_unknown='error')
    encoded_data = encoder.fit_transform(df[cat_columns])
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(input_features=cat_columns))

    # Concatenate the encoded dataframe with the original dataframe
    df_encoded = pd.concat([df[num_columns], encoded_df], axis=1)

    # Taking a look at the encoded dataset
    print(f"[info] Input data as dataframe :\n{df_encoded.to_markdown()}")
