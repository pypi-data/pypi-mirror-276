import streamlit as st
import plotly.express as px


from besser.bot.db.monitoring_db import MonitoringDB, TABLE_INTENT_PREDICTION, TABLE_SESSION


def home(monitoring_db: MonitoringDB):
    st.header('Home')
    bot_names = bot_filter(monitoring_db)
    col1, col2 = st.columns(2)
    with col1:
        intent_histogram(monitoring_db, bot_names)
    with col2:
        get_matched_intents_ratio(monitoring_db, bot_names)


def bot_filter(monitoring_db: MonitoringDB):
    bots = monitoring_db.get_table(TABLE_SESSION)['bot_name'].unique()
    bot_names = st.multiselect(label='Select one or more bots', options=bots, placeholder='All bots')
    return bot_names


def get_matched_intents_ratio(monitoring_db: MonitoringDB, bot_names=[]):
    table_intent_prediction = monitoring_db.get_table(TABLE_INTENT_PREDICTION)
    if bot_names:
        table_session = monitoring_db.get_table(TABLE_SESSION)
        # Filter the tables by the specified bots
        table_session = table_session[table_session['bot_name'].isin(bot_names)]
        table_intent_prediction = table_intent_prediction[table_intent_prediction['session_id'].isin(table_session['id'])]
    value_counts = table_intent_prediction['intent'].value_counts()
    fallback_count = value_counts['fallback_intent'] if 'fallback_intent' in value_counts else 0
    intent_matched_count = len(table_intent_prediction) - fallback_count
    data = {'names': ['Matched', 'Fallback'], 'values': [intent_matched_count, fallback_count]}
    fig = px.pie(data, values='values', names='names',
                 #color_discrete_sequence=['blue', 'red'],
                 hole=0.5,
                 title='Matched intents ratio')
    st.plotly_chart(fig, use_container_width=True)


def intent_histogram(monitoring_db: MonitoringDB, bot_names=[]):
    table_intent_prediction = monitoring_db.get_table(TABLE_INTENT_PREDICTION)
    if bot_names:
        table_session = monitoring_db.get_table(TABLE_SESSION)
        # Filter the tables by the specified bots
        table_session = table_session[table_session['bot_name'].isin(bot_names)]
        table_intent_prediction = table_intent_prediction[table_intent_prediction['session_id'].isin(table_session['id'])]
    fig = px.histogram(table_intent_prediction, x='intent', color='intent', title='Histogram of Intents')
    st.plotly_chart(fig, use_container_width=True)
