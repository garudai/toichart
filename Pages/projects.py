import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
st.title("OI Chart")

df = pd.read_csv("C:\\Users\\Dell\\Documents\\optionchaindata\\Jul_06_23BNFJul_06_23_11_41.csv")
pagetitle = "TOI"
layout = "centered"
#-------------------------------------------------------------

#st.set_page_config(page_title=pagetitle, layout=layout)
st.title(pagetitle)

## ---- Drop down values for selection 

#months = [datetime.today().month, datetime.today().month + 1]

#--- Input & save periods
st.sidebar.header("Please filter here:")
expiry = df["expiryDate"].drop_duplicates()
strikes = df["strikePrice"].drop_duplicates()

Expiry = st.sidebar.selectbox('',expiry)

#Strikes = st.sidebar.selectbox('',strikes)


df_selection = df.query(
    "expiryDate == @Expiry "
)

TOIdata = df_selection.pivot_table(index=['timpestamp'], columns=['intrumentType'], values=['openInterest'],aggfunc=['sum'])
TOIdata.columns = TOIdata.columns.map(''.join)


TOIdata['OIdiff'] = TOIdata['sumopenInterestPE']-TOIdata['sumopenInterestCE']
TOIdata['Index1']=TOIdata['OIdiff'].ewm(span=10,adjust=False).mean()
TOIdata['Index2']=TOIdata['OIdiff'].ewm(span=30,adjust=False).mean()
TOIchart = TOIdata[['OIdiff','Index1','Index2']]
#st.dataframe(TOIchart)
st.line_chart(TOIchart)
