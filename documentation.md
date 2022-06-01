## setup
For now, SQLAlchemy is only supported on the Python 3.9.0 installation on the RConnect Test server, so make sure you have a Python 3.9.0 installation with `rsconnect` also installed.

WARNING:
DO NOT RE-PUBLISH OR REMOVE APPS FROM SERVER BEFORE DOWNLOADING USER DATA. ALL USER DATA WILL BE LOST.


## mentor signup
1. Locate the app GUID for the mentor registration app under 'info' (only necessary if app currently exists on server)
2. Uncomment line 2 (`sign_up_mentee_mentor = 'Mentor'`) and comment out line 3 (`sign_up_mentee_mentor = 'Mentee'`) in `mentee_mentor_select.py`
3. Deploy the app. cd into the project folder and run:
`rsconnect deploy streamlit -n msk_rconnect_test --app-id GUID --python path-to-python.exe --entrypoint app_registration.py .`

## transition to mentee signup
1. Download the user data from mentor signup
2. Subset `tracks_mentees.csv` to only the Tracks selected during mentor signup

## mentee signup
1. Locate the app GUID for the mentee registration app under 'info' (only necessary if app currently exists on server)
2. Uncomment line 3 (`sign_up_mentee_mentor = 'Mentee'`) and comment out line 2 (`sign_up_mentee_mentor = 'Mentor'`) in `mentee_mentor_select.py`
3. Deploy the app. cd into the project folder and run:
`rsconnect deploy streamlit -n msk_rconnect_test --app-id GUID --python path-to-python.exe --entrypoint app_registration.py .`