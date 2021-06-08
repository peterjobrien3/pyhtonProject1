# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
print("Hello")

# Install Pandas, Numpy and Matplotlib and pyjstat, DID NOT INSTALL REQUESTS FOR API
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from pyjstat import pyjstat

# Assign URL to variable: url
url = 'https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/E2049/JSON-stat/2.0/en'
# Get the dataset using pyjstat
census_dataset=pyjstat.Dataset.read(url)
# Write the dataset to a dataframe and print it.
census_df=census_dataset.write('dataframe')
print(census_df)
# print the head of the dataframe
print(census_df.head())
# View the shape of the dataframe
print(census_df.shape)
# View the information on the dataframe
print(census_df.info())
# Check the columns for any missing data
print(census_df.isna().any())
# Subset for 2016 census data only
census_2016=census_df[census_df["CensusYear"].isin(["2016"])]
print(census_2016)
# Set the index of census_2016 to County
census_2016_co=census_2016.set_index("County")
print(census_2016_co.head())
# Save as a csv and check for non applicable rows.
census_2016_co.to_csv("census2016_co.csv")
print(census_2016_co.shape)
# Delete "State" in col. "County" (Index Column use .drop,
census_2016_co=census_2016_co.drop(labels="State", axis=0)
print(census_2016_co.shape)
# Delete "Both sexes" in col. "Sex", use.loc
census_2016_co=census_2016_co.loc[census_2016_co["Sex"]!="Both sexes"]
print(census_2016_co.shape)
# "All ages" col. in "Age Group". use .loc
census_2016_co_clean=census_2016_co.loc[census_2016_co["Age Group"]!="All ages"]
print(census_2016_co_clean.shape)
# Population Statistics
population_stats_county=census_2016_co_clean.groupby("County")["value"].agg([np.min, np.max, np.mean, np.median])
print(population_stats_county)
population_stats_age_group=census_2016_co_clean.groupby("Age Group")["value"].agg([np.min, np.max, np.mean, np.median])
print(population_stats_age_group)
population_total=census_2016_co_clean["value"].sum()
print("Total Population Census 2016 ="+str(population_total))
population_by_county=census_2016_co_clean.groupby("County")["value"].sum()
# Create a dataframe of population by county insert and column of the percentage of the total and sort descending.
population_by_county_df=pd.DataFrame(population_by_county)
population_by_county_df['%'] = ((population_by_county_df['value'] / population_by_county_df['value'].sum())*100).round(2).astype(str) + '%'
population_by_county_df=population_by_county_df.sort_values("value",ascending=False)
print(population_by_county_df)
# Create a dataframe of population by county, define the index order when creating the dataframe, insert a column of the percentage of the total
population_by_agegroup=census_2016_co_clean.groupby("Age Group")["value"].sum()
population_by_agegroup_df=pd.DataFrame(population_by_agegroup,index=['0 - 4 years','5 - 9 years','10 - 14 years','15 - 19 years','20 - 24 years','25 - 29 years','30 - 34 years','35 - 39 years','40 - 44 years','45 - 49 years','50 - 54 years','55 - 59 years','60 - 64 years','65 - 69 years','70 - 74 years','75 - 79 years','80 - 84 years','85 years and over'
])
population_by_agegroup_df['%'] = ((population_by_agegroup_df['value'] / population_by_agegroup_df['value'].sum())*100).round(2).astype(str) + '%'
print(population_by_agegroup_df)
# Population by age group as a bar chart
population_by_county.plot(x="County", y="Population in Millions", kind="bar", title="Population by County - Cenusus 2016")
plt.show()
# Age group as a percentage of population bar chart Pie chart
population_by_agegroup.plot(kind="pie", subplots=True, title="Population by Age Group - 2016 Census")
plt.show()

# Extract non car buying age groups