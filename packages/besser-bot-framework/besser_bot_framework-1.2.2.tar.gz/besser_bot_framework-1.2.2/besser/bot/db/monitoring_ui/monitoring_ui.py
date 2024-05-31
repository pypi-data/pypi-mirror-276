import sys

import streamlit as st
from streamlit.web import cli as stcli

from besser.bot.db.monitoring_ui.db_connection import connect_to_db, close_connection
from besser.bot.db.monitoring_ui.home import home
from besser.bot.db.monitoring_db import MonitoringDB
from besser.bot.db.monitoring_ui.sidebar import sidebar_menu
from besser.bot.db.monitoring_ui.table_overview import table_overview
from besser.bot.db.monitoring_ui.flow_graph import flow_graph

st.set_page_config(layout="wide")

if __name__ == "__main__":
    if st.runtime.exists():
        if 'monitoring_db' not in st.session_state:
            st.session_state['monitoring_db'] = connect_to_db()
        with st.sidebar:
            page = sidebar_menu()
            if st.button('Reconnect'):
                close_connection(st.session_state['monitoring_db'])
                st.session_state['monitoring_db'] = connect_to_db()
        monitoring_db: MonitoringDB = st.session_state['monitoring_db']
        if page == 'Home':
            home(monitoring_db)
        elif page == 'Flow Graph':
            flow_graph(monitoring_db)
        elif page == 'Table Overview':
            table_overview(monitoring_db)
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
