import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from PIL import Image
import streamlit.components.v1 as components
# import matplotlib.pyplot as plt
# load model
import pickle
# [theme]
base="light"
primaryColor="purple"

st.set_page_config(layout='wide')

def main():
    # st.subheader("Prediction from Model")
#         st.title("MachineLearning Analytics App")
    st.subheader("Heart Disease Prediction")
    model= pickle.load(open('model.pkl', 'rb'))
    # knn=joblib.load(model)

    # data = st.file_uploader('Upload File PDF',type='.pdf')
    # if data == None:
    #     st.write('Silakan Upload File dengan format pdf')

    # if st.button('Extract Features'):
    #     # aDict = pickle.load(open("aDict.p","rb"))
    #     text = getBagian(data)
    #     pasal = extract_pasal(text)
    #     df = pd.DataFrame.from_dict(pasal)
    #     pslist = df.pasal.unique()
    #     st.dataframe(pslist)
    #     df[['pasal','drop']] = df['pasal'].str.split(' ayat',expand=True)
    #     st.dataframe(df.pasal.unique())
    # st.subheader("Features")
    #Intializing
    co = ['Age','Sex','Chest pain type', 'Cholesterol','Max HR','Thallium']
    c1,c2 = st.columns((1,1))
    with c1:
        s1 = st.number_input(label="Age",value=20,min_value=0, max_value=150, step=1)
        s2 = st.number_input(label="Sex (0/1)",value=1,min_value=0, max_value=1, step=1)
        s3 = st.number_input(label="Chest pain type (0/1/2/3) ",value=0,min_value=0, max_value=3, step=1)
    with c2:
        s4 = st.number_input(label="Cholesterol",value=150,min_value=0, max_value=500, step=1)
        s5 = st.number_input(label="Max HR",value=100,min_value=0, max_value=300, step=1)
        s6 = st.number_input(label="Thallium (0/1/2/3)",value=1,min_value=0, max_value=3, step=1)

    if st.button("Click Here to Classify"):
        dfvalues = pd.DataFrame(list(zip([s1],[s2],[s3],[s4],[s5],[s6])),columns =co)
        input_variables = np.array(dfvalues[['Age', 'Sex','Chest pain type', 'Cholesterol','Max HR','Thallium']])
        prediction = model.predict(input_variables)
        # st.write(prediction)
        if prediction == 0:
            st.subheader('Prediction')
            st.title('Patient does not have Heart Disease')
        else:
            st.subheader('Prediction')
            st.title('Patient has Heart Disease')
        

if __name__=='__main__':
    main()
