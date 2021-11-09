# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 22:43:50 2021

@author: Max Stauffer
"""

import pandas as pd
from os.path import exists
import pickle

# # Question 3
#
# In this question you will use Pandas to read, clean, and append several data 
# files from the National Health and Nutrition Examination Survey NHANES. We 
# will use the data you prepare in this question as the starting point for 
# analyses in one or more future problem sets. For this problem, you should use 
# the four cohorts spanning the years 2011-2018. Find links to different
# NHANES cohorts [here](https://wwwn.cdc.gov/nchs/nhanes/Default.aspx).
#
# Hint: Use `pd.read_sas()` to import files with the .XPT (“SAS transport”) 
# extension.
#
# a. Use Python and Pandas to read and append the demographic datasets keeping 
# only columns containing the unique ids (SEQN), age (RIDAGEYR), race and 
# ethnicity (RIDRETH3), education (DMDEDUC2), and marital status (DMDMARTL), 
# along with the following variables related to the survey weighting: 
# (RIDSTATR, SDMVPSU, SDMVSTRA, WTMEC2YR, WTINT2YR). Add an additional 
# column identifying to which cohort each case belongs. Rename the columns 
# with literate variable names using all lower case and convert each column 
# to an appropriate type. Finally, save the resulting data frame to a 
# serialized “round-trip” format of your choosing (e.g. pickle, feather,
# or parquet).

dmdata = pd.DataFrame()
# We want to define some useful variables we will use in part (a), like the url
# of the data set, the four cohorts, and some of the preferred column names 
url = 'https://wwwn.cdc.gov/Nchs/Nhanes/'
colnames = {'SEQN':'id', 
            'RIDAGEYR':'age',
            'RIDRETH3':'race',
            'DMDEDUC2':'edu',
            'DMDMARTL':'married',
            'RIDSTATR':'exam_status',
            'SDMVPSU':'mvpsu',
            'SDMVSTRA':'mvstra',
            'WTMEC2YR':'int2yr',
            'WTINT2YR':'mec2yr'
            }
cohorts = {'G':'2011-2012',
           'H':'2013-2014',
           'I':'2015-2016',
           'J':'2017-2018'}       

# This piece of code is reading in data from each year, from the web if not 
# downloaded locally. It then changes the column names, meging row-wise into
# one large dataframe while appending a new variable for cohort.    

for cohort in cohorts:
    if exists("DEMO_" + cohort + ".XPT"):
        df = pd.read_sas("DEMO_" + cohort + ".XPT")
    else:
        df = pd.read_sas(url + cohorts[cohort]+"/DEMO_" + cohort + ".XPT")
    df = (df
          .rename(columns=colnames)
          .loc[:,colnames.values()]
          .assign(cohort=cohorts[cohort])
          )
    dmdata = pd.concat((dmdata, df), axis = 0)

# Finally we change some of the column's datatypes to categorical in order to
# better fit the data for future analysis. Codes are taken from the NHANES
# codebook.

cat_vars = {
    'race': {
        1: "Mexican American",
        2: "Other Hispanic",
        3: "Non-Hispanic White",
        4: "Non-Hispanic Black",
        6: "Non-Hispanic Asian",
        7: "Other race including multi-racial"
        },
    'edu': {
        1: "Less than 9th grade",
        2: "9-11th Grade",
        3: "High school / GED",
        4: "AA or some college",
        5: "College graduate or above",
        7: "Refused",
        9: "Don't Know"
        },
    'married' : {
        1: "Married",
        2: "Widowed",
        3: "Divorced",
        4: "Separated",
        5: "Never married",
        6: "Living with partner",
        77: "Refused",
        99: "Dont know"
        },
    'exam_status' : {
        1: "Interviewed only",
        2: "Both interviewed and MEC examined"
        }
    }
for c in cat_vars.keys():
    dmdata[c] = dmdata[c].replace(cat_vars[c])
    dmdata[c] = pd.Categorical(dmdata[c])

# Writing the dataframe to a file using pickle:

f = open('dmdata.pickle', 'wb')
pickle.dump(dmdata, f)
f.close()

# b. Repeat part a for the oral health and dentition data (OHXDEN_*.XPT) 
# retaining the following variables: SEQN, OHDDESTS, tooth counts (OHXxxTC), 
# and coronal cavities (OHXxxCTC).

oraldentdata = pd.DataFrame()
# Similarly to part (a), we conditionally read in the data frame by cohort,
# then merging them all row-wise into one large data frame. Along the way we
# modify the column names to be more informative.
colnames = {'SEQN':'id',
            'OHDDESTS':'dent_status'
            }
for cohort in cohorts:
    if exists("OHXDEN_" + cohort + ".XPT"):
        df = pd.read_sas("OHXDEN_" + cohort + ".XPT", 
                         format='xport',encoding='utf-8')
    else:
        df = pd.read_sas(url + cohorts[cohort] + "/OHXDEN_" + cohort + ".XPT",
                         format='xport', encoding= 'utf-8')
    dfcopy = (df
              .copy()
              .filter(regex='.+[^R]TC$')
          )
    dfcopy.columns = (['coronal_cavity_' + c[3:5] if c.endswith('CTC') 
                       else 'tooth_count_' + c[3:5] for c in dfcopy.columns])
    df = pd.concat(
        (
            (df
             .rename(columns=colnames)
             .loc[:,('id', 'dent_status')]
             .assign(cohort=cohorts[cohort])
             ),
        dfcopy), axis = 1)
    oraldentdata = pd.concat((oraldentdata, df), axis=0)
oraldentdata = oraldentdata.reset_index(drop=True)

# Finally we switch some of the columns to be categorical data.

for col in [cols for cols in oraldentdata.columns if (cols != 'cohort' and
                                                      cols != 'id')]:
    if col.startswith('coronal_cavity'):
        oraldentdata[col] = oraldentdata[col].replace({
            'D': 'Sound primary tooth',
            'E': 'Missing due to dental disease',
            'J': 'Permanent root tip, no restorative replacement',
            'K': 'Primary tooth with surface condition',
            'M': 'Missing due to other causes',
            'P': 'Missing due to dental disease replaced with removable',
            'Q': 'Missing due to other causes replaced with removable',
            'R': 'Missing due to dental disease but fixed restoration',
            'S': 'Sound permanent tooth',
            'T': 'Permanent root tip is present but replaced',
            'U': 'Unerupted',
            'X': 'Missing due to other causes, but fixed restoration',
            'Z': 'Tooth present, condition cannot be assessed'
            })
        oraldentdata[col] = pd.Categorical(oraldentdata[col])
    elif col.startswith('tooth_count'):
        oraldentdata[col] = oraldentdata[col].replace({
            1: 'Primary tooth present',
            2: 'Permanent tooth present',
            3: 'Dental implant',
            4: 'Tooth not present',
            5: 'Permanent dental root fragment present',
            9: 'Could not assess'
            })
        oraldentdata[col] = pd.Categorical(oraldentdata[col])
    else:
        oraldentdata[col] = oraldentdata[col].replace({
            1: 'Complete',
            2: 'Partial',
            3: 'Not done'
            })
        oraldentdata[col] = pd.Categorical(oraldentdata[col])

# Writing the dataframe to a file using pickle:

f = open('oraldentdata.pickle', 'wb')
pickle.dump(oraldentdata, f)
f.close()


# c. In your notebook, report the number of cases there are in the two 
# datasets above.

print(dmdata.shape)
print(oraldentdata.shape)