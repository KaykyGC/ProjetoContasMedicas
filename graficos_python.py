import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def random_dates(start, end, n=10):
    start_u = start.value//10**9
    end_u = end.value//10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

start_date = pd.to_datetime('2025-01-01')
end_date = pd.to_datetime('2025-12-31')
num_datas = 50 # quantidade de datas aleatórias

datas = random_dates(start_date, end_date, n=num_datas)





df = pd.DataFrame({
    'data': datas,
    

})
print(df)


