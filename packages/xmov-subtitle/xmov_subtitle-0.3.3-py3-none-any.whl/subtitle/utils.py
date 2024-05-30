import os
import regex as re

import unicodedata

CUR_DIR = os.path.dirname(__file__)
ENG_CHAR = re.compile(r"['-]?[a-zA-Z]")


def join_to_sent(words):
    sent = ""
    for i, word in enumerate(words):
        if word.startswith("##"):
            sent += word[2:]
            continue
        sep = decide_sep(words, i)
        sent += sep + word
    return sent


def decide_sep(words, idx):
    if idx > 0 and ENG_CHAR.match(words[idx][0]) and ENG_CHAR.match(words[idx - 1][-1]):
        return " "
    return ""


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_contains_number(tokens):
    # 检查是否含有数字
    if re.findall('[0-9]', tokens):
        return True
    return False


def is_contains_chinese(tokens):
    # 检查是否含有中文字符
    for token in tokens:
        if '\u4e00' <= token <= '\u9fa5':
            return True
    return False


def is_punctuation(char):
    """Checks whether `chars` is a punctuation character."""
    cp = ord(str(char))
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode
    # Punctuation class but we treat them as punctuation anyways, for
    # consistency.
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
            (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False


def is_all_punctuation(chars):
    for ch in chars:
        if not is_punctuation(ch):
            return False
    return True


def is_voiced_chars(ch):
    if is_contains_chinese(ch) or is_alphabet(ch) or is_contains_number(ch):
        return True
    return False


def split_text_by_regex(text, pattern, forbidden_position=None):
    if forbidden_position is None:
        forbidden_position = []

    sentences = []
    cursor = 0

    # 使用 finditer 查找所有匹配项
    matchers = list(re.finditer(pattern, text))

    new_matchers = []
    for match in matchers:
        match_flag = True
        for symbol_pair_start, symbol_pair_end in forbidden_position:
            if symbol_pair_start <= match.start() < symbol_pair_end:
                match_flag = False
                break
        if match_flag:
            new_matchers.append(match)

    if new_matchers:
        for matcher in new_matchers:
            # 检查是否有非空的文本在匹配项之前
            if matcher.start() >= cursor:
                sentences.append(text[cursor:matcher.end()])
            # 更新游标位置
            cursor = matcher.end()
        # 检查是否有非空的文本在最后一个匹配项之后
        if cursor < len(text):
            sentences.append(text[cursor:])
    else:
        sentences = [text, ]
    return sentences