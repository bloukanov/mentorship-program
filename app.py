import streamlit as st
import sqlalchemy as db
import pandas as pd
import numpy as np
from db import User, Interest, Session


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

st_session = _get_full_session()

# st.write(session)
headers = st_session.ws.request.headers
# st.write(headers['Host'])
# USER OF CURRENT SESSION!!!
try:
    st_user = eval(headers["Rstudio-Connect-Credentials"])['user']
except:
    if headers['Host'] == 'localhost:8501':
        st_user = "LoukanoB localhost"
    else:
        st_user = 'unknown user'


# found how to find session user here:
# https://github.com/sapped/flip/blob/main/streamlit/user/user.py


def create_tables():
    import os

    prospective_mentors = pd.DataFrame({'username':[],'interest':[]})
    prospective_mentees = pd.DataFrame({'username':[],'interest':[],'rank':[]})

    if not os.path.isfile('prospective_mentors.csv'):
        prospective_mentors.to_csv('prospective_mentors.csv',index=False)

    if not os.path.isfile('prospective_mentees.csv'):
        prospective_mentees.to_csv('prospective_mentees.csv',index=False)

# create_tables()

interests_csv = pd.read_csv('interests.csv')
prospective_mentors = pd.read_csv('prospective_mentors.csv')
prospective_mentees = pd.read_csv('prospective_mentees.csv')

st.title('MSK Development Mentorship Program')


st.markdown('Welcome! You are logged in as __'+st_user+'__.')


# @st.cache
def convert_data():
    with Session.begin() as session:
        df = pd.read_sql('''
        select a.id as userid, a.username, a.mentor, b.interest, b.rank
        from users a
        left join interests b on a.id = b.userid
        ''',session.bind)
    return df.to_csv(index=False).encode('utf-8') 

if st_user in ['LoukanoB', 'LoukanoB localhost', 'AjayiO', 'UrickC']:
    csv = convert_data()
    # st.write('hey')
    st.download_button(
        label="Download user data",
        data=csv,
        file_name='interests.csv',
        mime='text/csv',
        )
    st.write('')
    st.write('')


# if len(prospective_mentors.username[prospective_mentors.username==user]) == 0 and len(prospective_mentees.username[prospective_mentees.username==user]) == 0:
if User.find_by_username(st_user) is None:
    st.write('Looks like this is your first time here. Would you like to sign up as a Mentee or a Mentor? Use the panel on the left to choose.')
    sign_up_mentee_mentor = st.sidebar.selectbox('Mentee or Mentor',['Select One','Mentee','Mentor'])

    if sign_up_mentee_mentor == 'Mentor':
        st.write('''Great! Choose the skills you would like to share and click Submit.
        ''')
        st.markdown('_Note: The more skills you add, the better your match is likely to be!_')

        with st.form('mentor registration'):
            mentor_interest_select = st.multiselect('Select one or more:',interests_csv.interest)
            mentor_submit = st.form_submit_button()
            if mentor_submit:
                try:
                    #write to data to db
                    user = User(st_user,mentor=True)
                    user.interests = [Interest(int,np.nan) for int in mentor_interest_select]
                    user.save_to_db()

                    st.success('Thanks for signing up to be a mentor! Refresh the page or check back later to view or update your selections.')
                except:
                    st.error('''There was an error saving your data. Please try again, and if this persists contact WFAF at
                    DEVWFAF@mskcc.org.
                ''')

    elif sign_up_mentee_mentor == 'Mentee':
        # st.write('Under construction!')
        st.markdown('''Great! Please select the skills you would like to learn, __in order of preference from left to right__,
        and click Submit.
        ''')
        st.markdown('_Note: The more skills you add, the better your match is likely to be!_')

        # with st.form('mentee registration'):
        mentee_interest_select = st.multiselect('Select one or more:',interests_csv.interest)
        enum = list(enumerate(mentee_interest_select))
        ranks = [x[0]+1 for x in enum]
        ints = [x[1] for x in enum]
        st.write('  \n'.join([str(x[0]+1)+': '+x[1] for x in enum]))
        # mentee_submit = st.form_submit_button()
        if st.button('Submit'):
            try:
                # add data to file
                user = User(st_user,mentor=False)
                user.interests = [Interest(ints[i],ranks[i]) for i in range(len(enum))]
                user.save_to_db()
                st.success('Thanks for signing up to be a mentee! Refresh the page or check back later to view or update your selections.')
            except:
                st.error('''There was an error saving your data. Please try again, and if this persists contact WFAF at
                DEVWFAF@mskcc.org.
                ''')

else:
    if User.is_mentor(st_user):
        st.markdown('Nice to see you again. You have registered as a __Mentor__. The interests you selected are:')
        ints = Interest.find_by_username(st_user)
        # x0 is Interest object, X1 is rank, and X2 is interest
        st.write('  \n'.join([x[2] for x in ints]))
            
    else:
        st.markdown('Nice to see you again. You have registered as a __Mentee__. The interests you selected are:')
        ints = Interest.find_by_username(st_user)
        # x0 is Interest object, X1 is rank, and X2 is interest
        st.write('  \n'.join([str(x[1]) + ': ' + x[2] for x in ints]))
    
    st.write('')
    st.write('')
    st.write('''To change your preferences, simply Delete your current profile 
    and refresh the page to create a new one.
    ''')
    if st.button('Delete Profile'):
        try:
            # user = User(st_user,User.is_mentor(st_user))
            # user.delete_from_db()
            with Session.begin() as session:
                session.query(Interest).filter(Interest.user.has(username=st_user)).delete(synchronize_session=False)
                session.query(User).filter_by(username=st_user).delete(synchronize_session=False)
                st.warning('Profile successfully deleted. Please refresh the page to create a new one.')
        except:
            st.error('''There was an error deleting your profile. Please try again, and if this persists contact WFAF at
            DEVWFAF@mskcc.org.
            ''')

# c1 = Customers(name = 'Ravi Kumar', address = 'Station Road Nanded', email = 'ravi@gmail.com')


