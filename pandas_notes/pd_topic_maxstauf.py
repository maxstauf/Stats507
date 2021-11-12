# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
#     notebook_metadata_filter: markdown
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ## Contents
# Add a bullet for each topic and link to the level 2 title header using 
# the exact title with spaces replaced by a dash. 
#
# + [Topic: Categorical Data in Pandas](#Topic:-Categorical-Data-in-Pandas) 
# + [Categorical Data Overview ](#Categorical-Data-Overview)
# + [Creating Categorical Data](#Creating-Categorical-Data) 
# + [Categorical Caveats ](#Categorical-Caveats)
# + [Categorical Operations](#Categorical-Operations)

# ## Topic: Categorical Data in Pandas
# ### Maxwell Stauffer
# maxstauf@umich.edu

#Requirements:
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

# ## Categorical Data Overview 

#  - A data type corresponding to a variable that takes on a limited, fixed 
# number of possible values.
#  - Examples: gender, blood type, state, etc.
#  - Obvious comparison is with R's `factor`
#

# ## Creating Categorical Data

# - Data consists of an array of `categories`, with an integer array of `codes`
# that point to the real value.
# - Many different ways to construct
#     - Let `dtype="category"` when creating a `Series`
#     - Converting column using `.astype("category")`
#     - Using `cut()` to group data in bins
#     - Passing a `pandas.Categorical` object directly

df = pd.DataFrame({"value": np.random.randint(0, 100, 20)})
labels = ["{0} - {1}".format(i, i + 9) for i in range(0, 100, 10)]
df["group"] = pd.cut(df.value, range(0, 105, 10), right=False, labels=labels)
df.head(10)

# ## Categorical Caveats 

# - Note that for the example above, we gave labels to assign to each category,
# this is not always the case with categorical variable creation
# - Unlike R's `factor`, categorical data does not convert input values to 
# strings, they are the same data type as the original values
# - Thus in most methods, there is no current way to assign or change labels at
# creation time. Use `.rename_categories` to change the categories after 
# creation time.
# - This interaction puzzled me in HW2, and led me to want to investigate this

raw_cat = pd.Categorical(["a", "b", "c", "d"], 
                         categories={"b" : "boy", "c" : "cat", "d" : "disk"}, 
                         ordered=False
)
print(raw_cat) # Our dictionary supplying labels failed, only took keys
raw_cat.rename_categories({"b":"baseball", "c":"clam chowder", "d":"dogs"})

# ##  Categorical Operations

# - Can append or remove categories with `.add_categories` or 
# `.remove_categories`
# - `CategoricalDtype` (which has to be imported) allows comparison based on 
# ordering the categories (by default categories are unordered)
# - Many pandas operations work with Categorical variables, if the underlying 
# type is correct
#     - Get counts with `Series.value_counts()`, do comparisons with boolean 
# operations
#     - Some exceptions: `Series.max()`, `Series.min()`, `Series.mode()` won't 
# work
#     - String and datetime operations work if categories are those types

# +
cat = pd.Series([1, 2, 3]).astype(CategoricalDtype([3, 2, 1], ordered=True))

cat_b = pd.Series([2, 2, 2]).astype(CategoricalDtype([3, 2, 1], ordered=True))
# cat > cat_b
# -




