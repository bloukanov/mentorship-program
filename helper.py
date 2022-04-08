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


def form_callback(_fullname,_job):
    if _fullname == '' or _job == '':
        st.error('Please fill in all required fields')
        return False