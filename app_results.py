import streamlit as st
import pandas as pd
import numpy as np
import os


#### GET USER
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
    if headers['Host'][:9] == 'localhost':
        st_user = "LoukanoB"
        # st_user = 'urickc'
    else:
        # st_user = 'unknown user'
        # st_user = 'LoukanoB'
        st.error('The user of this session is unknown. Please contact the developer.')


matches = pd.read_csv('cwg_test2_results_round1.csv')

# this is a simple conacat of mentee and mentor raw output from registration site
registration_data = pd.read_csv('registration_data.csv')

# @st.cache
# def convert_data(df):
#     return df.to_csv(index=False).encode('utf-8') 

# # DOWNLOAD DATA BUTTON
# if st_user.lower() in ['loukanob', 'urickc']:
#     csv = convert_data(registration_data)
#     st.write('')
#     st.write('')
#     st.download_button(
#         label="Download user data",
#         data=csv,
#         file_name='results_round1.csv',
#         mime='text/csv',
#         )
#     st.write('')
#     st.write('')

if 'round_accept' not in registration_data.columns:
    registration_data['round_accept'] = np.nan

if 'round_reject_reason' not in registration_data.columns:
    registration_data['round_reject_reason'] = np.nan

st.title('MSK Development Mentorship Program')
# st.subheader('Results')

# only grant access to people who signed up
st.markdown("Welcome back! You are logged in as __{}__. Your match is below.".format(st_user))

mentee_mentor_list = ['Mentee','Mentor']
user_profile = registration_data[registration_data.username == st_user].iloc[0]
mentee_mentor = mentee_mentor_list[int(user_profile.mentor)]

# if user_profile.mentor == 0:
st.info('At the bottom of this page, please select whether you accept this pairing or not.')


col1, col2 = st.columns(2)


with col1:
    st.markdown('''## You ({})'''.format(mentee_mentor.lower()))
    # st.write(mentee_mentor)
    user_ints = registration_data.loc[registration_data.username == st_user,['rank','interest']]

    # st.markdown('__{}__'.format(mentee_mentor))

    st.subheader('Profile')
    # st.write(pd.isna(user_profile.pronouns))
    st.markdown(f'''__{user_profile.fullname.upper()}{' ('+user_profile.pronouns.lower()+')' if not pd.isna(user_profile.pronouns) else ''}__  
    __City, State__: {user_profile.city}  
    __Job Title__: {user_profile.job}  
    __Years of experience in role at MSK__: {user_profile.years_msk}  
    __Total years of experience in role__: {user_profile.years_all}
    '''
    )
    st.markdown("__Team__: "+user_profile.team)

    st.subheader('Tracks')

    # st.write(User.is_mentor(st_user))

    if user_profile.mentor==1:
        st.write('  \n'.join(user_ints['interest']))
            
    else:
        st.write('  \n'.join([str(int(user_ints.iloc[n,0])) + ': ' + user_ints.iloc[n,1] for n in range(user_ints.shape[0])]))


with col2:
    not_mentee_mentor = mentee_mentor_list[1-int(user_profile.mentor)]

    st.markdown('## Your match ({})'.format(not_mentee_mentor.lower()))

    match_username = matches.loc[matches[mentee_mentor.lower()]==st_user,not_mentee_mentor.lower()].values[0]

    match_profile = registration_data[registration_data.username == match_username].iloc[0]
    match_ints = registration_data.loc[registration_data.username == match_username,['rank','interest']]

    # st.markdown('__{}__'.format(not_mentee_mentor))

    st.subheader('Profile')
    st.markdown(f'''__{match_profile.fullname.upper()} ({match_profile.pronouns.lower()})__  
    __City, State__: {match_profile.city}  
    __Job Title__: {match_profile.job}  
    __Years of experience in role at MSK__: {match_profile.years_msk}  
    __Total years of experience in role__: {match_profile.years_all}
    '''
    )
    st.markdown("__Team__: "+match_profile.team)

    st.subheader('Tracks')

    # st.write(User.is_mentor(st_user))

    if match_profile.mentor==1:
        st.write('  \n'.join(match_ints['interest']))
            
    else:
        st.write('  \n'.join([str(int(match_ints.iloc[n,0])) + ': ' + match_ints.iloc[n,1] for n in range(match_ints.shape[0])]))



# if user_profile.mentor == 0:
st.markdown('## Your decision')
st.markdown('''Do you accept this pairing? If you select No, we will attempt one more matching
round, but __there is no guarantee that you will be matched with anyone else__. If you select No now,
you risk not participating in the pilot program.
''')

# col3, col4, col5, col6, col7, col7 = st.columns(6)

st.write('''
You may also return to the [registration site](https://tlvistishny1.mskcc.org/mentee-registration-test/) to change your profile and 
match preferences, or to remove yourself from the program.
 ''')

with st.form('decision'):
    decision = st.radio('Accept this pairing?', ('Yes, I accept my pairing', 'No, I do not accept my pairing, and I understand the risks'))
    rejection_reason = st.text_input('If you choose not to accept, can you please explain why?')
    
    if st.form_submit_button():

        if decision == 'Yes, I accept my pairing':
            try:
                registration_data.loc[registration_data.username == st_user,'round_accept'] = 1
                registration_data.to_csv('registration_data.csv',index=False)   

                st.success('''Thank you, your response has been recorded. Keep an eye on your inbox for next steps. 
                We hope you enjoy your mentorship!''')

            except:
                st.error('''There was an error saving your response. Please try again, and if this persists contact WFAF at
                DEVWFAF@mskcc.org.
                ''')

        if decision == 'No, I do not accept my pairing, and I understand the risks':
            if rejection_reason == '':
                st.error('Please explain why you are not accepting this pairing.')
            else:
                try:
                    registration_data.loc[registration_data.username == st_user,'round_accept'] = 0
                    registration_data.loc[registration_data.username == st_user,'round_reject_reason'] = rejection_reason
                    registration_data.to_csv('registration_data.csv',index=False)

                    st.warning('''
                    Thank you, your response has been recorded. Please keep an eye on your inbox, and 
                    we will let you know if you are matched with someone else.
                    ''')
                except:
                    st.error('''There was an error saving your response. Please try again, and if this persists contact WFAF at
                    DEVWFAF@mskcc.org.
                    ''')


