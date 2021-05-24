import tabula
import pandas as pd
import numpy as np
import os

page = os.path.dirname(__file__) + '/pdf/vnp-1sept20.pdf'
table = tabula.read_pdf(page,
                        stream=True, pages='all',
                        area=(78.57, 84.34, 78.57+639.35, 84.34+358.49),
                        multiple_tables=False, guess=False)
df = table[0][1:]
df.columns = ['MP', 'Record', 'todrop']
df['Record'].ffill(axis=0, inplace=True)
df['Date'] = pd.to_datetime(df['Record'].loc[df.loc[df['Record'] == 'PRESENT:'].index[0]-2])
df.drop(['todrop'], axis=1, inplace=True)
df = df[(df['Record'] == 'PRESENT:') | (df['Record'] == 'ABSENT:')]
df = df[df['MP'].notna()]
titles = ['Assoc', 'Dr', 'Miss', 'Mr', 'Ms']
df1 = df[df['MP'].str.split(' ').str[0].isin(titles)]
    # df.drop(columns=d f.columns[0],
#         axis=1,
#         inplace=True)
# df.columns = ['School', 'IP Non-affiliated', 'Express Non-affiliated', 'N(A) Non-affiliated', 'N(T) Non-affiliated'
#               , 'IP Affiliated', 'Express Affiliated', 'N(A) Affiliated', 'N(T) Affiliated']
# df['School'].fillna('School', inplace=True)
# df = df[df['School'] != 'School']
# for column in df.columns[1:]:
#     df[column] = df[column].str.replace(r'((?<!\d)\d{1}(?!\d))',r'0\1', regex=True)
# df.fillna('N/A', inplace=True)
# df.drop(['index'], axis=1, inplace=True)
#
print('debug')
# df.to_csv('/Users/whkoh/dev/sites/2021-psle-schools/data.csv')