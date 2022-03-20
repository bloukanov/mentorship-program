import streamlit as st


track_info = '''
__Skill Based__   
Soft skills for the workplace
  
__Self-Care + Support__  
Self-care  
  
__Peer Mentorship__  
Would you like to be matched with someone with a similar job function to you? 

'''

teams = ['Select One','Development Information Strategy and Operations','Development Programs','Finance','Individual and Institutional Giving']


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
    if headers['Host'] == 'localhost:8501':
        st_user = "LoukanoB"
    else:
        st_user = 'unknown user'
