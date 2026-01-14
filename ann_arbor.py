import numpy as np
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

#--- Magic Numbers -----------------------------------------------------------------
DATA_PATH = 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv'
ANNOT_X = 310
FIGSIZE = (12,7)
DPI = 150
XLIM = (1, 367)
YLIM = (-50, 50)
#-----------------------------------------------------------------------------------

#--- Data ---
df = pd.read_csv(DATA_PATH)

dfmin = df[df['Element'] == 'TMIN'].copy()
dfmax = df[df['Element'] == 'TMAX'].copy()

def transform_to_celsius(tenths):
          return tenths / 10

dfmin['Deg_celsius'] = dfmin['Data_Value'].apply(transform_to_celsius)
dfmax['Deg_celsius'] = dfmax['Data_Value'].apply(transform_to_celsius)

#--- Weather station MIN / MAX ---
dfmin['Date'] = pd.to_datetime(dfmin['Date'])
dfmax['Date'] = pd.to_datetime(dfmax['Date'])

df_min_dec = (dfmin
          [~((dfmin['Date'].dt.month == 2) & (dfmin['Date'].dt.day == 29))]
          .groupby('Date', as_index=False)['Deg_celsius'].min()
             )

df_max_dec = (dfmax
          [~((dfmax['Date'].dt.month == 2) & (dfmax['Date'].dt.day == 29))]
          .groupby('Date', as_index=False)['Deg_celsius'].max()
          )

#--- 2015 DF creation ---
max15 = (dfmax
        [dfmax['Date'].dt.year == 2015]
        .groupby('Date', as_index=False)['Deg_celsius'].max()
        )

max15['Dayofyear'] = (
          max15['Date'].dt.dayofyear
)

min15 = (dfmin
         [dfmin['Date'].dt.year == 2015]
         .groupby('Date', as_index=False)['Deg_celsius'].min()
        )

min15['Dayofyear'] = (
          min15['Date'].dt.dayofyear
)

#--- Leap years ---
"""Min is leap en min after feb haalt het schrikkeljaar eruit. Ondanks dat de values eruit zijn voor een schrikkeljaar
zal dayofyear nog altijd de laatste dag als 366 tellen. Daarom krijg je nog steeds 366 groepen als je groepeert.
We trekken dan een gecombineerde true false af (namelijk schrikkeljaar en na 28 feb), maar bij aftrekken wordt true false -1 of -0"""

min_is_leap = df_min_dec['Date'].dt.is_leap_year
min_after_feb28 = (df_min_dec['Date'].dt.month > 2)

df_min_dec['Dayofyear'] = (
          df_min_dec['Date'].dt.dayofyear
          - (min_is_leap & min_after_feb28)
)

min_dec = (df_min_dec
          [~(df_min_dec['Date'].dt.year == 2015)]
          .groupby('Dayofyear', as_index=False)['Deg_celsius']
          .min()
)

max_is_leap = df_max_dec['Date'].dt.is_leap_year
max_after_feb28 = (df_max_dec['Date'].dt.month > 2)

df_max_dec['Dayofyear'] = (
          df_max_dec['Date'].dt.dayofyear
          - (max_is_leap & max_after_feb28)
)

max_dec = (df_max_dec
          [~(df_max_dec['Date'].dt.year == 2015)]
          .groupby('Dayofyear', as_index=False)['Deg_celsius']
          .max()
)

#--- Plotting ---
#Initiation
plt.figure(figsize = FIGSIZE, dpi = DPI)

ax = plt.gca()
ax.set_xlabel('Months', fontsize=14, color='black', labelpad=4)
ax.set_ylabel('Degrees Celsius (°C)', rotation=90, labelpad = 4, fontsize=14)
ax.set_title('Temperatures in Ann Arbor, Michigan:\n2005—2014 vs. 2015', fontsize=16, color='black', pad=8)

ax.set_xlim(XLIM)
ax.set_ylim(YLIM)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

month_starts = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

plt.xticks(month_starts, month_names)

x = plt.gca().xaxis
for item in x.get_ticklabels():
          item.set_rotation(30)

#Lineplots
plt.plot(max_dec['Dayofyear'], max_dec['Deg_celsius'], color='firebrick', linestyle='-', linewidth=1.25, alpha=0.7,
        label='Daily maximum temperatures (°C)\nin 2005-2014')

plt.plot(min_dec['Dayofyear'], min_dec['Deg_celsius'], color='dodgerblue', linestyle='-', linewidth=1.25, alpha=0.7,
        label='Daily minimum temperatures (°C)\nin 2005-2014')

leg1= ax.legend(loc='upper right', fontsize=8, labelspacing=0.25, borderpad=0.25, handlelength=1)

#Fillbetween
plt.gca().fill_between(
    min_dec['Dayofyear'],
    min_dec['Deg_celsius'],
    max_dec['Deg_celsius'],
    facecolor='lightgray',
    alpha=0.6
)

#Inline titles
y_max = max_dec.loc[max_dec['Dayofyear'] == ANNOT_X, 'Deg_celsius'].values[0]
y_min = min_dec.loc[min_dec['Dayofyear'] == ANNOT_X, 'Deg_celsius'].values[0]

plt.annotate(
    "Maximum daily \ntemperatures from \n2005-2014",
    xy=(ANNOT_X, y_max),
    xytext=(ANNOT_X, y_max - 25),   # onder de lijn
    arrowprops=dict(arrowstyle="->", color='firebrick'),
    color='firebrick',
    ha='left', fontsize='8'
)

plt.annotate(
    "Minimum daily \ntemperatures from \n2005-2014",
    xy=(ANNOT_X, y_min),
    xytext=(ANNOT_X, y_min - 25),   # onder de lijn
    arrowprops=dict(arrowstyle="->", color='dodgerblue'),
    color='dodgerblue',
    ha='left', fontsize='8'
)

#Scatterplot
#Align on index
max_m = max15.merge(max_dec, on='Dayofyear', suffixes=('_2015', '_hist'))
min_m = min15.merge(min_dec, on='Dayofyear', suffixes=('_2015', '_hist'))

mask_max = max_m['Deg_celsius_2015'] > max_m['Deg_celsius_hist']
mask_min = min_m['Deg_celsius_2015'] < min_m['Deg_celsius_hist']

plt.scatter(max_m.loc[mask_max, 'Dayofyear'], 
            max_m.loc[mask_max, 'Deg_celsius_2015'],
            s=15, c='red',
            label='2015 Record highs')

plt.scatter(min_m.loc[mask_min, 'Dayofyear'], 
            min_m.loc[mask_min, 'Deg_celsius_2015'],
            s=15, c='mediumblue', 
            label='2015 Record lows')

record_handles = [
    Line2D([0], [0], marker='o', color='w',
           markerfacecolor='red', markersize=6,
           label='2015 record highs'),
    Line2D([0], [0], marker='o', color='w',
           markerfacecolor='mediumblue', markersize=6,
           label='2015 record lows')
]

leg2 = ax.legend(
    handles=record_handles,
    loc='lower left',
    fontsize=8,
    frameon=False
)

ax.add_artist(leg1)

#--- Analysis Phrase ---
n_highs = mask_max.sum()
n_lows  = mask_min.sum()

txt = f"2015 record days: {n_highs} highs vs {n_lows} lows"

ax = plt.gca()
ax.text(
    0.02, 0.10, txt,                 # x,y in axes fraction
    transform=ax.transAxes,
    fontsize=8,
    ha='left', va='bottom',
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=3)
)

#--- Show ---
plt.tight_layout()
plt.show()



