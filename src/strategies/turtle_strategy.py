import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CSV_PATH_MSFT = os.path.join(BASE_DIR, "data", "raw", "MSFT.csv")

df_MSFT = pd.read_csv(CSV_PATH_MSFT, index_col='Date', parse_dates=True)

# Rolling channels
max20 = df_MSFT['High'].rolling(window=20).max()
min10 = df_MSFT['Low'].rolling(window=10).min()

# Shifts
max20_yesterday = max20.shift(1)
max20_two_days = max20.shift(2)
min10_yesterday = min10.shift(1)
min10_two_days = min10.shift(2)

close_today = df_MSFT['Close']
close_yesterday = df_MSFT['Close'].shift(1)

# Copy df
tortue_MSFT = df_MSFT.copy()
tortue_MSFT['Buy'] = 0
tortue_MSFT['Sell'] = 0

df_MSFT['Close'].plot()
max20.plot(color='green')
min10.plot(color='red')


# état de position
in_position = False

for date in tortue_MSFT.index:

    # BUY CONDITION
    if (not in_position) and \
       (close_today.loc[date] > max20_yesterday.loc[date]) and \
       (close_yesterday.loc[date] <= max20_two_days.loc[date]):
        
        tortue_MSFT.loc[date, 'Buy'] = 1
        in_position = True
        print("BUY SIGNAL :", date, tortue_MSFT.loc[date, 'Close'])
        continue   # on passe au jour suivant pour eviter de buy et sell le meme jour

    # SELL CONDITION 
    if (in_position) and \
       (close_today.loc[date] < min10_yesterday.loc[date]) and \
       (close_yesterday.loc[date] >= min10_two_days.loc[date]):

        tortue_MSFT.loc[date, 'Sell'] = 1
        in_position = False
        print("SELL SIGNAL :", date, tortue_MSFT.loc[date, 'Close'])

buy_points = tortue_MSFT[tortue_MSFT['Buy']==1]['Close']
sell_points = tortue_MSFT[tortue_MSFT['Sell']==1]['Close']
plt.scatter(buy_points.index, buy_points, marker='^', s=100, color='green', label='Buy Signal')
plt.scatter(sell_points.index, sell_points, marker='v', s=100, color='red', label='Sell Signal')

plt.legend()
plt.show()

# portfolio

trades = []

for date, row in tortue_MSFT.iterrows():
    if row['Buy'] == 1:
        trades.append({'Date': date, 'Side': 'BUY', 'Price': row['Close']})
    elif row['Sell'] == 1:
        trades.append({'Date': date, 'Side': 'SELL', 'Price': row['Close']})

trades = pd.DataFrame(trades).set_index('Date')

pnl_events = []
position = 0
entry_price = None

for date, trade in trades.iterrows():
    side = trade['Side']
    price = trade['Price']

    if side == 'BUY' and position == 0:
        position = 1
        entry_price = price

    elif side == 'SELL' and position == 1:
        profit = price - entry_price  
        pnl_events.append({'Date': date, 'PnL': profit})
        position = 0
        entry_price = None

pnl = pd.DataFrame(pnl_events).set_index('Date')

# Profit cumulé au moment de chaque SELL
pnl['Equity'] = pnl['PnL'].cumsum()

# Étaler sur toutes les dates du backtest
equity = pnl['Equity'].reindex(tortue_MSFT.index, method='ffill').fillna(0)

# Plot
plt.figure(figsize=(12, 6))
equity.plot(label='Turtle Equity (1 share)')
plt.title('Cumulative Profit of Turtle Strategy')
plt.ylabel('Profit (in price units)')
plt.legend()
plt.show()
