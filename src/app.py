# Importing Packages
import streamlit as st
import pandas as pd
import os

st.title("Sales Forecast App for Corporation Favorita")
st.write("""Welcome to Corporation Favorita Sales Prediction app!
         This app allows you to predict the Sales for a specific 
         product in a chosen store at Corporation Favorita
     
     """)

product_name = st.text_input("Enter the name of the product")
Promotion = st.selectbox("On promotion,0 for No and 1 for Yes",[0,1])
transactions = st.number_input("Enter the number of transactions for the product")
dcoilwtico = st.number_input("Enter the oil price (dcoilwtico)")
year = st.number_input("year",step=1)

products = st.selectbox('products',['AUTOMOTIVE', 'CLEANING', 'BEAUTY', 'FOODS', 'STATIONERY',
       'CELEBRATION', 'GROCERY', 'HARDWARE', 'HOME', 'LADIESWEAR',
       'LAWN AND GARDEN', 'CLOTHING', 'LIQUOR,WINE,BEER', 'PET SUPPLIES'])
state = st.selectbox('state',['Pichincha', 'Cotopaxi', 'Chimborazo', 'Imbabura',
       'Santo Domingo de los Tsachilas', 'Bolivar', 'Pastaza',
       'Tungurahua', 'Guayas', 'Santa Elena', 'Los Rios', 'Azuay', 'Loja',
       'El Oro', 'Esmeraldas', 'Manabi'])
dayofweek = st.number_input("dayofweek,0=Sun and 6=Sat",step=1)
month = st.slider("month",1,12)
day = st.slider("day",1,31)

# Prediction
if st.button("predict"):
    #Dataframe Creation
    df = pd.DataFrame(
      {
       "product_name" : [product_name], "Promotion_1":  [Promotion], "transactions":[transactions]
          
      }  
   
    )

    print(f"[info] Input data as dataframe :\n{df.to_markdown()}")



