from typing import final
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# import squarify

st.set_page_config(layout="wide")
st.write("# BIODIVERSITY IN US NATIONAL PARKS")
st.write("Presented by : **_Naveen kumar &_** **_Chetna Jayakumar_**.")
st.write("##### CONTEXT:")
st.write('The National Park Service publishes a database of animal and plant species identified in individual national parks and verified by evidence such as observations, vouchers and reports that document the presence of a species in the parks.')
st.write('##### GOAL:')
st.write('To increase the survival rate and save the lives of endangered and threatened species')

species = pd.read_csv('species.csv',dtype='str')
# Removal of rows that has Null values
species = species[~species['Order'].isnull()]
species = species[~species['Family'].isnull()]
species = species[~species['Occurrence'].isnull()]
species = species[~species['Nativeness'].isnull()]
species = species[~species['Abundance'].isnull()]
species.replace(r'', np.NaN)

parks = pd.read_csv('parks.csv', dtype={'Park Name': 'str', 'State': 'str', 'Acres': 'int'})
parks.replace(r'',np.NaN)
# creating new fields
parks["Region"]=np.nan
parks.rename(columns={'State':'State_code'},inplace=True)
parks["State"] = np.nan

parks["Region"]= np.where((parks["State_code"]=="SD")| (parks["State_code"]=="OH") | (parks["State_code"]=="MI") | (parks["State_code"]=="ND") | (parks["State_code"]=="MN"), "MidWest", parks["Region"])
parks["Region"]= np.where((parks["Region"]=="nan") & ((parks["State_code"]=="ME")), "Northeast", parks["Region"])
parks["Region"]= np.where((parks["Region"]=="nan") & ((parks["State_code"]=="TX")| (parks["State_code"]=="FL") | (parks["State_code"]=="SC")| (parks["State_code"]=="TN, NC") | (parks["State_code"]=="AR")| (parks["State_code"]=="KY")| (parks["State_code"]=="VA")), "South", parks["Region"])
parks["Region"]= np.where((parks["Region"]=="nan") & ((parks["State_code"]=="UT")| (parks["State_code"]=="CO") | (parks["State_code"]=="NM")| (parks["State_code"]=="CA") | (parks["State_code"]=="OR")| (parks["State_code"]=="AK")| (parks["State_code"]=="CA, NV")| (parks["State_code"]=="MT")| (parks["State_code"]=="NV")| (parks["State_code"]=="AZ")| (parks["State_code"]=="WY")| (parks["State_code"]=="HI")| (parks["State_code"]=="WA")| (parks["State_code"]=="WY, MT, ID")), "West",parks["Region"])

parks["State"] = np.where(parks["State_code"]=="ME", "Maine", parks["State"])
parks["State"] = np.where(parks["State_code"]=="UT", "Utah", parks["State"])
parks["State"] = np.where(parks["State_code"]=="SD", "South Dakota", parks["State"])
parks["State"] = np.where(parks["State_code"]=="TX", "Texas", parks["State"])
parks["State"] = np.where(parks["State_code"]=="FL", "Florida", parks["State"])
parks["State"] = np.where(parks["State_code"]=="CO", "Colorado", parks["State"])
parks["State"] = np.where(parks["State_code"]=="NM", "New Mexico", parks["State"])
parks["State"] = np.where(parks["State_code"]=="CA", "California", parks["State"])
parks["State"] = np.where(parks["State_code"]=="SC", "South Carolina", parks["State"])
parks["State"] = np.where(parks["State_code"]=="OR", "Oregon", parks["State"])
parks["State"] = np.where(parks["State_code"]=="OH", "Ohio", parks["State"])
parks["State"] = np.where(parks["State_code"]=="AK", "Alaska", parks["State"])
parks["State"] = np.where(parks["State_code"]=="CA, NV", "California/Nevada", parks["State"])
parks["State"] = np.where(parks["State_code"]=="MT", "Montana", parks["State"])
parks["State"] = np.where(parks["State_code"]=="NV", "Nevada", parks["State"])
parks["State"] = np.where(parks["State_code"]=="AZ", "Arizona", parks["State"])
parks["State"] = np.where(parks["State_code"]=="TN, NC", "Tennessee/North Carolina", parks["State"])
parks["State"] = np.where(parks["State_code"]=="WY", "Wyoming", parks["State"])
parks["State"] = np.where(parks["State_code"]=="HI", "Hawaii", parks["State"])
parks["State"] = np.where(parks["State_code"]=="AR", "Arkansas", parks["State"])
parks["State"] = np.where(parks["State_code"]=="MI", "Michigan", parks["State"])
parks["State"] = np.where(parks["State_code"]=="KY", "Kentucky", parks["State"])
parks["State"] = np.where(parks["State_code"]=="WA", "Washington", parks["State"])
parks["State"] = np.where(parks["State_code"]=="VA", "Virginia", parks["State"])
parks["State"] = np.where(parks["State_code"]=="ND", "North Dakota", parks["State"])
parks["State"] = np.where(parks["State_code"]=="MN", "Minnesota", parks["State"])
parks["State"] = np.where(parks["State_code"]=="WY, MT, ID", "Wyoming, Montana,Idaho", parks["State"])

del species['Unnamed: 13']
final_df = pd.merge(left=parks, right=species, how='right')

native_df = pd.DataFrame(final_df[final_df["Nativeness"]=="Native"].groupby(["Region","Category","Nativeness","Occurrence","Abundance"]).size(),columns=["Count"])
native_df.reset_index(inplace=True)

nativebirds_df = pd.DataFrame(final_df[final_df["Category"] =="Bird"].groupby(["Region","Category","Nativeness","Latitude","Longitude","Conservation Status"]).size(),columns=["Count"])
nativebirds_df.reset_index(inplace=True)

birds = pd.DataFrame(final_df[final_df["Conservation Status"] =="Species of Concern"].groupby(["Region","Category","Nativeness","Latitude","Longitude"]).size(),columns=["Count"])
birds.reset_index(inplace=True)

mammals = pd.DataFrame(final_df[final_df["Category"] =="Mammal"].groupby(["Abundance","Region","Category","Nativeness","Latitude","Longitude","Conservation Status"]).size(),columns=["Count"])
mammals.reset_index(inplace=True)

aggregation = species.groupby(['Park Name']).count()
conserve_species = species[~species['Conservation Status'].isnull()]

##Scatter Mapbox Plot
st.write("### Area covered by each Park on map ")
st.write('The plot depicts the area covered by each park with respect to their coordinates to accomodate the species on the earth.')
fig4 = px.scatter_mapbox(parks,lat ="Latitude", lon ="Longitude",color="Acres",hover_name = "Park Name", size="Acres", width=1000, height=700,zoom=2)
fig4.update_layout(mapbox_style="open-street-map")
st.write(fig4)

##Scatter_Bubble Chart
st.write("### Largest Park in Regions on coordinates of Earth")
st.write('This chart helps in finding the region which has the largest park which is region specific.')
fig2 = px.scatter(final_df,x="Latitude",y="Longitude",color="Region",hover_name="Acres", size="Acres",log_x=True, width=1000, height=500)
st.write(fig2)

# st.write("### Area occupied by each State in US")
# st.write('This map shows the area occupied by each state in US.')
# fig11 = px.treemap(parks, path=["Region","State"], values="Acres",
# color='Acres', hover_data=['Park Name'],color_continuous_scale='RdBu',width=1000, height=500)
# # color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop'])
# st.write(fig11)




##Scatter Plot
st.write("### National Parks in each State")
st.write('The plot illustrates the all the National parks in and around the states of US.')
fig1 = px.scatter(parks,x="Park Name",y="State", color='Acres', width=1000, height=800)
st.write(fig1)

##Bar Chart
st.write("### Overview on Family of species")
st.write('This Chart Shows the count on the overview of all the species in the parks.')
a=species["Category"].unique()
b=species["Category"].value_counts()
fig6 = px.bar(species,x=a, y=b,labels={"x":"Category", "y":"count"},width=1000, height=500)
st.write(fig6)

st.write("### Species in each National park  in US")
st.write('This map shows the Species in each National park  in US.')
fig11 = px.treemap(final_df, path=["Park Name","Category"], values="Acres",
color='Acres', hover_data=['Park Name'],color_continuous_scale='RdBu',width=1000, height=500)
# color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop'])
st.write(fig11)

## Donut Chart
st.write("### Mammals and their abundance")
st.write('The mammals and their percentage of abundance is shown in this donut chart.')
f1=go.Figure(data=[go.Pie(labels=mammals["Abundance"], values=mammals["Count"], hole=.4)])
st.write(f1)

##Bar Chart
st.write("### Nativity and Protectivity status of Mammals ")
st.write('As per the information that the chart shows, the native mammals tend to be the species of concern and endangered species.')
fig10 = px.bar(mammals, x="Count", y="Conservation Status", color ="Nativeness", width=1000, height=600,orientation="h")
st.write(fig10)

##Stacked Bar Chart
st.write("### Family of species based on conservation status ")
st.write('This chart shows the reason for the goal which explains the conservation status wrt the species.')
fig7 = px.histogram(conserve_species,x="Category",color="Conservation Status",width=1000, height=500)
st.write(fig7)


##Density Mapbox Plot
st.write('### Species of concern-Birds based on Region ')
st.write('The most important species of concern among the other species is found as Birds.So to find the native places and immigrant birds this charts is helpful and important.')
fig8 = px.density_mapbox(birds, lat='Latitude', lon='Longitude', z='Count', radius=10, center=dict(lat=0, lon=180), zoom=0,mapbox_style="stamen-terrain",width=1000, height=500)
st.write(fig8)

##Box Plot
st.write("### Native Birds & their Origin")
st.write('Also we are discovering the origin of the Birds based on the sub-regions in the country.')
fig9 = px.box(nativebirds_df,x="Conservation Status", y="Count", color="Region",width=1200,height=500)
fig9.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
st.write(fig9)

##Sunburst Plot
st.write("### Categorization on Native species with their species category & abundance ")
st.write('The overall view species and their abundance on all the regions is clearly illustrated using the below chart.')
fig5 = px.sunburst(native_df, path=['Region','Category','Abundance'], values='Count',width=800, height=700)
st.write(fig5)

# #Treemap
# pic = px.treemap(names=final_df['Park Name'],parents=final_df['Category'])
# pic.update_traces(root_color="red")
# pic.update_layout(margin = dict(t=50, l=25, r=25, b=25))
# st.write(pic)




st.write("##### CONCLUSION:")
st.write('The northern part of the continent needs more attention and especially for the Birds and Mammals. As a solution they can follow the way the southern part of the continent does to protect the wild life.')


