
# coding: utf-8

# In[137]:


from matplotlib import pyplot as plt
import pandas as pd
from scipy.stats import chi2_contingency


# In[2]:


species = pd.read_csv('species_info.csv')


# In[13]:


print species.head()


# In[161]:


print species.scientific_name.nunique()


# In[14]:


print species.category.unique()


# In[8]:


print species.conservation_status.unique()


# In[19]:


print species.groupby(species.conservation_status).scientific_name.nunique().reset_index()


# In[17]:


species.fillna('No Intervention', inplace=True)


# In[20]:


print species.groupby(species.conservation_status).scientific_name.nunique().reset_index()


# In[21]:


protection_counts = species.groupby('conservation_status')    .scientific_name.count().reset_index()    .sort_values(by='scientific_name')


# In[22]:


print protection_counts.head()


# In[27]:


ax = plt.subplot()


# In[140]:


plt.figure(figsize = (10,4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)),protection_counts.scientific_name, color = '#ff8c00')
ax.set_xticks(range(len(protection_counts)))
status = protection_counts['conservation_status'].tolist()
ax.set_xticklabels(status)            
plt.ylabel("Number of Species")
plt.title("Conservation Status by Species")
plt.show()


# In[95]:


species['is_protected'] = species.conservation_status.apply (lambda x: True if x != 'No Intervention' else False)


# In[104]:


category_counts = species.groupby(['category','is_protected']).scientific_name.count().reset_index()
print category_counts


# In[107]:


category_pivot = category_counts.pivot(columns = 'is_protected', index = 'category', values = 'scientific_name').reset_index()
print category_pivot


# In[116]:


category_pivot.columns = (['category','not_protected','protected'])
print category_pivot


# In[119]:


category_pivot['percent_protected'] = category_pivot.apply(lambda row: float(row['protected'])/ (float(row['protected']) + float(row['not_protected'])), axis = 1)
print category_pivot


# In[143]:


contingency_nearly_MB = category_pivot[(category_pivot['category'] == 'Mammal') | (category_pivot['category'] == 'Bird')]
contingency_MB = contingency_nearly_MB.iloc[:,1:3]
contingency_MB.index = ['Bird','Mammal']
print contingency_MB


# In[139]:


chi2, pval, dof, expected = chi2_contingency(contingency_MB)
print pval


# In[144]:


contingency_nearly_MR = category_pivot[(category_pivot['category'] == 'Reptile') | (category_pivot['category'] == 'Mammal')]
contingency_MR = contingency_nearly_MR.iloc[:,1:3]
contingency_MR.index = ['Mammal','Reptile']
print contingency_MR


# In[145]:


chi2, pval, dof, expected = chi2_contingency(contingency_MR)
print pval


# So mammals are more likely to be endangered than reptiles

# In[146]:


observations = pd.read_csv('observations.csv')
print observations.head()


# In[149]:


species['is_sheep'] = species.common_names.apply(lambda x : True if 'Sheep' in x else False)


# In[153]:


sheep_species = species[(species['is_sheep'] == True) & (species['category'] == 'Mammal')]
print sheep_species


# In[155]:


sheep_observations = pd.merge(sheep_species, observations, how = 'inner')
print sheep_observations


# In[156]:


obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
print obs_by_park


# In[159]:


plt.figure(figsize=(16,4))
ax = plt.subplot()
parks = obs_by_park['park_name'].tolist()
plt.bar(range(len(parks)),obs_by_park.observations, color = ['#ad4913','#8da7c6','#e2ca0f','#777371'])
ax.set_xticks(range(len(parks)))
ax.set_xticklabels(parks)
plt.ylabel("Number of Observations")
plt.title("Observations of Sheep per Week")
plt.show()


# Sample size needs to be 520.
# 
# Three weeks at Bryce technically 2 weeks and 14 hours (rounded)
# One week at Yellowstone
