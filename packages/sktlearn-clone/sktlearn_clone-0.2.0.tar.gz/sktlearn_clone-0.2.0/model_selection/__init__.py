from .kfold import KFold
from .train_test_split import TrainTestSplitter

def train_test_split(X, y, test_size=0.25, random_state=None):
    splitter = TrainTestSplitter(test_size=test_size, random_state=random_state)
    return splitter.split(X, y)