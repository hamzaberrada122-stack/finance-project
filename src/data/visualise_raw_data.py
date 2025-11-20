import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CSV_PATH_AMD = os.path.join(BASE_DIR, "data", "raw", "AMD.csv")
CSV_PATH_GOOG = os.path.join(BASE_DIR, "data", "raw", "GOOG.csv")
CSV_PATH_MSFT = os.path.join(BASE_DIR, "data", "raw", "MSFT.csv")
CSV_PATH_NVDA = os.path.join(BASE_DIR, "data", "raw", "NVDA.csv")

df_AMD=pd.read_csv(CSV_PATH_AMD,index_col='Date',parse_dates=True)    
df_GOOG=pd.read_csv(CSV_PATH_GOOG,index_col='Date',parse_dates=True)  
df_MSFT=pd.read_csv(CSV_PATH_MSFT,index_col='Date',parse_dates=True)  
df_NVDA=pd.read_csv(CSV_PATH_NVDA,index_col='Date',parse_dates=True)  

# line charts des valeurs des actions de chacune des compagnies
df_AMD['Close'].loc['2022'].plot()
df_AMD['Close'].loc['2022'].resample('M').mean().plot(label='moyenne par mois',alpha=0.8,ls=':',lw=3)
df_AMD['Close'].loc['2022'].resample('W').mean().plot(label='moyenne par semaine',alpha=0.8,ls='--',lw=2)

plt.legend()
plt.show()

#construction d'une table qui a comme les lignes les mois a la place des jours, et a comme colonnes les funcs means,std etc
m= df_AMD['Close'].resample('M').agg(['mean','std','max','min'])

#construction d'un plot où on visualise la moyenne entouré en transparent du min max des valeurs sur des lignes sous format <mois>
m['mean'].plot(label='moyenne')
plt.fill_between(m.index,m['min'],m['max'],alpha=0.2,label='min-max')
plt.legend()
plt.show()

#plot pour comparer la construction du plot avec rolling prenant la moyenne de 3 jours vs 10 vs 15
df_AMD['Close'].loc['2020'].rolling(window=3).mean().plot(label='moyenne en 3 jours')
df_AMD['Close'].loc['2020'].rolling(window=10).mean().plot(label='moyenne en 10 jours',alpha=0.8,ls=':')
df_AMD['Close'].loc['2020'].rolling(window=15).mean().plot(label='moyenne en 15 jours',alpha=0.6,ls='--')
plt.legend()
plt.show()

#plot construction avec moyenne exponentielle prenant differentes valeurs: 0.2, 0.4 etc
for i in np.arange(0.2,1,0.2):
    df_AMD['Close'].loc['2023-03'].ewm(alpha=i).mean().plot(label=f'ewm {i}',ls=':')

plt.legend()
plt.show()

#on merge deux tableaux MAD et NVIDIA et on formate les suffixes
m2 = pd.merge(df_AMD,df_NVDA,on='Date',how='inner',suffixes=('_AMD','_NVIDIA'))

m2[['Close_AMD','Close_NVIDIA']].plot()
plt.show()

#on fait la meme avec google et msft (merge)
m3 = pd.merge(df_GOOG,df_MSFT,on='Date',how='inner',suffixes=('_GOOG','_MSFT'))

m3[['Close_GOOG','Close_MSFT']].plot(subplots=True)
plt.show()

#table avec les 4 entreprises m5 mergeant m3 et m4
m4 = pd.merge(df_AMD,df_NVDA,on='Date',how='inner',suffixes=('_AMD','_NVDA',))
m5=pd.merge(m3,m4,on='Date',how='inner',suffixes=('_GOOG','_MSFT','_AMD','_NVDA'))

#calculer la correlation entre toutes les entreprises de 2020 à 2025
corr = m5[['Close_AMD','Close_NVDA','Close_MSFT','Close_GOOG']].corr()
plt.matshow(corr, cmap='coolwarm')
plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
plt.yticks(range(len(corr.index)), corr.index)
plt.show()

# x=df_AMD["Date"]
# y=df_AMD["Close"]
# plt.plot(x,y)
# plt.show()
# x=df_MSFT["Date"]
# y=df_MSFT["Close"]
# plt.plot(x,y)
# plt.show()
# x=df_GOOG["Date"]
# y=df_GOOG["Close"]
# plt.plot(x,y)
# plt.show()
# x=df_NVDA["Date"]
# y=df_NVDA["Close"]
# plt.plot(x,y)
# plt.show()

