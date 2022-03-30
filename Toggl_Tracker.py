# %%
#This code is to automate the generation of CSV from the Toggl time tracking tool in order to populate a 
#Power Bi dataset for the purposes of reporting and invoicing easily using the Toggl API. 

# %%
#Importing necessary python libraries
import requests
import pandas as pd
import base64
import os
from datetime import datetime
import json

# %%
#toggl api token
toggl_api_token = 'XXX'
string = toggl_api_token + ':api_token'
#conversion to base64 encoding and classification of bse64 as headers variable 
headers = {
    'Authorization': 'Basic ' + base64.b64encode(string.encode('ascii')).decode("utf-8")}

#url for authorisation
auth_url = 'https://api.track.toggl.com/api/v8/me'

#calling authorisation endpoint and response as a json
auth_resp = requests.get(auth_url, headers=headers)
auth_resp_json = json.loads(auth_resp.text)
auth_resp_json

# %%
#time entries url
time_entries_url = 'https://api.track.toggl.com/reports/api/v2/details?'

#request parameters
user_agent = auth_resp_json['data']['email']
workspaces_list = auth_resp_json['data']['workspaces']
workspaces_dict = workspaces_list[0]
workspace_id = workspaces_dict['id']
user_agent_param = 'user_agent='+user_agent
workspace_id_param = 'workspace_id='+str(workspace_id)
since = datetime.strptime('Sun, 01 Aug 2021 12:14:05', '%a, %d %b %Y %H:%M:%S')
since_iso = since.isoformat()
since_param = 'since='+since_iso

#request for first page of data
page_param1 = 'page=1'
combined_params1 = workspace_id_param+'&'+since_param+'&'+user_agent_param
time_entries_page1 = requests.get(time_entries_url,headers=headers, params = combined_params1)
time_entries_data_page1 = time_entries_page1.json()
time_entries_data_page1

# %%
#request for second page of data
page_param2 = 'page=2'
combined_params2 = workspace_id_param+'&'+since_param+'&'+user_agent_param+'&'+page_param2
time_entries_page2 = requests.get(time_entries_url,headers=headers, params = combined_params2)
time_entries_data_page2 = time_entries_page2.json()
time_entries_data_page2

# %%
#converting returned data to pandas dataframe
data_page1 = time_entries_data_page1['data']
df_page1 = pd.DataFrame(data_page1)
data_page2 = time_entries_data_page2['data']
df_page2 = pd.DataFrame(data_page2)

#dropping un-used columns
df_page1 = df_page1.drop(columns=['use_stop', 'task', 'billable', 'is_billable', 'cur', 'tags','project_color'])
df_page2 = df_page2.drop(columns=['use_stop', 'task', 'billable', 'is_billable', 'cur', 'tags','project_color'])


# %%
#appending pages into a single dataframe
data = df_page1.append(df_page2, ignore_index=True)
data

# %%
#pandas dataframe to csv file
csv = data.to_csv(r'C:\Users\markr\Documents\Portfolio\Toggl Tracker\output.csv')

# %%



