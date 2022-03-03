import streamlit as st
from streamlit.server.server import Server
import streamlit as st
# import sqlalchemy as db
# from sqlalchemy import Table, Column, Integer, String, MetaData
import pandas as pd


try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    try:
    # After Streamlit 0.65
        from streamlit.report_thread import get_report_ctx
        from streamlit.server.server import Server
    except: 
    # After ~1.3
        from streamlit.script_run_context import get_script_run_ctx as get_report_ctx
        from streamlit.server.server import Server

def _get_full_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    # MODIFIED ORIGINAL _get_session CODE SO WE CAN ACCESS HEADERS FOR USER
    # return session_info.session
    return session_info

session = _get_full_session()

# st.write(session)
headers = session.ws.request.headers
# USER OF CURRENT SESSION!!!
try:
    user = eval(headers["Rstudio-Connect-Credentials"])['user']
except:
    user = 'you'
# st.write(user)


# engine = db.create_engine('sqlite:///data.sqlite',echo = True)
# connection = engine.connect()

# meta = MetaData()

# students = Table(
#    'students', meta, 
#    Column('id', Integer, primary_key = True), 
#    Column('name', String), 
#    Column('lastname', String), 
# )

def create_tables():
    import os

    prospective_mentors = pd.DataFrame({'username':[],'interest':[]})
    prospective_mentees = pd.DataFrame({'username':[],'interest':[],'rank':[]})

    if not os.path.isfile('prospective_mentors.csv'):
        prospective_mentors.to_csv('prospective_mentors.csv',index=False)

    if not os.path.isfile('prospective_mentees.csv'):
        prospective_mentees.to_csv('prospective_mentees.csv',index=False)

# create_tables()

interests = pd.read_csv('interests.csv')
prospective_mentors = pd.read_csv('prospective_mentors.csv')
prospective_mentees = pd.read_csv('prospective_mentees.csv')

st.title('MSK Development Mentor Program')


st.markdown('Welcome! You are logged in as __'+user+'__.')



if len(prospective_mentors.username[prospective_mentors.username==user]) == 0 and len(prospective_mentees.username[prospective_mentees.username==user]) == 0:
    st.write('Looks like this is your first time here. Would you like to sign up as a Mentee or a Mentor? Use the panel on the left to choose.')
    sign_up_mentee_mentor = st.sidebar.selectbox('Mentee or Mentor',['Select One','Mentee','Mentor'])

    if sign_up_mentee_mentor == 'Mentor':
        mentor_interest_select = st.multiselect('Please select the skills you would like to share:',interests.interest)

    elif sign_up_mentee_mentor == 'Mentee':
        st.write('Under construction!')




# st.write('Please select your interests ')

# st.text_input('')


# st.