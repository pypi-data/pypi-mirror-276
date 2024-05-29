import torch
import numpy as np
from typing import List, Union
from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset
from ._tokenize_vec import TokenizeVec


def train_test_set(tokenize_vec: TokenizeVec, texts: List[str], y: Union[torch.LongTensor, List, np.ndarray], max_length: int = 0,
			  test_size=0.2, n_jobs=-1, random_state=None):
    X = tokenize_vec.parallel_encode_plus(texts, max_length=max_length, padding='max_length',
                                        truncation=True, add_special_tokens=True,
                                        return_token_type_ids=True,return_attention_mask=True,
                                        return_tensors='pt', n_jobs=n_jobs)
    if isinstance(y, List) or isinstance(y, np.ndarray):
        y = torch.tensor(y, dtype=torch.long)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return TensorDataset(X_train, y_train), TensorDataset(X_test, y_test)
