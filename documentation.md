## setup
For now, SQLAlchemy is only supported on the Python 3.9.0 installation on the RConnect Test server, so make sure you have a Python 3.9.0 installation with `rsconnect` also installed.

WARNING:
DO NOT RE-PUBLISH OR REMOVE APPS FROM SERVER BEFORE DOWNLOADING USER DATA. ALL USER DATA WILL BE LOST.


## mentor signup
1. Locate the app GUID for the mentor registration app under 'info' (only necessary if app currently exists on server)
2. Uncomment line 2 (`sign_up_mentee_mentor = 'Mentor'`) and comment out line 3 (`sign_up_mentee_mentor = 'Mentee'`) in `mentee_mentor_select.py`
3. Deploy the app. cd into the project folder and run:
`rsconnect deploy streamlit -n msk_rconnect_test --app-id GUID --python path-to-python.exe --entrypoint app_registration.py .`
4. Set access permissions to 'All users - login required'
5. Customize app name (Info tab) and url (Access tab) to 'mentor-registration' if this is first deployment

## transition to mentee signup
1. Download user data from the mentor signup
2. Restrict access of mentor app to 'Specific users or groups' and do not add any users/groups.
3. Subset `tracks_mentees.csv` to only the Tracks selected during mentor signup

## mentee signup
1. Locate the app GUID for the mentee registration app under 'info' (only necessary if app currently exists on server)
2. Uncomment line 3 (`sign_up_mentee_mentor = 'Mentee'`) and comment out line 2 (`sign_up_mentee_mentor = 'Mentor'`) in `mentee_mentor_select.py`
3. Deploy the app. cd into the project folder and run. If there is not already a version on the server, add the --new tag to not overwrite the mentor app.
`rsconnect deploy streamlit -n msk_rconnect_test --app-id GUID --python path-to-python.exe --entrypoint app_registration.py .`
4. Set access permissions to 'All users - login required'
5. Customize app name (Info tab) and url (Access tab) to 'mentee-registration' if this is first deployment