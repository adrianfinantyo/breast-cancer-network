#!/usr/bin/env python
# coding: utf-8

# # Diseases Mining from Pubtator Central

# ### Preqrequisites Libraries

# In[1]:


from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import calendar
import time


# ### Mining Config

# In[2]:


url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids={}"

pubs_df = pd.read_csv("./data/1676879038-pubs-breast-cancer-4860.csv")


# ### Functions

# In[3]:


logs_str = "Logs: {}"

def get_disease_from_pubs(row):
    print(logs_str.format("Getting disease from pub: {}".format(row['PMID'])))

    disease = np.array([])

    metadata_url = url.format(row['PMID'])
    metadata_response = requests.get(metadata_url)

    metadata_soup = BeautifulSoup(metadata_response.content, 'lxml')
    disease_sections = metadata_soup.find_all('infon', {'key': 'type'})
    for disease_section in disease_sections:
        if(disease_section.get_text().strip().lower() == 'disease'):
            text = disease_section.parent.find('text').get_text().strip()
            new_disease = np.array([row['PMID'], text])
            disease = np.append(disease, new_disease)

    print(logs_str.format("Found: {} diseases".format(disease.size)))

    return disease

def get_disease(df, limit=0):
    print(logs_str.format("🔨 Getting disease from {} publications".format(df.shape[0])))
    disease = np.array([])
    for index, row in df.iterrows():
        if(limit > 0 and index >= limit):
            break

        print(logs_str.format("Iteration number: {}".format(index)))
        
        try:
            new_disease = get_disease_from_pubs(row)
            disease = np.append(disease, new_disease)
        except Exception as e:
            print(logs_str.format("Error: {}".format(e)))
            continue
    
    print("-" * 50)
    print(logs_str.format("🌟 Job done!"))
    
    return disease

def transorm_to_df(dis, columns):
    df = pd.DataFrame(dis.reshape(-1, 2), columns=columns)
    return df


# ### Mining

# In[ ]:


diseases = get_disease(pubs_df)
diseases_df = transorm_to_df(diseases, ['PMID', 'Disease'])

diseases_df.dropna(inplace=True) # Remove NaN
diseases_df["Disease"] = diseases_df["Disease"].astype(str).str.lower() # Lowercase
diseases_df = diseases_df.drop_duplicates() # Remove duplicates

diseases_df.describe()


# ### Export Data to CSV

# In[ ]:


file_path = "./data/"
ts = calendar.timegm(time.gmtime())
num_dis = diseases_df.shape[0]
file_name = "{}-diseases-{}.csv".format(ts, num_dis)

diseases_df.to_csv(file_path+file_name, index=False)

