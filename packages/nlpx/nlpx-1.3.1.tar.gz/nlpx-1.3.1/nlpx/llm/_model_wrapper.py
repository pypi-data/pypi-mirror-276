import torch
import numpy as np
from torch import optim
from pathlib import Path
from typing import Union, List
from torch.nn import functional as F
from torch.utils.data import DataLoader, TensorDataset, Dataset

from nlpx.training import Trainer, SimpleTrainer, evaluate
from ._tokenize_vec import TokenizeVec


class ModelWrapper:

	def __init__(self, model_path: Union[str, Path] = None, classes: List[str] = None,
					device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		self.classes = classes
		self.device = device
		self.model = torch.load(model_path, map_location=device) if model_path else None

	def train(self, model, train_set: Dataset, eval_set: Dataset, collate_fn=None, max_iter=100,
				optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
				batch_size=8, eval_batch_size=16,
				num_workers=4, num_eval_workers=2,
				early_stopping_rounds=10):
		trainer = Trainer(model, train_set, eval_set, collate_fn,
						  max_iter, optimizer, learning_rate, T_max,
						  batch_size, eval_batch_size,
						  num_workers, num_eval_workers,
						  early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
						  self.device)
		self.model = trainer.train()

	def predict(self, X: torch.FloatTensor):
		logits = self.logits(X)
		return logits.argmax(1)

	def predict_classes(self, X: torch.FloatTensor):
		assert self.classes is not None, 'classes must be specified'
		pred = self.predict(X)
		return [self.classes[i] for i in pred.detach().numpy().ravel()]

	def predict_proba(self, X: torch.FloatTensor):
		logits = self.logits(X)
		result = F.softmax(logits, dim=1).max(1)
		return result.indices, result.values

	def predict_classes_proba(self, X: torch.FloatTensor):
		assert self.classes is not None, 'classes must be specified'
		indices, values = self.predict_proba(X)
		return [self.classes[i] for i in indices.detach().numpy().ravel()], values

	def logits(self, X: torch.FloatTensor):
		self.model.eval()
		with torch.no_grad():
			logits = self.model(X)
		return logits

	def evaluate(self, eval_set: Dataset, batch_size=16, num_workers=0, max_length: int = 0,  collate_fn=None):
		eval_loader = DataLoader(dataset=eval_set, batch_size=batch_size,
								 num_workers=num_workers, collate_fn=collate_fn)
		_, acc = evaluate(self.model, eval_loader, self.device)
		return acc

	def save(self, model_path: Union[str, Path] = './best_model.pt'):
		torch.save(model_path, self.model)

	def load(self, model_path: Union[str, Path] = './best_model.pt'):
		self.model = torch.load(model_path, map_location=self.device)


class SimpleModelWrapper(ModelWrapper):

	def __init__(self, tokenize_vec: TokenizeVec, model_path: Union[str, Path] = None, classes: List[str] = None,
				device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(model_path, classes, device)
		self.tokenize_vec = tokenize_vec

	def train(self, model, texts: List[str], y: Union[torch.LongTensor, List, np.ndarray], max_length: int = 0,
			  eval_size=0.2, random_state=None, collate_fn=None,max_iter=100,
			  optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
			  batch_size=8, eval_batch_size=16,
			  num_workers=4, num_eval_workers=2,
			  early_stopping_rounds=10, n_jobs=-1):
		X = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
		if isinstance(y, List) or isinstance(y, np.ndarray):
			y = torch.tensor(y, dtype=torch.long)
		trainer = SimpleTrainer(model, X, y, eval_size, random_state, collate_fn,
								 max_iter, optimizer, learning_rate, T_max,
								 batch_size, eval_batch_size,
								 num_workers, num_eval_workers,
								 early_stopping_rounds,
								 self.device)
		self.model = trainer.train()

	def predict(self, texts: List[str], max_length: int = 0, n_jobs=-1):
		logits = self.logits(texts, max_length, n_jobs=n_jobs)
		return logits.argmax(1)

	def predict_classes(self, texts: List[str], max_length: int = 0, n_jobs=-1):
		assert self.classes is not None, 'classes must be specified'
		pred = self.predict(texts, max_length, n_jobs=n_jobs)
		return [self.classes[i] for i in pred.detach().numpy().ravel()]
	
	def predict_proba(self, texts: List[str], max_length: int = 0, n_jobs=-1):
		logits = self.logits(texts, max_length, n_jobs=n_jobs)
		result = F.softmax(logits, dim=1).max(1)
		return result.indices, result.values

	def predict_classes_proba(self, texts: List[str], max_length: int = 0, n_jobs=-1):
		assert self.classes is not None, 'classes must be specified'
		indices, values = self.predict_proba(texts, max_length, n_jobs)
		return [self.classes[i] for i in indices.detach().numpy().ravel()], values

	def logits(self, texts: List[str], max_length: int = 0, n_jobs=-1):
		X = self.get_vec(texts, max_length, n_jobs=n_jobs)
		return super().logits(X)

	def evaluate(self, texts: List[str], y: Union[torch.LongTensor, List, np.ndarray], batch_size=16, num_workers=0,
				 max_length: int = 0, collate_fn=None, n_jobs=-1):
		X = self.get_vec(texts, max_length, n_jobs=n_jobs)
		if isinstance(y, List) or isinstance(y, np.ndarray):
			y = torch.tensor(y, dtype=torch.long)
		eval_set = TensorDataset(X, y)
		return super().evaluate(eval_set, batch_size=batch_size, num_workers=num_workers, collate_fn=collate_fn)

	def get_vec(self, texts: List[str], max_length: int, n_jobs: int):
		return self.tokenize_vec.parallel_encode_plus(texts, max_length=max_length, padding='max_length',
														truncation=True, add_special_tokens=True,
														return_token_type_ids=True,return_attention_mask=True,
														return_tensors='pt', n_jobs=n_jobs)

