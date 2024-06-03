import torch
from torch import optim
from torch.utils.data import DataLoader, TensorDataset, Dataset
from torch.optim.lr_scheduler import CosineAnnealingLR
from sklearn.model_selection import train_test_split


def evaluate(model, eval_loader, device):
	total = 0.0
	losses = 0.0
	correct = 0.0
	model.eval()
	with torch.no_grad():
		for x, y in eval_loader:
			x, y = x.to(device), y.to(device)
			loss, logits = model(x, y)
			correct += (logits.argmax(1) == y).sum().item()
			losses += loss.item()
			total += len(y)
	return losses / total, correct / total


class Trainer:

	def __init__(self, model, train_set: Dataset, eval_set: Dataset, collate_fn=None,
				 max_iter=100, optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
				 batch_size=8, eval_batch_size=16,
				 num_workers=4, num_eval_workers=2,
				 early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
				 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
				 ):
		self.model = model.to(device)
		self.train_loader = DataLoader(dataset=train_set, batch_size=batch_size,
									   num_workers=num_workers, shuffle=True, collate_fn=collate_fn)
		self.eval_loader = DataLoader(dataset=eval_set, batch_size=eval_batch_size,
									  num_workers=num_eval_workers, collate_fn=collate_fn)
		self.max_iter = max_iter
		self.optimizer = optimizer(model.parameters(), lr=learning_rate)
		self.T_max = T_max
		self.early_stopping_rounds = early_stopping_rounds
		self.device = device

	def train(self):
		cnt = 0
		cnt2 = 0
		best_acc = 0.0
		last_acc = 0.0
		min_loss = 100.0
		best_model = None
		if self.T_max and self.T_max > 0:
			scheduler = CosineAnnealingLR(self.optimizer, T_max=self.T_max)
		for epoch in range(self.max_iter):
			total = 0.0
			losses = 0.0
			correct = 0.0
			self.model.train()
			for x, y in self.train_loader:
				x, y = x.to(self.device), y.to(self.device)
				loss, logits = self.model(x, y)
				self.optimizer.zero_grad()
				loss.backward()
				self.optimizer.step()
				if self.T_max and self.T_max > 0:
					scheduler.step()

				losses += loss.item()
				correct += (logits.argmax(1) == y).sum().item()
				total += len(y)

			val_loss, val_acc = evaluate(self.model, self.eval_loader, self.device)
			print('epoch-{}/{}\tlr: {:.6f}, train_loss: {:.4f}, train_acc: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}'.format(
				epoch + 1, self.max_iter, self.optimizer.param_groups[0]['lr'], losses / total, correct / total, val_loss, val_acc
			))

			if val_acc > best_acc or (val_acc == best_acc and val_loss < min_loss):
				best_acc = val_acc
				best_model = self.model
				cnt = 0
				cnt2 = 0
				last_acc = val_acc
				best_acc = max(best_acc, val_acc)
				min_loss = min(min_loss, val_loss)
				continue

			if epoch >= min(5, self.early_stopping_rounds) and max(cnt, cnt2) >= self.early_stopping_rounds:  # x次epoch的val_acc不提升或x次epoch的val_acc不变化
				print("Early stopping at epoch-{}/{}".format(epoch + 1, self.max_iter))
				break

			if last_acc == val_acc:  # val_acc不在变化
				cnt2 += 1
			else:
				cnt2 = 0

			cnt += 1
			last_acc = val_acc
			best_acc = max(best_acc, val_acc)
			min_loss = min(min_loss, val_loss)
		return best_model


class SimpleTrainer(Trainer):

	def __init__(self, model, X, y, eval_size=0.2, random_state=None, collate_fn=None,
				 max_iter=100, optimizer=optim.AdamW, learning_rate=0.001, T_max: int = 0,
				 batch_size=8, eval_batch_size=16,
				 num_workers=4, num_eval_workers=2,
				 early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
				 device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=eval_size, random_state=random_state)
		super().__init__(model,
						 TensorDataset(X_train, y_train),
						 TensorDataset(X_test, y_test),
						 collate_fn,
						 max_iter,
						 optimizer,
						 learning_rate,
						 T_max,
						 batch_size,
						 eval_batch_size,
						 num_workers,
						 num_eval_workers,
						 early_stopping_rounds,
						 device
						 )
