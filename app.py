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
Promotion = st.number_input("Enter 1 if the product was on promotion and 0 if the product was not on promotion")
transactions = st.number_input("Enter the number of transactions for the product")

# Prediction
if st.button("predict"):
    #Dataframe Creation
    pd.DataFrame(
      {
       "product_name" : [product_name], "Promotion_1":  [Promotion], "transactions":[transactions]
          
      }  
   
    )

print(f"[info] Input data as dataframe :\n{df.to_markdown()}")



