import math
import torch
from torch import nn
import torch.nn.functional as F


def attention(query: torch.Tensor, key: torch.Tensor, value: torch.Tensor):
	batch_size, length, d_k = key.size()
	key = key.contiguous()
	scores = torch.matmul(query, key.view(batch_size, d_k, length)) / math.sqrt(d_k)
	scores = F.softmax(scores, dim=-1)
	return torch.matmul(scores, value).sum(dim=1)


class ClassifySelfAttention(nn.Module):

	def __init__(self, embed_dim: int):
		super().__init__()
		self.w_omega = nn.Parameter(torch.Tensor(embed_dim, embed_dim))
		self.u_omega = nn.Parameter(torch.Tensor(embed_dim, 1))
		nn.init.uniform_(self.w_omega, -0.1, 0.1)
		nn.init.uniform_(self.u_omega, -0.1, 0.1)

	def forward(self, x: torch.Tensor):
		u = torch.tanh(torch.matmul(x, self.w_omega))
		att = torch.matmul(u, self.u_omega)
		att_score = F.softmax(att, dim=1)
		scored_x = x * att_score
		return torch.sum(scored_x, dim=1)


class MultiHeadClassifySelfAttention(nn.Module):

	def __init__(self, embed_dim: int, num_heads: int = 1):
		super().__init__()
		self.num_heads = num_heads
		self.attention = ClassifySelfAttention(num_heads * embed_dim)

	def forward(self, x: torch.Tensor):
		if self.num_heads > 1:
			x = torch.concat([x for _ in range(self.num_heads)], dim=-1)
		return self.attention(x)


class RNNAttention(nn.Module):

	def __init__(self, embed_dim: int, hidden_size: int = 64, num_layers: int = 1, num_heads: int = 1,
				 out_features: int = 2, rnn=nn.GRU, drop_out: float = 0.0):
		"""
		:param embed_dim: RNN的input_size，word embedding维度
		:param hidden_size: RNN的hidden_size, RNN隐藏层维度
		:param num_layers: RNN的num_layers, RNN层数
		:param num_layers: RNN的num_layers, RNN层数
		:param num_heads: 抽头数
		:param rnn: 所用的RNN模型：GRU和LSTM，默认是GRU
		:param drop_out：
		"""

		super().__init__()
		self.rnn = rnn(input_size=embed_dim, hidden_size=hidden_size, num_layers=num_layers, bidirectional=True,
					   batch_first=True)
		self.attention = MultiHeadClassifySelfAttention(hidden_size * 2, num_heads)

		# 定义全连接层
		self.fc = nn.Linear(hidden_size * 2 * num_heads, out_features)
		if 0.0 < drop_out < 1.0:
			self.fc = nn.Sequential(
				nn.Dropout(drop_out),
				self.fc
			)

	def forward(self, inputs, labels=None):
		output, _ = self.rnn(inputs)
		output = self.attention(output)
		logits = self.fc(output)
		if labels is None:
			return logits

		loss = F.cross_entropy(logits, labels)
		return loss, logits
