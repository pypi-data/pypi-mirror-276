import torch
from pathlib import Path
from typing import Union, Iterable
from torch.nn import Embedding

from ._utils import UTF8, read_file, read_corpus_files, batch_cut, token_counter, batch_pad_mask, cut, batch_pad, pad,\
    pad_mask, load_embedding


# -------------------------------------------------Tokenizer class-----------------------------------------------------
class BaseTokenizer:
    """
    encode返回的是 list
    """
    SAVE_SEP = '|'
    PAD, UNK, BOS, EOS, SEP = '<pad>', '<unk>', '<bos>', '<eos>', '<sep>'
    BACKUP_TOKENS = [PAD, UNK, BOS, EOS, SEP]

    def __init__(self, file: str = None, corpus: Iterable[str] = None, cut_corpus: Iterable[Iterable[str]] = None, vocab: Iterable[str] = None,
            min_frequency=0, reserved_token=[], language='cn', cut_type='word', word_frequency=False):
        """
        :param file: 语料文件，可以是文件也可以是文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
        :param corpus: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
        :param cut_corpus: 语料，每个元素是是分词后的一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
        :param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
        :param min_frequency: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
        :param reserved_token: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param word_frequency: 是否统计词频
        """
        self.language = language
        self.cut_type = cut_type
        self.reserved_token = self.BACKUP_TOKENS + [token for token in reserved_token if token not in self.BACKUP_TOKENS]
        if vocab is not None:
            for token in [token for token in self.reserved_token if token in vocab]:
                vocab.remove(token)
            self.vocab = self.reserved_token + vocab
            self.token_to_idx = {k: i for i, k in enumerate(self.vocab)}
        else:
            if file is not None and corpus is None:
                corpus = read_corpus_files(file)
            if corpus is not None:
                cut_corpus = batch_cut(corpus, language=language, cut_type=cut_type, keep_punctuation=True)
            if cut_corpus is not None:
                counter = token_counter(cut_corpus)
                sorted_token_frequency = sorted(counter.items(), key=lambda kv: kv[1], reverse=True)
                self.vocab = self.reserved_token.copy()
                self.vocab += [token for token, freq in sorted_token_frequency if freq >= min_frequency and token not in self.vocab]
                self.token_to_idx = {k: i for i, k in enumerate(self.vocab)}
                if word_frequency:
                    self.word_frequency = [(self.token_to_idx[token], freq) for token, freq in sorted_token_frequency if
                                           token not in self.reserved_token]
            else:
                raise ValueError('参数file, corpus, vocab不能同时为None.')
        self.vocab_size = len(self.vocab)
        self.pad, self.unk, self.bos, self.eos, self.sep = [self.token_to_idx[token] for token in self.BACKUP_TOKENS]

    def encode(self, sentence: str, max_length: int = None, truncation=True, padding=True, padding_side='right',
            pad_begin_end=False, keep_punctuation=False, is_split_into_words: bool = False):
        """
        :param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了'
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :param keep_punctuation: 是否保留标点符号
        :param is_split_into_words: 是否已经分词
        :return:
        """
        if isinstance(sentence, str):
            if is_split_into_words:
                tokens = self.do_encode(sentence)
            else:
                tokens = cut(sentence, self.language, self.cut_type, keep_punctuation=keep_punctuation)
                tokens = self.do_encode(tokens)
            return self.padding(tokens, max_length, truncation, padding, padding_side, pad_begin_end)

        raise ValueError('参数"sentence"类型错误')

    def batch_encode(self, sentences: Union[Iterable[str], Iterable[Iterable]], max_length: int = None, truncation=True, padding=True, padding_side='right',
            pad_begin_end=False, keep_punctuation=False, is_split_into_words: bool = False):
        """
        :param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :param keep_punctuation: 是否保留标点符号
        :param is_split_into_words: 是否已经分词
        :return:
        """
        if isinstance(sentences, Iterable):
            if is_split_into_words:
                tokens = map(self.do_encode, sentences)
            else:
                batch_cuts = batch_cut(sentences, language=self.language, cut_type=self.cut_type, keep_punctuation=keep_punctuation)
                tokens = map(self.do_encode, batch_cuts)
            return self.padding(tokens, max_length, truncation, padding, padding_side, pad_begin_end)

        raise ValueError('参数"sentence"类型错误')

    def do_encode(self, cut_tokens: Union[str, Iterable[str]]):
        """
        把词转换成数字
        :param cut_tokens: '学生' 或 ['学生', '手机', '老师']
        :return:
        """
        if isinstance(cut_tokens, str):
            return self.token_to_idx.get(cut_tokens, self.unk)
        return list(map(self.do_encode, cut_tokens))

    def decode(self, tokens: Iterable[int], return_special_tokens=False, return_sentence=False):
        """
        :param tokens: [2, 19, 27, 3, 0, 0]
        :param return_special_tokens: 是否返回'<pad>', '<unk>', '<bos>', '<eos>'等特殊字符
        :param return_sentence: 返回的是一句话还是词序列
        :return: 由return_sentence决定，返回的是 '上课时学生手机响个不停‘, 还是 ['上课', '时', '学生', '手机', ’响个, '不停']
        """
        return [self.decode(index, return_special_tokens, return_sentence) for index in tokens]

    def batch_decode(self, tokens: Iterable[Iterable[int]], return_special_tokens=False, return_sentence=False):
        """
        :param tokens: [[2, 19, 27, 3, 0, 0], [2, 10, 3, 0, 0, 0]]
        :param return_special_tokens: 是否返回'<pad>', '<unk>', '<bos>', '<eos>'等特殊字符
        :param return_sentence: 返回的是一句话还是词序列
        :return: 由return_sentence决定，返回的是 '上课时学生手机响个不停‘, 还是 ['上课', '时', '学生', '手机', ’响个, '不停']
        """
        return [self.decode(index, return_special_tokens, return_sentence) for index in tokens]

    def padding(self, tokens: Union[map, Iterable[int], Iterable[Iterable[int]]], max_length: int, truncation=True, padding=True,
            padding_side='right', pad_begin_end=False):
        """
        :param tokens: [2, 19, 27, 3] 或 [[2, 19, 27, 3], [2, 10, 3]]
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :return:
        """
        if isinstance(tokens, map) or isinstance(tokens[0], Iterable):
            return batch_pad(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)
        return pad(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)

    def get_real_vocab(self):
        """
        :return: 除去特殊字符的词表
        """
        return self.vocab[len(self.reserved_token):]

    def save(self, path='vocab.txt', encoding=UTF8):
        with open(path, 'w', encoding=encoding) as f:
            f.write(self.SAVE_SEP.join([self.language, self.cut_type]) + '\n')
            f.write(self.SAVE_SEP.join(self.reserved_token) + '\n')
            f.write(self.SAVE_SEP.join(self.vocab))

    @classmethod
    def load(cls, path='vocab.txt', encoding=UTF8):
        with open(path, encoding=encoding) as f:
            lines = f.readlines()
        language, cut_type = lines[0].strip().split(Tokenizer.SAVE_SEP)
        return cls(vocab=lines[2].strip().split(Tokenizer.SAVE_SEP), reserved_token=lines[1].strip().split(Tokenizer.SAVE_SEP),
                        language=language, cut_type=cut_type)

    @classmethod
    def from_file(cls, file: str, encoding=UTF8, pattern='*', func=read_file, min_frequency=0, reserved_token=[], language='cn', cut_type='word',
            word_frequency=False):
        """
        :param file: 语料文件，可以是文件也可以是文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
        :param encoding: 编码
        :param pattern: 文件后缀，当file是文件夹的时候，会根据此后缀过滤文件
        :param func: 具体读取文件的处理函数，默认是read_file，可替换。注意：其函数签名为 function_name(path: str, encoding: str) -> corpus: Iterable[str]
        :param min_frequency: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
        :param reserved_token: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param word_frequency: 是否统计词频
        """
        corpus = read_corpus_files(file, encoding, pattern, func)
        return cls(corpus=corpus, min_frequency=min_frequency, reserved_token=reserved_token, language=language, cut_type=cut_type,
                        word_frequency=word_frequency)

    @classmethod
    def from_corpus(cls, corpus: Iterable[str], min_frequency=0, reserved_token=[], language='cn', cut_type='word', word_frequency=False):
        """
        :param corpus: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
        :param min_frequency: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
        :param reserved_token: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param word_frequency: 是否统计词频
        """
        return cls(corpus=corpus, min_frequency=min_frequency, reserved_token=reserved_token, language=language, cut_type=cut_type,
                        word_frequency=word_frequency)

    @classmethod
    def from_cut_corpus(cls, cut_corpus: Iterable[Iterable[str]], min_frequency=0, reserved_token=[], language='cn', cut_type='word', word_frequency=False):
        """
        :param cut_corpus: 分词后的语料，每个元素是一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
        :param min_frequency: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
        :param reserved_token: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param word_frequency: 是否统计词频
        """
        return cls(cut_corpus=cut_corpus, min_frequency=min_frequency, reserved_token=reserved_token, language=language, cut_type=cut_type,
                        word_frequency=word_frequency)

    @classmethod
    def from_vocab(cls, vocab: Iterable[str], reserved_token=[]):
        """
        :param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
        :param reserved_token: 保留token, 如 '<pad>', '<unk>'等
        """
        return cls(vocab=vocab, reserved_token=reserved_token)

    def _get_token(self, indices: Iterable[int], return_special_tokens):
        if return_special_tokens:
            return [self.vocab[i] for i in indices]
        return [self.vocab[i] for i in indices if i not in [self.pad, self.bos, self.eos, self.unk]]

    def __len__(self):
        return self.vocab_size

    def __getitem__(self, index):
        return self.vocab[index]

    # def __call__(self, sentence: Union[str, Iterable[str]], max_length: int = None, truncation=True, padding=True, padding_side='right',
    #         pad_begin_end=False, keep_punctuation=False):
    #     return self.encode(sentence, max_length, truncation, padding, padding_side, pad_begin_end, keep_punctuation)


class Tokenizer(BaseTokenizer):
    """
    encode返回的是 {'input_ids': list} 或 {'input_ids': list, 'mask_ids': list}
    """

    def __init__(self, file: str = None, corpus: Iterable[str] = None, cut_corpus: Iterable[Iterable[str]] = None, vocab: Iterable[str] = None,
            min_frequency=0, reserved_token=[], language='cn', cut_type='word', word_frequency=False):
        """
        :param file: 语料文件， 如：'./train.csv'
        :param corpus: 语料，每个元素是一句话，如：['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
        :param cut_corpus: 语料，每个元素是是分词后的一句话，如：[['上课', '时', '学生', '手机', '响', '个', '不停'], ['家长', '拿', '发票', '让', '老师', '赔']]
        :param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
        :param min_frequency: 最小词频，小于词词频的词会被忽略，默认是0，所有的词都保留
        :param reserved_token: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param word_frequency: 是否统计词频
        """
        super().__init__(file=file, corpus=corpus, cut_corpus=cut_corpus, vocab=vocab, min_frequency=min_frequency, reserved_token=reserved_token,
                         language=language, cut_type=cut_type, word_frequency=word_frequency)

    def encode_plus(self, sentence: Union[str, Iterable[str], Iterable[Iterable]], max_length: int = None, truncation=True, padding=True, padding_side='right',
            pad_begin_end=False, keep_punctuation=False, return_mask=False, is_split_into_words=False):
        """
        :param sentence: '上课时学生手机响个不停，老师一怒之下把手机摔了' 或 ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :param keep_punctuation: 是否保留标点符号
        :param return_mask: 是否返回 mask_ids
        :param is_split_into_words: 是否已经分词
        :return:
        """
        if isinstance(sentence, str):
            if is_split_into_words:
                tokens = self.do_encode(sentence)
            else:
                tokens = cut(sentence, self.language, self.cut_type, keep_punctuation=keep_punctuation)
                tokens = self.do_encode(tokens)
            return self.padding_plus(tokens, max_length, truncation, padding, padding_side, pad_begin_end, return_mask)

        raise ValueError('参数"sentence"类型错误')

    def batch_encode_plus(self, sentences: Union[str, Iterable[str], Iterable[Iterable]], max_length: int = None, truncation=True, padding=True, padding_side='right',
            pad_begin_end=False, keep_punctuation=False, return_mask=False, is_split_into_words=False):
        """
        :param sentences: ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ....]
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :param keep_punctuation: 是否保留标点符号
        :param return_mask: 是否返回 mask_ids
        :param is_split_into_words: 是否已经分词
        :return:
        """
        if isinstance(sentences, Iterable):
            if is_split_into_words:
                tokens = map(self.do_encode, sentences)
            else:
                batch_cuts = batch_cut(sentences, language=self.language, cut_type=self.cut_type, keep_punctuation=keep_punctuation)
                tokens = map(self.do_encode, batch_cuts)
            return self.padding_plus(tokens, max_length, truncation, padding, padding_side, pad_begin_end, return_mask)

        raise ValueError('参数"sentence"类型错误')


    def padding_plus(self, tokens: Union[map, Iterable[int], Iterable[Iterable[int]]], max_length: int, truncation=True, padding=True,
            padding_side='right', pad_begin_end=False, return_mask=False):
        """
        :param tokens: [2, 19, 27, 3] 或 [[2, 19, 27, 3], [2, 10, 3]]
        :param max_length:
        :param truncation:
        :param padding:
        :param padding_side:
        :param pad_begin_end:
        :return:
        """
        if isinstance(tokens, map) or isinstance(tokens[0], Iterable):
            if return_mask:
                return batch_pad_mask(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)
            return {'input_ids': batch_pad(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)}

        if return_mask:
            return pad_mask(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)
        return {'input_ids': pad(tokens, max_length, truncation, padding, padding_side, pad_begin_end, self.pad, self.bos, self.eos)}

    def __call__(self, sentence: Union[str, Iterable[str]], max_length: int = None, truncation=True, padding=True, padding_side='right',
            pad_begin_end=False, keep_punctuation=False, return_mask=False):
        return self.encode(sentence, max_length, truncation, padding, padding_side, pad_begin_end, keep_punctuation, return_mask)


class TokenEmbedding(Tokenizer):
    """
    可以传入已经训练好的embedding文件路径，也可以embedding数据, encode返回的是 {'input_ids': list} 或 {'input_ids': list, 'mask_ids': list}
    """

    def __init__(self, file: str = None, vocab: Iterable[str] = None, embedding: Iterable[Iterable[float]] = None, reserved_token=[],
            language='cn', cut_type='word', func=load_embedding, is_large_file=False):
        """
        :param file: embedding文件， 如：'./sgns.weibo.word.bz2'
        :param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']，与embedding必须同时传入
        :param embedding: [[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578]]与vocab必须同时传入
        :param reserved_token: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        :param func: 具体读取文件的处理函数，load_embedding，可替换。
               注意：其函数签名为 function_name(path: str, is_large_file: bool) -> (vocab: list[str], embedding: list[list[float]])
        :param is_large_file: 是否是大文件
        """
        if file:
            assert Path(file).is_file(), 'file必须是具体文件,不能是文件夹'
            vocab, embedding = func(file, is_large_file)
        elif not vocab or not embedding:
            raise ValueError('参数"path"为空的情况下，"vocab"和"embedding"不能为空.')
        super().__init__(vocab=vocab, reserved_token=reserved_token, language=language, cut_type=cut_type)
        reserved_token = self.reserved_token.copy()
        reserved_token.reverse()
        self.dim = len(embedding[0])
        for token in reserved_token:
            embedding = [[self.do_encode(token)] * self.dim] + embedding
        self.embedding = Embedding.from_pretrained(torch.tensor(embedding, dtype=torch.float))

    def __call__(self, sentence: Union[str, Iterable[str], Iterable[Iterable]], max_length: int = None):
        input_ids = self.batch_encode(sentence, max_length)
        return self.encode(torch.tensor(input_ids, dtype=torch.long))

    @classmethod
    def from_file(cls, file: str, func=load_embedding, is_large_file=False, reserved_token=[], language='cn', cut_type='word'):
        """
        :param file: embedding文件， 如：'./sgns.weibo.word.bz2'. 注意：必须是单一文件，不能是文件夹。
        :param func: 具体读取文件的处理函数，load_embedding，可替换。注意：其函数签名为 function_name(path: str, is_large_file: bool) -> [vocab], [[embedding]]
        :param is_large_file: 是否是大文件
        :param reserved_token: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        """
        return cls(file=file, reserved_token=reserved_token, language=language, cut_type=cut_type, func=func, is_large_file=is_large_file)

    @classmethod
    def from_vocab_embedding(cls, vocab: Iterable[str], embedding: Iterable[Iterable[float]], large_file=False, reserved_token=[], language='cn',
            cut_type='word'):
        """
        :param vocab: 词表，如：['上课', '学生', '手机', '不停', '，', '老师']
        :param embedding: [[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578],[0.2548, -0.6879, 0.2578]]
        :param large_file: 是否是大文件
        :param reserved_token: 保留token, 如 '<pad>', '<unk>'等
        :param language: 语言 'cn'和'en'
        :param cut_type: 分词类型，只支持'word'和‘char'两种类型
        """
        return cls(vocab=vocab, embedding=embedding, large_file=large_file, reserved_token=reserved_token, language=language, cut_type=cut_type)


if __name__ == '__main__':
    # file_name = './article.txt'
    # text = read_file(file_name)

    import pandas as pd
    import matplotlib.pyplot as plt

    DATA_PATH = r'D:\Study\kkb\代码实战课\week1\toutiao-text-classify\dataset\train.csv'
    # df = pd.read_csv(DATA_PATH)  # ['label']  ['sentence']

    # show_label_category_count(df['label'])
    # show_sentence_len_hist(df['sentence'], language='cn', cut_type='word', bins=50, scope=(0, 30))
    # show_token_frequency_plot(df['sentence'], language='cn', cut_type='word', scope=(0, 8000))

    # tokenizer = Tokenizer(corpus=df['sentence'].values, min_frequency=10, language='cn', cut_type='word')
    # tokenizer = BaseTokenizer.from_corpus(df['sentence'].values)
    # tokenizer.save()

    # sent = ('上课时学生手机响个不停，老师一怒之下把手机摔了，家长拿发票让老师赔，大家怎么看待这种事？', '老师一怒之下把手机摔了')
    # tokenizer = BaseTokenizer.load()
    # d = tokenizer.encode(sent, max_length=30, keep_punctuation=True, pad_begin_end=True)
    # print(d)
    # print(tokenizer.decode(d, return_special_tokens=False, return_sentence=True))
    # tokenizer = Tokenizer.load()
    # # print(type(tokenizer))
    # # # print(len(tokenizer))
    # # # print(tokenizer.vocab[:20])
    # # # print(tokenizer.reserved_token)
    # # # print(tokenizer.encode(['the', 'my']))
    # #
    # print(tokenizer.vocab[:20])
    # print(sent)
    # e = tokenizer(sent, max_length=30, keep_punctuation=True, pad_begin_end=True)
    # print(e)
    # d = tokenizer.decode(e)
    # print(d)

    # print(tokenizer.decode(d['input_ids'], return_special_tokens=False, return_sentence=True))
    # print(tokenizer.decode(d['input_ids']))

    # tk = [[101, 2198, 5125, 3198, 7313, 4764, 3221, 4507, 102, 7313, 4764, 3221, 4507, 102, 4764, 3221],
    #       [101, 2198, 5125, 3198, 7313, 4764, 3221, 4507, 102]]
    # r = tokenizer.padding(tk, max_length=15, truncation=True, padding_side='right', pad_begin_end=True)
    # print(r)

    # PATH = r'D:\Study\kkb\代码实战课\week1\toutiao-text-classify\dataset\sgns.weibo.word.bz2'
    # tokenizer = TokenEmbedding(PATH)
    # tokenizer = TokenEmbedding.from_file(PATH, is_large_file=False)
    # d = tokenizer.encode(sent, max_length=30, keep_punctuation=True, pad_begin_end=True)
    # print(d)
    # print(tokenizer.decode(d['input_ids'], return_special_tokens=False, return_sentence=True))
    # print(tokenizer.decode(d['input_ids']))
    #
    # tk = [[101, 2198, 5125, 3198, 7313, 4764, 3221, 4507, 102, 7313, 4764, 3221, 4507, 102, 4764, 3221],
    #       [101, 2198, 5125, 3198, 7313, 4764, 3221, 4507, 102]]
    # r = tokenizer.padding(tk, max_length=15, truncation=True, padding_side='right', pad_begin_end=True)
    # print(r)

    # print(batch_pad_mask(tk))

    # tokenizer = BaseTokenizer.from_file('./', pattern='*.txt', language='en')
    # print(tokenizer.vocab)

    # for f in get_files(r'D:\tmp'):
    #     print(f)

    # for line in read_large_file('./article.txt'):
    #     print(line)

