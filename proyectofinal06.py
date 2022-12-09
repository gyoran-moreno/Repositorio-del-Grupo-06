import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import gdown 
import os
import requests
import json
from streamlit_lottie import st_lottie


#cabecera para los gifs, para que se puedan ser descargados o se puedan subir desde el ordenador
def load_lottiefile(filepath: str):
	with open(filepath, "r") as f:
		return json.load(f)

def load_lottieurl(url: str):
	r= requests.get(url)
	if r.status_code != 200:
		return None
	return r.json()

#menu de seleccionar, para que asi sea mas facil ir a información y los integrantes
selected = option_menu(
	menu_title=None,
	options=["INICIO", "INFORMACIÓN", "INTEGRANTES"],
	icons=["house","book","envelope"],
	menu_icon="cast",
	default_index= 0,
	orientation="horizontal",
)
#nombre y url del gif a subir
lottie_grupo= load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_z4uccqir.json")

#boton de integrantes mas información adicional
if selected == "INTEGRANTES":
	st.title("GRUPO 06")
	st.subheader("MIEMBROS DEL GRUPO")
	col1, col2= st.columns([2,2])
	with col1:
		st.markdown("""
			- ENRIQUE OROZCO MENDOZA
			- JIMENA MILUSKA PEÑA MEJIA
			- VALERY KRYSTAL SICCHA HUAYANAY
			- SEBASTIAN ANTONIO SALDAÑA RODRIGUEZ
			- GYORAN ZAITO MORENO HUASUPOMA
		    """)
	with col2:
		st.markdown("""
			- correo: enrique.orozco@upch.pe
			- correo: jimena.pena@upch.pe
			- correo: valery.siccha@upch.pe
			- correo: sebastian.saldana@upch.pe
			- correo: gyoran.moreno@upch.pe
			""")
	st_lottie(lottie_grupo, key="house")
	st.write("---")

#nombre y url del gif a subir
lottie_info= load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_tzv8osvb.json")

#boton de información mas información adicional
if selected == "INFORMACIÓN":
	st.title("INFORMACIÓN SOBRE LA PÁGINA")
	col1, col2= st.columns([3,2])
	with col1:
		st.write("""
			*La información que contiene la página permite saber sobre el estado de licenciamiento de la universidad, así mismo información adicional, los datos son del DataSet “Sunedu - Licenciamiento institucional” elaborado por el Ministerio de educación del Perú.*
			""")
	with col2:
		st_lottie(lottie_info, height= None, width=150, key="info")
	st.info("Información de la tabla: https://www.datosabiertos.gob.pe/dataset/sunedu-licenciamiento-institucional")
	st.write("---")

#nombre y url del gif a subir
lottie_bienve= load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_qjEvNMXYul.json")

#inicio de la pagina

st.title("SUNEDU - LICENCIAMIENTO INSTITUCIONAL")

col1, col2= st.columns([3,2])

with col1:
	st.markdown("""
		Nuestra presente página es para ayudar a estudiantes y/o padres de familia que busca si cierta universidad está licenciada o no por parte de SUNEDU
		---
		""")
with col2:
	st_lottie(lottie_bienve,height= 280, width=250, key="hello")

#descarga y lectura del dataset

#id= 1XHTCztia4fEDwsUciKVLmFEFcMAnvT6n
@st.experimental_memo
def download_data():
	#https://drive.google.com/uc?id=YOURFILEID
	url = "https://drive.google.com/uc?id=1XHTCztia4fEDwsUciKVLmFEFcMAnvT6n"
	output = 'data.csv'
	gdown.download(url,output,quiet = False)

#tabla general de las universidades(dataset)
st.write("*- A continuación se muestra la tabla general de las universidades con sus datos respectivos*")
download_data()
st.subheader("Tabla General")
data= pd.read_csv("data.csv",sep="|",  encoding= "latin_1")
data=data.set_index("CODIGO_ENTIDAD")
x= data.set_index("NOMBRE")
st.dataframe(data)

#seleccionador por tipo de gestion, ademas muestra una tabla por orden de gestion
st.write("""
	*- Seleccione “Privado” o “Público” para que así le muestre las universidades por su tipo de gestión, además de la información del estado de licenciamiento de la universidad*
	""")
esta= data["TIPO_GESTION"].unique()
licensi= data["ESTADO_LICENCIAMIENTO"].unique()
estado=st.selectbox("Gestion tipo:",("Publico","Privado"))


if estado== "Publico":
    public= data.loc[data.loc[:,"TIPO_GESTION"]=="PÚBLICO"]
    st.dataframe(data.loc[data.loc[:,"TIPO_GESTION"]=="PÚBLICO"])
elif estado== "Privado":
    public= data.loc[data.loc[:,"TIPO_GESTION"]=="PRIVADO"]
    st.dataframe(data.loc[data.loc[:,"TIPO_GESTION"]=="PRIVADO"])

#seleccionador para comparar el periodo de licenciamiento de diferentes universidades, así mismo muestra la información de la universidad seleccionada
st.write("""
	*- A continuación usted podrá comparar diferentes universidades por su “Periodo de licenciamiento”, además le mostrará solo la información de las universidades seleccionadas*
	""")
opti= st.multiselect(
    "Seleccione las universidades que desea comparar el periodo de licenciamiento:", 
    options= data["NOMBRE"].unique()
    )
para= x.loc[opti]
st.dataframe(para)
baraa= x.loc[opti,"PERIODO_LICENCIAMIENTO"]

st.bar_chart(baraa)
