import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CSV_PATH_AMD = os.path.join(BASE_DIR, "data", "raw", "AMD.csv")
CSV_PATH_GOOG = os.path.join(BASE_DIR, "data", "raw", "GOOG.csv")
CSV_PATH_MSFT = os.path.join(BASE_DIR, "data", "raw", "MSFT.csv")
CSV_PATH_NVDA = os.path.join(BASE_DIR, "data", "raw", "NVDA.csv")

df_AMD=pd.read_csv(CSV_PATH_AMD)    
df_GOOG=pd.read_csv(CSV_PATH_GOOG)  
df_MSFT=pd.read_csv(CSV_PATH_MSFT)  
df_NVDA=pd.read_csv(CSV_PATH_NVDA)  

# line charts des valeurs des actions de chacune des compagnies
x=df_AMD["Date"]
y=df_AMD["Close"]
plt.plot(x,y)
plt.show()
x=df_MSFT["Date"]
y=df_MSFT["Close"]
plt.plot(x,y)
plt.show()
x=df_GOOG["Date"]
y=df_GOOG["Close"]
plt.plot(x,y)
plt.show()
x=df_NVDA["Date"]
y=df_NVDA["Close"]
plt.plot(x,y)
plt.show()

# 
