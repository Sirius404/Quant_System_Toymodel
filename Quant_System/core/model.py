import pandas as pd
import numpy as np
import fbprophet
import pytrends
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import matplotlib
import time

data = pd.read_csv('../Data/stock.csv')
indicator = ['open', 'close', 'high', 'low']
data['trade_date'] = pd.to_datetime(data['trade_date'])
prediction = pd.DataFrame(columns=['open', 'close', 'high', 'low','trade_date'])

def predict(data,indicator):
    data['ds'] = data['trade_date']
    data['y'] = data[indicator]

    def create_model():
        # Make the model
        model = fbprophet.Prophet(
            daily_seasonality=False,
            weekly_seasonality=False,
            yearly_seasonality=True,
            changepoint_prior_scale=0.05,
            changepoints=None,
        )

        model.add_seasonality(name="monthly", period=30.5, fourier_order=5)
        return model

    def predict_future(days=30):
        # Use past self.training_years years for training
        train = data

        model = create_model()

        model.fit(train)

        # Future dataframe with specified number of days to predict
        future = model.make_future_dataframe(periods=days, freq="D")
        future = model.predict(future)
        future = future[future["ds"] >= max(data["ds"])]
        future["diff"] = future["yhat"].diff()

        future = future.dropna()

        # Find the prediction direction and create separate dataframes
        future["direction"] = (future["diff"] > 0) * 1

        # Rename the columns for presentation
        future = future.rename(
            columns={
                "ds": "Date",
                "yhat": "estimate",
                "diff": "change",
                "yhat_upper": "upper",
                "yhat_lower": "lower",
            }
        )
        return future

    future = predict_future()

    return future

def get_pre(indicator=['open', 'close', 'high', 'low']):
    for i in indicator:
        prediction[i] = predict(data, i)['estimate']
    prediction['trade_date'] = predict(data, 'close')['Date']
    return prediction

# prediction = get_pre()
# print(prediction)
