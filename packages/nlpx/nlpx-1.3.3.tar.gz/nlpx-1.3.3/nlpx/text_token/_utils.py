import re
import operator
from pathlib import Path
from functools import reduce
from typing import List, Union, Iterable

UTF8 = 'utf-8'
REMOVE_CHARS = '[·’!"\#$%&\'()＃！（）*+,-./:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~]+'


def get_texts_max_length(texts: List[str], language='cn', cut_type='word', keep_punctuation=False) -> int:
    batch_cuts = batch_cut(texts, language, cut_type, keep_punctuation)
    return max(list(map(lambda s: len(s), batch_cuts)))


# -----------------------------------------------------------Read file-------------------------------------------------
def read_file(path: str, encoding=UTF8):
    """
    读取文件内容
    :param path: 文件名，不能是文件夹
    :param encoding: 编码
    :return: 包含非空文本行的生成器，如 ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
    """
    # if Path(path).stat().st_size <= 10000: #1048576000: # 小于等于1G
    with open(path, encoding=encoding) as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]


def read_large_file(path: str, encoding=UTF8):
    with open(path, encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if line:
                yield line


async def async_read_file(path: str, encoding=UTF8):
    return read_file(path, encoding)


def read_corpus_files(path: str, encoding=UTF8, pattern='*', func=read_file, async_func=async_read_file):
    """
    读取文件或文件夹下所有符合条件的文件
    :param path: 文件或文件夹， 如：'./train.txt'. 如果是文件夹，会读取文件夹下的所有目录和文件.
    :param encoding: 编码
    :param suffix: 文件后缀，当path是文件夹的时候，会根据此后缀过滤文件
    :param func: 具体读取文件的读函数，默认是read_file，可替换。注意：其函数签名为 function_name(path: str, encoding: str) -> corpus: Iterable[str]
    :param async_func: 传入文件夹时的读函数，用协程读取每个文件，默认是async_read_file，可替换。注意：其函数签名为 async function_name(path: str, encoding: str) -> corpus: Iterable[str]
    :return: 非空文本行，如 ['上课时学生手机响个不停，老师一怒之下把手机摔了。', '家长拿发票让老师赔', ...]
    """
    path = Path(path)
    if path.is_file():
        return func(path, encoding)

    import asyncio
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(async_func(file, encoding)) for file in path.rglob(pattern)]  # 这里不能用map，否则读不出数据
    wait_coro = asyncio.wait(tasks)
    loop.run_until_complete(wait_coro)
    all_lines = (task.result() for task in tasks)
    loop.close()

    return reduce(operator.iconcat, all_lines, [])


def load_embedding(path: str, is_large_file=False):
    if path.endswith('.bz2'):
        return load_embedding_from_bz2(path, is_large_file)
    return load_embedding_nomal(path, is_large_file)


def load_embedding_from_bz2(path: str, is_large_file=False):
    import bz2
    if is_large_file:
        with bz2.open(path, 'r') as f:
            tokens, vecs = _get_token_vecs(f, require_decode_token=True)
        return list(tokens), list(vecs)

    with bz2.open(path, 'r') as f:
        lines = f.readlines()
    return _handle_lines(lines, require_decode_token=True)


def load_embedding_nomal(path: str, is_large_file=False):
    if is_large_file:
        with open(path, 'r', encoding=UTF8) as f:
            tokens, vecs = _get_token_vecs(f, require_decode_token=False)
        return list(tokens), list(vecs)

    with open(path, 'r', encoding=UTF8) as f:
        lines = f.readlines()
    return _handle_lines(lines, require_decode_token=False)


def _get_token_vecs(f, require_decode_token):
    token_vec = (_handle_line(line, require_decode_token) for line in f if len(line.rstrip().split()) > 2)
    return zip(*token_vec)


def _handle_lines(lines: Iterable[str], require_decode_token: bool):
    if len(lines[0].split()) <= 2:
        lines = lines[1:]
    token_vec = list(map(lambda line: _handle_line(line, require_decode_token), lines))
    tokens, vecs = zip(*token_vec)
    return list(tokens), list(vecs)


def _handle_line(line: str, require_decode_token: bool):
    def get_vec(elems):
        return list(map(float, elems))

    elems = line.rstrip().split()
    return elems[0].decode(UTF8) if require_decode_token else elems[0], get_vec(elems[1:])


# --------------------------------------------------Token cut----------------------------------------------------------
def cut_char(sentence: str):
    """
    把句子按字分开，不破坏英文结构
    """
    # 首先分割 英文 以及英文和标点
    pattern_char_1 = re.compile(r'([\W])')
    parts = pattern_char_1.split(sentence)
    parts = [p for p in parts if len(p.strip()) > 0]
    # 分割中文
    pattern = re.compile(r'([\u4e00-\u9fa5])')
    chars = pattern.split(sentence)
    return [w for w in chars if len(w.strip()) > 0]


def batch_cut(text: Iterable[str], language='cn', cut_type='word', keep_punctuation=False):
    """
    多句话批量分词
    :param text: 多句话，即多行
    :param language: 哪国语言，支持cn和en
    :param cut_type: 按词还是字分，支持word和char
    :param keep_punctuation: 是否保留标点符号
    :return: 分词后的list(2维)
    """
    import re
    if language == 'cn':
        import jieba
        replace_char = ''
        if cut_type == 'word':
            if keep_punctuation:
                def fn(s):
                    return jieba.cut(s.strip())
            else:
                def fn(s):
                    return jieba.cut(re.sub(REMOVE_CHARS, replace_char, s.strip()))
        else:
            if keep_punctuation:
                def fn(s):
                    return cut_char(s.strip())
            else:
                def fn(s):
                    return cut_char(re.sub(REMOVE_CHARS, replace_char, s.strip()))
        return map(fn, text)
        # return [cut_char(re.sub(REMOVE_CHARS, '', line.strip())) for line in text]

    if language == 'en':
        replace_char = ' '
        if cut_type == 'word':
            def fn(s):
                return re.sub(REMOVE_CHARS, replace_char, s).strip().lower().split()
        else:
            if keep_punctuation:
                def fn(s):
                    return list(s.strip().lower())
            else:
                def fn(s):
                    return list(re.sub('[^A-Za-z]+', replace_char, s).strip().lower())
        return map(fn, text)
        # return [fn(line) for line in text]

    raise NotImplementedError(f'暂时未实现"{language}"的分词功能')


def cut(sentence: str, language='cn', cut_type='word', keep_punctuation=False):
    """
    单句话分词
    :param sentence: 单句话，即一行
    :param language: 哪国语言，支持cn和en
    :param cut_type: 按词还是字分，支持word和char
    :param keep_punctuation: 是否保留标点符号
    :return: 分词后的list(1维)
    """
    import re
    if language == 'cn':
        import jieba
        replace_char = ''
        if cut_type == 'word':
            if keep_punctuation:
                return list(jieba.cut(sentence.strip()))
            else:
                return list(jieba.cut(re.sub(REMOVE_CHARS, replace_char, sentence.strip())))
        else:
            if keep_punctuation:
                return cut_char(sentence.strip())
            else:
                return cut_char(re.sub(REMOVE_CHARS, replace_char, sentence.strip()))

    if language == 'en':
        replace_char = ' '
        if cut_type == 'word':
            return re.sub(REMOVE_CHARS, replace_char, sentence).strip().lower().split()
        else:
            if keep_punctuation:
                return list(sentence.strip().lower())
            else:
                return list(re.sub('[^A-Za-z]+', replace_char, sentence).strip().lower())

    raise NotImplementedError(f'暂时未实现"{language}"的分词功能')


# --------------------------------------------------Token counter------------------------------------------------------
def token_counter(cut_corpus: Union[map, Iterable[str], Iterable[Iterable[str]]]):
    """
    统计词频
    :param cut_corpus: 分词后的语料
    :return: collections.Counter, 可以用items()方法取出[tuple(word, count)]
    """
    from collections import Counter
    if isinstance(cut_corpus, map) or (isinstance(cut_corpus, Iterable) and isinstance(cut_corpus[0], Iterable)):
        # return Counter([token for line in batch_cut for token in line])
        return Counter(reduce(operator.iconcat, cut_corpus, []))
    elif isinstance(cut_corpus, Iterable) and isinstance(cut_corpus[0], str):
        return Counter(cut_corpus)
    raise TypeError("'cut_corpus'参数类型不对")


# -----------------------------------------------------Text analysis----------------------------------------------
def show_label_category_count(labels):
    """
    :param corpus: 语料，可以是Iterable[str], Iterable[Iterable[str]], pandas的Series[str]
    :return: labels, label_count
    """
    import sys
    import pandas as pd
    import matplotlib.pyplot as plt
    if isinstance(labels, pd.Series):
        label_count = labels.value_counts(sort=False)
        label_count.plot(kind='bar')
        labels = labels.unique()
        min_count, max_count = label_count.min(), label_count.max()
    else:
        from collections import Counter
        label_count = Counter(labels)

        labels, counts = [], []
        min_count, max_count = sys.maxsize, 0
        for label, count in label_count.items():
            labels.append(label)
            counts.append(count)
            min_count = count if min_count > count else min_count
            max_count = count if max_count < count else max_count

        plt.bar(labels, counts, width=0.5)
        plt.xticks(ticks=labels, rotation=60)

    print(f'最大值: {max_count}，最小值: {min_count}，相差{max_count / min_count:.0f}倍')
    plt.show()
    return labels, label_count


def show_sentence_len_hist(corpus, language='cn', cut_type='word', bins=50, scope: tuple = None):
    """
    :param corpus: 语料，可以是Iterable[str], Iterable[Iterable[str]], pandas的Series[str]
    :param language:
    :param cut_type:
    :param bins:
    :param scope:
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    if isinstance(corpus, pd.Series):
        sent_length = corpus.map(lambda x: len(cut(x, language, cut_type)))
        sent_length.hist(bins=bins)
    else:
        batch_cuts = batch_cut(corpus, language, cut_type)
        length = list(map(lambda s: len(s), batch_cuts))
        if scope:
            length = [x for x in length if scope[0] <= x <= scope[1]]
        print(f'最短的句子是{min(length)}，最长为{max(length)}')
        plt.hist(length, bins=bins)
    plt.xlabel('sentence length')
    plt.ylabel('sentence count')
    plt.grid()
    plt.show()


def show_token_frequency_plot(corpus, language='cn', cut_type='word', scope: tuple = None):
    """
    :param corpus: 语料，可以是Iterable[str], Iterable[Iterable[str]], pandas的Series[str]
    :param language:
    :param cut_type:
    :param scope:
    """
    import math
    import pandas as pd
    import matplotlib.pyplot as plt
    show_num = 10
    batch_cuts = batch_cut(corpus, language, cut_type)
    counter = token_counter(batch_cuts)
    sorted_token_count = sorted(counter.items(), key=lambda kv: kv[1], reverse=True)
    print(f'出现频率最大的{show_num}个token:\n {sorted_token_count[:show_num]}')
    print(f'出现频率最小的{show_num}个token:\n {sorted_token_count[-show_num:]}')
    if scope is not None:
        sorted_token_count = sorted_token_count[scope[0]:scope[1]]

    sorted_count = list(map(lambda kv: kv[1], sorted_token_count))

    # sorted_count = sorted(counter.values(), reverse=True)
    # if scope is not None:
    #     token_count = sorted_count[scope[0]:scope[1]]

    plt.plot(list(map(lambda n: math.log(n), sorted_count)))
    # plt.plot(sorted_count, scalex='log', scaley='log')
    plt.xlabel('token:x')
    plt.ylabel('frequency:log(x)')
    plt.show()


# -------------------------------------------------pad function--------------------------------------------------------
def _pad(tokens: Iterable[int], max_length: int = None, truncation=True, padding=True, padding_side='right', pad_begin_end=False,
        pad_value=0, bos_value=1, eos_value=2):
    """
    pad token list(1维)
    :return: padded list, valid_size size
    """
    assert padding_side in ('right', 'left'), '参数padding_side只能是"right"或"left".'
    size = len(tokens)
    if pad_begin_end:
        size += 2
        if max_length and truncation and size > max_length:
            return [bos_value] + tokens[:max_length - 2] + [eos_value], max_length
        if max_length and padding and size < max_length:
            if padding_side == 'right':
                return [bos_value] + tokens + [eos_value] + [pad_value] * (max_length - size), size
            elif padding_side == 'left':
                return [pad_value] * (max_length - size) + [bos_value] + tokens + [eos_value], size
            raise ValueError(f'参数"padding_side"错误: {padding_side}')
        return [bos_value] + tokens + [eos_value], size
    else:
        if max_length and truncation and size > max_length:
            return tokens[:max_length], max_length
        if max_length and padding and size < max_length:
            if padding_side == 'right':
                return tokens + [pad_value] * (max_length - size), size
            elif padding_side == 'left':
                return [pad_value] * (max_length - size) + tokens, size
            raise ValueError(f'参数"padding_side"错误: {padding_side}')
        return tokens, size


def pad(tokens: Iterable[int], max_length: int = None, truncation=True, padding=True, padding_side='right', pad_begin_end=False,
        pad_value=0, bos_value=1, eos_value=2):
    """
    :param tokens: (1维)
    :param max_length:
    :param truncation:
    :param padding:
    :param padding_side:
    :param pad_begin_end:
    :param pad_value:
    :param bos_value:
    :param eos_value:
    :return: padded list
    """
    return _pad(tokens, max_length, truncation, padding, padding_side, pad_begin_end, pad_value, bos_value, eos_value)[0]


def batch_pad(batch: Union[map, Iterable[Iterable[int]]], max_length: int = None, truncation=True, padding=True, padding_side='right',
        pad_begin_end=False, pad_value=0, bos_value=1, eos_value=2):
    """
    :param batch: (2维)
    :return:
    """
    if not max_length:
        max_length = max(len(item) for item in batch)
    return list(map(lambda tokens: pad(tokens, max_length, truncation, padding, padding_side, pad_begin_end, pad_value, bos_value, eos_value), batch))


def _pad_mask(tokens: Iterable[int], max_length: int = None, truncation=True, padding=True, padding_side='right', pad_begin_end=False,
        pad_value=0, bos_value=1, eos_value=2):
    input_ids, real_size = _pad(tokens, max_length, truncation, padding, padding_side, pad_begin_end, pad_value, bos_value, eos_value)
    size = len(input_ids)
    if size > real_size:
        if padding_side == 'right':
            return input_ids, [1] * real_size + [0] * (size - real_size)
        return input_ids, [0] * (size - real_size) + [1] * real_size
    else:
        return input_ids, [1] * size


def pad_mask(tokens: Iterable[int], max_length: int = None, truncation=True, padding=True, padding_side='right', pad_begin_end=False,
        pad_value=0, bos_value=1, eos_value=2):
    input_ids, mask_ids = _pad_mask(tokens, max_length, truncation, padding, padding_side, pad_begin_end, pad_value, bos_value, eos_value)
    return {'input_ids': input_ids, 'mask_ids': mask_ids}


def batch_pad_mask(batch: Union[map, Iterable[Iterable[int]]], max_length: int = None, truncation=True, padding=True, padding_side='right',
        pad_begin_end=False, pad_value=0, bos_value=1, eos_value=2):
    if not max_length:
        max_length = max(len(item) for item in batch)
    ids = list(
        map(lambda tokens: _pad_mask(tokens, max_length, truncation, padding, padding_side, pad_begin_end, pad_value, bos_value, eos_value), batch))
    input_ids, mask_ids = zip(*ids)
    return {'input_ids': list(input_ids), 'mask_ids': list(mask_ids)}

