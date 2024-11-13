import pandas as pd
import streamlit as st
# import plotly.express as px
import matplotlib.pyplot as plt
import datetime
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Banque de madagascar",page_icon =":bar_chart:",layout="wide")

st.title(" :bar_chart: tableau de bord")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)

import os

def get_file_extension(filname):
    _, extension = os.path.splitext(filname)
    return f"{extension}"

fl = st.file_uploader(" :file_folder: uplod un fichier",type =(["csv","xlxs","txt","xls"]))

def upload_file(file):
    if file is not None:
        filname = file.name
        st.write(filname)
        if get_file_extension(filname)==".csv":
            df = pd.read_csv(file)
            return df

df = upload_file(fl)
Adresse = []
if fl and df.shape[0] > 0: 
    df["DateTransaction"] = pd.to_datetime(df["DateTransaction"])
    st.write(df.head())

    with st.sidebar:
        st.sidebar.header("choisissez votre filtre")
        Adresse = st.sidebar.multiselect("Adresse", df["Ville"].unique())
        
        col1, col2 = st.columns((2))

        #Pour obtenir une date max et min
        startDate = pd.to_datetime(df["DateTransaction"]).min()
        endDate = pd.to_datetime(df["DateTransaction"]).max()
    
        with col1:
            date1 = pd.to_datetime(st.date_input("Date de début",startDate))

        with col2:
            date2 = pd.to_datetime(st.date_input("Date de fin",endDate))

        df1 = (df["DateTransaction"]>= date1) & (df["DateTransaction"]<=date2).copy()


    col1, col2 = st.columns((2))
    def type_transaction_compte(data_frame):
        category_df = data_frame.groupby('TypeTransaction', as_index=False)['CompteID'].count()
        category_df = pd.DataFrame(category_df)
        #image 
        fig = ax.bar(category_df, y="CompteID", x="TypeTransaction", template = "seaborn")
        st.plotly_chart(fig,use_container_width=True , height=200)
        # st.bar_chart(category_df,y="CompteID", x="TypeTransaction")
        
    with col1:
        st.subheader("Type Transaction par compte")
        if len(Adresse) < 1 :
            type_transaction_compte(df)
        else:
            filtred_df = df[df["Ville"].isin(Adresse)]
            type_transaction_compte(filtred_df)
    
    def nombre_compte_churn(data):
        category_df = data.groupby('StatutCompte', as_index =False)['CompteID'].count()
        category_df = pd.DataFrame(category_df)
        # print(category_df)
        ###############image#######
        fig = ax.pie(category_df, values="CompteID", names="StatutCompte" , hole =0.5)
        st.plotly_chart(fig,use_container_width=True)
        # st.bar_chart(category_df, y="CompteID", x="StatutCompte")

    with col2:
        st.subheader("Statut par compte")
        if len(Adresse) < 1 :
            nombre_compte_churn(df)
        else:
            filtred_df = df[df["Ville"].isin(Adresse)]
            nombre_compte_churn(filtred_df)
