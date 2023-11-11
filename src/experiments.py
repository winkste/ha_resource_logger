#%%
import os
from pathlib import Path
import pandas as pd
#%%

print(Path.cwd())
df = pandas.read_csv('../bin/data copy.csv', index_col='date', parse_dates=['date'])
print(df)


# %%
import pandas as pd

x = pd.Series(['2023-10-08 00:00:00', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0'])
print(x) 

# %%
df2 = df.append(x, ignore_index=True)
print(df2)

# %%
input_data = ['2023-10-08 00:00:00', '1.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0']

#%%
new_index = pd.to_datetime(input_data[0])
new_index

new_data_set = input_data[1:]
new_data_set

# Get the list of all column names from headers
column_names = df.columns.values.tolist()
column_names
# %%
new_row = pd.DataFrame([new_data_set], columns=column_names, index=[new_index])
new_row
# %%
df2 = pd.concat([df, pd.DataFrame(new_row)], ignore_index=False)
df2
# %%

#%%
import pandas

# load the all data from the csv data set file
df = pandas.read_csv('../bin/data copy.csv', index_col='date', parse_dates=['date'])

# prepare the new data set to be integrated into the data frame

# get the column names from the existing data frame as list
column_names = df.columns.values.tolist()
# input data as list : [DATE_TIME, 0...9 Values]
input_data = ['2023-10-10', '2.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0']
# convert the first element in the input data into date object
new_date_index = pd.to_datetime(input_data[0]).date()
# slice just the data values without the date_time
new_data_set = input_data[1:]
# create a new dataframe based on the data set, the column names and the new time based index
new_row = pd.DataFrame([new_data_set], columns=column_names, index=[new_date_index])
# concatenate the two data frames to one
df2 = pd.concat([df, pd.DataFrame(new_row)], ignore_index=False)
print(df2)
df2.to_csv('../bin/data copy2.csv', index='date', index_label="date")

# %%
input_data = ['2023', '2.0', '0.0', '0.0', '0.0']
data_frame = pd.read_csv('../bin/history.csv', index_col='year')
print(data_frame)
#%%
# prepare the new data set to be integrated into the data frame
# get the column names from the existing data frame as list
column_names = data_frame.columns.values.tolist()
#%%
# convert the first element in the input data into date object
new_data_index = input_data[0]
# slice just the data values without the date_time
new_data_set = input_data[1:]
# create a new dataframe based on the data set, the column names and the new time based index
new_row = pd.DataFrame([new_data_set], columns=column_names, index=[new_data_index])
print(new_row)

#%%
# concatenate the two data frames to one
data_frame2 = pd.concat([data_frame, pd.DataFrame(new_row)], ignore_index=False)
#print(data_frame2)

#%%
index = data_frame2.index
#%%
dupli = data_frame2.index.duplicated(keep='last')
print(dupli)

#%%
data_frame = pd.read_csv('../bin/history.csv')
#print(data_frame)
data_frame2 = data_frame.drop_duplicates(subset="year", keep='last')
print(data_frame2)
#%%
idx = pd.Index(data_frame2)
print(idx)
idx.duplicated()

#%%
data_frame3 = data_frame2[~data_frame2.index.duplicated(keep='last')]
#print(data_frame3)

#%%
data_frame = pd.read_csv('../bin/history copy.csv')
clean_data = data_frame.drop_duplicates(subset="year", keep='last')
clean_data = clean_data.set_index('year')
print(clean_data)

#%%
data_frame = pd.read_csv('../bin/actuals copy.csv')
clean_data = data_frame.drop_duplicates(subset="date", keep='last')
clean_data = clean_data.set_index('date')
print(clean_data)
#%%
data_frame.set_index('year')
#%%
print(clean_data.set_index('year'))
#%%
print(clean_data)
#%%
clean_data.to_csv('../bin/history copy.csv', index="year", index_label="year")
# %%

#%%
import os
from pathlib import Path
import pandas as pd

data_frame = pd.read_csv('../bin/actuals copy.csv')

# %%
print(data_frame.iloc[-1].tolist())
# %%
import os
from pathlib import Path
import pandas as pd
hist_file_name = '../bin/history copy.csv'

input_data = ['2023', '20', '30', '40', '50']

#%%
# load the all data from the csv data set file
data_frame = pd.read_csv(hist_file_name, index_col='year')
# prepare the new data set to be integrated into the data frame
# get the column names from the existing data frame as list
column_names = data_frame.columns.values.tolist()
# convert the first element in the input data into date object
new_data_index = input_data[0]
# slice just the data values without the date_time
new_data_set = input_data[1:]

#%%
# create a new dataframe based on the data set, the column names and the new time based index
new_row = pd.DataFrame([new_data_set], columns=column_names, index=[new_data_index])
# concatenate the two data frames to one
#%%
data_frame = pd.concat([data_frame, pd.DataFrame(new_row)], ignore_index=False)
#%%
data_frame.index = data_frame.index.astype(int)
data_frame.sort_index()
#%%
# store the update dataframe back to file
data_frame.to_csv(hist_file_name, index="year", index_label="year")
# clean the data set from duplicates
#remove_duplicates_from_data_file(hist_file_name, 'year')

#%%
data_frame = pd.read_csv(hist_file_name, index_col='year')
#%%
data_frame = pd.read_csv(hist_file_name)
data_frame.index = data_frame.index.astype(int)
#%%
list_data = data_frame.iloc[-1].tolist()
index = data_frame.index
# %%
data_frame.tail(1).index.item()
list = data_frame.tail(1).values.tolist()[0]
list[0]
list.insert(0, data_frame.tail(1).index.item())

#%%
df = data_frame.tail(1)
df.index = df.index.astype(str)
list_data = df.iloc[-1].tolist()
# %%
