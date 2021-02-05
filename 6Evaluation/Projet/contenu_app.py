
### IMPORT ###

from flask import Flask, render_template
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

import pymongo
from pymongo import MongoClient

### DEFINITION APP ###

app = Flask(__name__)

df_understat_L1 = pd.read_csv('Data_traitement/understatL1.csv', index_col=0)
df_cote_L1 = pd.read_csv('Data_traitement/coteL1.csv', index_col=0)

client = pymongo.MongoClient('127.0.0.1', 27017)
# client = pyMongo.MongoClient('mongo')
database = client['exercices']
collection_understatL1 = database['understatL1']
collection_coteL1 = database['coteL1']

##############
### GRAPHS ###
##############

# Compraison XG-XGA
def create_plot_1(df_understat_L1):
    trace1 = go.Bar(x = df_understat_L1['Team'], y = df_understat_L1['xG']/df_understat_L1['M'], name = 'xG')
    trace2 = go.Bar(x = df_understat_L1['Team'], y = df_understat_L1['xGA']/df_understat_L1['M'], name = 'xGA')
    layout = go.Layout(title = "Comparaison XG-XGA pour les équipes de Ligue 1 française" , xaxis = dict(title='Team'), yaxis = dict(title='xG/xGA'), title_x = 0.5)
    data = [trace1, trace2]
    fig = go.Figure(data = data, layout = layout)
    fig.write_image("static/images_plot/plot1.png")


# Comparaison XG-G
def create_plot_2(df_understat_L1):
    trace1 = go.Bar(x = df_understat_L1['Team'], y = (-df_understat_L1['xG-G']/df_understat_L1['M']), name = 'xG-G')
    layout = go.Layout(title = "Réussite de chaque équipe de Ligue 1 française sur les buts marqués par matchs", xaxis = dict(title='Team'), yaxis = dict(title='-(xG-G)/m'), title_x = 0.5)
    data = [trace1]
    fig = go.Figure(data = data, layout = layout)
    fig.write_image("static/images_plot/plot2.png")


# Comparaison XGA-GA
def create_plot_3(df_understat_L1):
    trace1 = go.Bar(x = df_understat_L1['Team'], y = df_understat_L1['xGA-GA']/df_understat_L1['M'], name = 'xGA-GA')
    layout = go.Layout(title = "Réussite de chaque équipe de Ligue 1 française sur les buts encaissés par matchs", xaxis = dict(title='Team'), yaxis = dict(title='(xGA-GA)/m'), title_x = 0.5)
    data = [trace1]
    fig = go.Figure(data = data, layout = layout)
    fig.write_image("static/images_plot/plot3.png")


# Comparaison XPTS-PTS
def create_plot_4(df_understat_L1):
    trace1 = go.Bar(x = df_understat_L1['Team'], y = (-df_understat_L1['xPTS-PTS'])/df_understat_L1['M'], name = 'xPTS-PTS')
    layout = go.Layout(title = "Réussite de chaque équipe de Ligue 1 française sur les points pris", xaxis = dict(title='Team'), yaxis = dict(title='-(xPTS-PTS)/m'), title_x = 0.5)
    data = [trace1]
    fig = go.Figure(data = data, layout = layout)
    fig.write_image("static/images_plot/plot4.png")


# Création graphque
create_plot_1(df_understat_L1)
create_plot_2(df_understat_L1)
create_plot_3(df_understat_L1)
create_plot_4(df_understat_L1)


## APP ROUTE : DESCRIPTION ##
@app.route('/')
def application():
    return render_template('template_description.html')


## APP ROUTE : GRAPH ##
@app.route('/graph')
def graph_page():
    return render_template('template_graph.html')


## APP ROUTE : CLASSEMENT ##
@app.route('/classement')
def classement_page():
    database = collection_understatL1.find()
    return render_template('template_classement.html', data = database)


## APP ROUTE : CALENDRIER ##
@app.route('/calendrier')
def calendrier_page():
    database2 = collection_coteL1.find()
    return render_template('template_calendrier.html', data2 = database2)


if __name__ == '__main__':
    app.run() 
