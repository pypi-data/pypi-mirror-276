from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import pickle
import numpy as np

def shuffle(data):
    """Shuffle dictionary of numpy array."""
    n = len(data[list(data.keys())[0]])
    idx = np.arange(n)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    for key in data.keys():
        data[key] = data[key][idx]
    return data


def split(data,k=0):
    """5-folding of dataset dictionary of numpy array.

    :param data: Dataset where each key maps to a numpy array.
    :type data: Dictionary
    :param k: (Optional) Indice of the fold, can be 0,1,2,3 or 4.
    :type k: int 
    :return: Dataset with train and test.
    :rtype: Dictionary
    """
    keys = list(data.keys())
    n = np.shape(data[keys[0]])[0]
    idx = np.linspace(0,n-1,n).astype(int)
    test = (idx[int(k*0.2*(n))]<=idx)&(idx<=idx[int((k+1)*0.2*(n-1))])
    train = ~test
    data_split = {"train":{},"test":{}}
    for key in keys:
        data_split["train"][key] = data[key][train]
        data_split["test"][key] = data[key][test]

    return data_split["train"],data_split["test"]
 
def mia():
    path = Path("result", "mia.pickle")
    with open(path, 'rb') as f:
        data = pickle.load(f)
    data = shuffle(data)
    print(len(data["loss"]))
    clf = RandomForestClassifier()
    train, test = split(data)
    clf.fit(train["loss"].reshape(-1,1), train["member"])
    member_hat = clf.predict(test["loss"].reshape(-1,1))
    member = test["member"]
    print(np.unique(member))
    balanced_accuracy = np.mean([np.mean(member_hat[member==m]==m) for m in np.unique(member)])
    print(balanced_accuracy)

if __name__=="__main__":
    mia()

