import numpy as np

def split_list(lookback : int, multistep: int, data: List[any]):
    if(lookback<=0 or lookback>=len(data)):
        raise ValueError("lookback out of range :- (0-length of sequence)")
    if(multistep<1 or multistep>=len(data)):
        raise ValueError("multistep out of range :- (1-length of sequence)")
    if(lookback + multistep > len(data)):
        raise ValueError("lookback out of range")

    data= np.array(data)
    X, y= [], []
    for i in range(lookback, len(data)-multistep+1):
        X.append(data[i-lookback:i])
        y.append(data[i:i+multistep])
    return np.array(X), np.array(y)