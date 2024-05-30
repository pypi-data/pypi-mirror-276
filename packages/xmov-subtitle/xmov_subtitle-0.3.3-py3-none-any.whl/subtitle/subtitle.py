import sys

sys.path.append('..')
from .version import VERSION
import logging
import os
from typing import List

import jieba.posseg as pseg
import nltk
import regex as re
from nltk.tokenize import MWETokenizer

from .str_utils import Trie
from .utils import is_chinese, is_alphabet, split_text_by_regex, is_contains_chinese, is_all_punctuation

CUR_DIR = os.path.dirname(__file__)

logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 设置日志格式
    handlers=[
        logging.StreamHandler()  # 同时输出日志到控制台
    ]
)

logger = logging.getLogger(__name__)

# 合并规则
PRIORITY_0_MERGE_RULES = [
    ('v', 'p'),
    ('r', 'r'),
    ('r', 'n'),
    ('r', 'm'),
    ('r', 'q', 'n'),
    ('m', 'n'),
    ('m', 'q'),
    ('m', 'm'),
    ('a', 'n')
]

PRIORITY_1_MERGE_RULES = [
    ('n', 'n'),
    ('n', 'f'),
    ('r', 'v'),
    ('r', 'c'),
    ('v', 'm', 'q'),
    ('v', 'm'),
    ('v', 'q', 'n'),
    ('v', 'v'),
    ('v', 'r'),
    ('v', 'u', 'n'),
    ('a', 'u', 'n'),
    ('v', 'n'),
]

ENG_PRIORITY_0_MERGE_RULES = [
    ('VB', 'JJ', 'TO'),
    ('VB', 'VBN', 'TO'),
    ('NN', 'POS', 'NN'),
    ('PRP', 'NN'),
    ('PRP', 'JJ', 'NN'),
    ('DT', 'NN'),
    ('DT', 'NN', 'NN'),
    ('DT', 'CD', 'NN'),
    ('DT', 'JJ', 'NN'),
    ('DT', 'VBG', 'NN'),
    ('DT', 'VBN', 'NN'),
    ('CD', 'JJ', 'NN'),
    ('CD', 'VBG', 'NN'),
    ('CD', 'VBN', 'NN'),
    ('CD', 'NN', 'NN'),
    ('DT', 'JJS'),
    ('VN', 'IN'),
    ('PRP', 'VB'),
    ('CD', 'NN'),
    ('CD', 'CD'),
    ('CD', 'CD', 'NN'),
    ('RB', 'JJ'),
    ('JJ', 'NN'),
    ('VB', 'IN'),

]

ENG_PRIORITY_1_MERGE_RULES = [
    ('NN', 'NN'),
    ('VB', 'TO'),
    ('VB', 'TO', 'NN'),
    ('MD', 'VB'),

]


class SubtitleParser:
    def __init__(self, user_dict=None):
        self.trie = Trie()
        self.init_user_words(user_dict)

        self.text_mid_punc_pattern = r'[^。；;:：](?<![0-9一二三四五六七八九十])[，,]["” ]?'
        self.text_end_punc_pattern = r'([～~。？?！;；!…]+["”)）]?)'
        self.text_end_punc_pattern += r'|(?<![\d一二三四五六七八九十]{1}|Miss|Mr|Mrs|Dr|Ms)\.[\s\."”)）]*'

        self.symbol_pairs = {
            ')': '(',
            '）': '（',
            '}': '{',
            ']': '[',
            '》': '《',
            '】': '【',
            '>': '<',
            '〗': '〖',
            '』': '『',
            '」': '「',
            '”': '“',
            '’': '‘',

        }
        self.tokenizer = MWETokenizer(mwes=None, separator=' ')

    def init_user_words(self, user_dict):
        lines = []
        if user_dict:
            with open(user_dict, 'r', encoding='utf-8') as r:
                lines = r.readlines()
                lines = [line.strip() for line in lines]
        lines = list(set(lines))

        for token in lines:
            self.trie.add(token)

    def add_user_word(self, words: List[str]):
        """新增用户词表"""
        for word in words:
            self.trie.add(word)

        print(f'total add {len(words)} words')

    def update_user_word(self, words: List[str]):
        """删除用户词表"""
        self.trie.reset()
        self.add_user_word(words)

    def get_length(self, text):
        # 英文标点算半个字符，中文数字，算一个
        total = 0
        for token in text:
            if is_chinese(token):
                total += 1
            else:
                total += 0.5
        return total

    def combine_sub_sentences_by_comma(self, sentences_list, max_len):
        # 按照逗号合并短句
        outs = []
        sub_sentences = []
        for i, sentence in enumerate(sentences_list):
            if (sub_sentences and ''.join(sub_sentences)[-1] in ['，', ','] and
                    self.get_length(''.join(sub_sentences) + sentence) <= max_len):
                # 如果当前句子是逗号，下一句是短句<=8 < 上一句，则不合并
                if (
                        sentence and sentence[-1] in ['，', ','] and
                        i < len(sentences_list) - 1 and
                        self.get_length(sentences_list[i + 1]) <= 8 < self.get_length(sub_sentences[-1])
                ):
                    if sub_sentences:
                        outs.append(''.join(sub_sentences))
                        sub_sentences = []
                    sub_sentences.append(sentence)
                else:
                    sub_sentences.append(sentence)
            else:
                if sub_sentences:
                    outs.append(''.join(sub_sentences))
                    sub_sentences = []
                sub_sentences.append(sentence)
        if sub_sentences:
            outs.append(''.join(sub_sentences))
        return outs

    def combine_sub_sentences(self, sentences_list, max_len):
        outs = []
        sub_sentences = []
        for sentence in sentences_list:
            if self.get_length(''.join(sub_sentences) + sentence) <= max_len:
                sub_sentences.append(sentence)
            else:
                if sub_sentences:
                    outs.append(''.join(sub_sentences))
                    sub_sentences = []
                sub_sentences.append(sentence)
        if sub_sentences:
            outs.append(''.join(sub_sentences))
        return outs

    def split_text_by_symbol_pairs(self, text, symbol_pairs, max_len=24):
        # 《》【】[]等成对存在的符号，尽量不要切断
        rev_symbol_pairs = {v: k for k, v in symbol_pairs.items()}
        stack = []
        sub_texts = []
        i = 0
        while i < len(text):
            char = text[i]
            if char in symbol_pairs:
                if stack and stack[0] == symbol_pairs[char]:
                    stack.append(char)
                    cur_stack = ''.join(stack)
                    if self.get_length(cur_stack) > max_len and self.find_symbol_pairs(cur_stack):
                        sub_texts.append(cur_stack[0])
                        i -= (len(cur_stack) - 1)
                    else:
                        sub_texts.append(cur_stack)
                    stack = []
                else:
                    stack.append(char)
            elif (char in symbol_pairs.values() and stack and
                  stack[0] not in symbol_pairs.values() and rev_symbol_pairs.get(char) in text[i:]):
                sub_texts.append(''.join(stack))
                stack = []
                stack.append(char)
            else:
                stack.append(char)
            i += 1
        if stack:
            sub_texts.append(''.join(stack))

        if not sub_texts:
            return [text]
        return sub_texts

    def find_symbol_pairs(self, text):
        # 《》【】[]等成对存在的符号，尽量不要切断
        stack = []
        symbol_pair_index = []
        for i, char in enumerate(text):
            if char in self.symbol_pairs:
                if stack and stack[0] == self.symbol_pairs[char]:
                    stack.append(char)
                    cur_symbol_pair = ''.join(stack)
                    symbol_pair_index.append((cur_symbol_pair, i - len(cur_symbol_pair) + 1, i + 1))
                    stack = []
                else:
                    stack.append(char)
            elif (char in self.symbol_pairs.values() and stack and
                  stack[0] not in self.symbol_pairs.values()):
                stack = []
                stack.append(char)
            else:
                stack.append(char)

        if stack and stack[0] == self.symbol_pairs.get(char, None):
            cur_symbol_pair = ''.join(stack)
            symbol_pair_index.append((cur_symbol_pair, i - len(cur_symbol_pair) + 1, i + 1))
        return symbol_pair_index

    def merge_eng_seg(self, word_list, max_len):
        new_word_list = []
        for i, (word, pos) in enumerate(word_list):
            if not new_word_list:
                new_word_list.append((word, pos, pos))
                continue
            last_word, start_pos, end_pos = new_word_list[-1]

            # CC连词后面: and changed / the world.
            # IN后面: With just 3 simple steps
            if end_pos in ['CC', 'IN', 'RB'] and pos not in ['SYM', 'DT']:
                new_word = f'{last_word} {word}'
                if self.get_length(new_word) < max_len:
                    new_word_list[-1] = (new_word, start_pos, pos)
                else:
                    new_word_list.append((word, pos, pos))

            # 数词+名词+of: a pair of
            elif word == 'of' and i >= 2 and word_list[i - 1][1] == 'NN' and word_list[i - 2][1] == 'DT':
                new_word = f'{last_word} {word}'
                if self.get_length(new_word) < max_len:
                    new_word_list[-1] = (new_word, 'DT', pos)
                else:
                    new_word_list.append((word, pos, pos))
            else:
                new_word_list.append((word, pos, pos))
        word_list = new_word_list

        # 先合并第一优先级的词
        word_list = self.merge_seg(word_list, ENG_PRIORITY_0_MERGE_RULES, max_len, sep=' ')
        # 先合并第二优先级的词
        word_list = self.merge_seg(word_list, ENG_PRIORITY_1_MERGE_RULES, max_len, sep=' ')
        return word_list

    def merge_chinese_seg(self, word_list, max_len):
        new_word_list = []
        for i, (word, pos) in enumerate(word_list):
            if not new_word_list:
                new_word_list.append((word, pos, pos))
                continue
            last_word, start_pos, end_pos = new_word_list[-1]

            # u, p前面
            if pos in ['u', 'p']:
                new_word = f'{last_word}{word}'
                if self.get_length(new_word) < max_len:
                    new_word_list[-1] = (new_word, start_pos, pos)
                else:
                    new_word_list.append((word, pos, pos))

            # c, d, p, u后面
            elif end_pos in ['c', 'd', 'p', 'u'] and pos not in ['w', 'x']:
                new_word = f'{last_word}{word}'
                if self.get_length(new_word) < max_len:
                    new_word_list[-1] = (new_word, start_pos, pos)
                else:
                    new_word_list.append((word, pos, pos))
            else:
                new_word_list.append((word, pos, pos))
        word_list = new_word_list

        # 先合并第一优先级的词
        word_list = self.merge_seg(word_list, PRIORITY_0_MERGE_RULES, max_len)
        # 先合并第二优先级的词
        word_list = self.merge_seg(word_list, PRIORITY_1_MERGE_RULES, max_len)
        return word_list

    def merge_seg(self, word_list, merge_rules, max_len, sep=''):
        merged_list = []
        i = 0
        while i < len(word_list):
            word, start_pos, end_pos = word_list[i]
            merged = False
            for merges in merge_rules:
                merges_len = len(merges)
                # 从上一个词合并
                if merged_list and merged_list[-1][-1] == merges[0] and i + merges_len <= len(word_list):
                    next_pos = [merged_list[-1][2]] + [pos for _, pos, _ in word_list[i:i + merges_len - 1]]
                    next_word = [merged_list[-1][0]] + [word for word, _, _ in word_list[i:i + merges_len - 1]]
                    if tuple(next_pos) == merges:
                        if self.get_length(sep.join(next_word)) < max_len:
                            merged_list[-1] = [sep.join(next_word), merged_list[-1][1], merges[-1]]
                            i += len(merges) - 2
                            merged = True
                            break
                # 从当前词合并
                elif end_pos == merges[0] and i + merges_len <= len(word_list):
                    next_pos = [pos for _, pos, _ in word_list[i:i + merges_len]]
                    next_word = [word for word, _, _ in word_list[i:i + merges_len]]
                    if tuple(next_pos) == merges:
                        if self.get_length(sep.join(next_word)) < max_len:
                            merged_list.append([sep.join(next_word), merges[0], merges[-1]])
                            i += len(merges) - 1
                            merged = True
                            break
            if not merged:
                merged_list.append([word, start_pos, end_pos])
            i += 1
        return merged_list

    def norm_eng_word_seg(self, word_seg):
        normed_word_seg = []
        for i, (word, pos) in enumerate(word_seg):
            if pos.startswith('NN'):
                pos = 'NN'
            elif pos in ['VB', 'VBD', 'VBP', 'VBZ']:
                pos = 'V'
            elif pos.startswith('RB'):
                pos = 'RB'
            elif pos in ['DT', ' PDT', ' WDT']:
                pos = 'DT'
            elif pos.startswith('PRP'):
                pos = 'PRP'
            elif pos in ['JJ', ' JJR', ' JJS']:
                pos = 'JJ'
            normed_word_seg.append((word, pos))
        return normed_word_seg

    def norm_word_seg(self, word_seg):
        normed_word_seg = []
        skip = False
        for i, (word, pos) in enumerate(word_seg):
            if skip:
                skip = False
                continue
            if pos in ['n', 'ng', 'nr', 'nr', 'nrfg', 'nrt', 'ns', 'nt', 'nw', 'nx', 'nz', 'vn', 'an', 'j']:
                pos = 'n'
            elif pos in ['v', 'vg', 'vx']:
                pos = 'v'
            elif pos in ['a', 'ag', 'b', 'z']:
                pos = 'a'
            elif pos in ['r', 'rz']:
                pos = 'r'
            elif pos in ['d', 'dg', 'ad', 'vd']:
                pos = 'd'
            elif pos.startswith('u'):
                pos = 'u'

            last_word = normed_word_seg[-1][0] if normed_word_seg else ''
            next_word = word_seg[i + 1][0] if i < len(word_seg) - 1 else ''

            if word in ["'", "’", "-"]:
                if word != '-' and last_word.endswith('s'):
                    # example: sods' , lovers' clothes
                    normed_word_seg[-1] = (last_word + word, normed_word_seg[-1][1])
                    continue
                elif is_alphabet(last_word) and i < len(word_seg) - 1 and is_alphabet(next_word):
                    # example: i'm, a-b, cross-organization
                    normed_word_seg[-1] = (last_word + word + next_word, normed_word_seg[-1][1])
                    skip = True
                    continue
            normed_word_seg.append((word, pos))
        return normed_word_seg

    def tokenize_text(self, text, max_len, lang: str):
        raw_text = text
        # 字幕均匀分布
        avg_max_len = self.calculate_avg_max_len(text, max_len)

        # 匹配用户自定义词表
        user_words = list(set(self.trie.fmm(text)))
        symbol_pairs = [item[0] for item in self.find_symbol_pairs(text) if self.get_length(item[0]) <= max_len]
        user_words = [word for word in user_words for invalid_word in symbol_pairs if word not in invalid_word]
        text_list = [text]
        if user_words:
            user_word_pattern = '|'.join(user_words)
            text_list = re.split("(" + user_word_pattern + ")", text)

        word_segs = []
        for text in text_list:
            # 用户词表不切分
            if text and text in user_words and self.get_length(text) <= max_len:
                word_segs.append((text, ''))
                continue

            # 匹配成对的《》【】[]的内容, 在字幕中不可被隔断，除非其中的内容总字数超过单行字幕上限
            symbol_pairs_text_list = self.split_text_by_symbol_pairs(text, self.symbol_pairs, max_len)
            for sub_text in symbol_pairs_text_list:
                if (0 < self.get_length(sub_text) <= max_len
                        and self.symbol_pairs.get(sub_text[-1])):
                    word_segs.append((sub_text, ''))
                    continue
                # 分词，简化词性
                if lang == 'en':
                    # word_seg = nltk.word_tokenize(text)
                    word_seg = self.tokenizer.tokenize(sub_text.split(' '))
                    word_seg = nltk.pos_tag(word_seg)
                    word_seg: list = self.norm_eng_word_seg(word_seg)
                else:
                    word_seg = pseg.lcut(sub_text)
                    word_seg = [(w.word, w.flag) for w in word_seg]
                    word_seg: list = self.norm_word_seg(word_seg)
                word_segs.extend(word_seg)

        # 按照词性合并 不可切分的词
        if lang == 'en':
            word_segs = [(word, pos) if word.strip() != '' else (word, '') for word, pos in word_segs]
            word_segs = self.merge_eng_seg(word_segs, max_len)
            out_word_seg = []
            for i, item in enumerate(word_segs):
                out_word_seg.append(item)
                if item[0] and i != len(word_segs) - 1 and item[0] + ' ' in raw_text:
                    out_word_seg.append((' ', ' ', ' '))
            word_segs = out_word_seg
        else:
            word_segs = self.merge_chinese_seg(word_segs, max_len)

        # 合并短句
        sub_sentences = self.merge_word_seg(word_segs, avg_max_len, max_len)
        sub_sentences = self.combine_sub_sentences(sub_sentences, avg_max_len)
        return sub_sentences

    def merge_word_seg(self, word_segs, avg_max_len, max_len):
        i = 0
        cur_sub_sentence = []
        sub_sentences = []
        while i <= len(word_segs) - 1:
            word, _, _ = word_segs[i]
            cur_sub_sentence.append(word)
            i += 1
            if self.get_length(''.join(cur_sub_sentence)) > avg_max_len:
                cur_sub_sent = ''.join(cur_sub_sentence[-3:-1])
                # 如果是英文，且是a an the 结尾，放到下一句
                if cur_sub_sent.lower() in ['a ', 'a', 'an', 'an ', 'the', 'the '] and self.get_length(
                        ''.join(cur_sub_sentence[-3:])) <= avg_max_len:
                    sub_sentences.append(''.join(cur_sub_sentence[:-3]))
                    cur_sub_sentence = cur_sub_sentence[-3:]
                else:
                    sub_sentences.append(''.join(cur_sub_sentence[:-1]))
                    cur_sub_sentence = [cur_sub_sentence[-1]]
                if 1 < i < len(word_segs) - 2:
                    residual_words = [word for word, _, _ in word_segs][i - 1:]
                    avg_max_len = self.calculate_avg_max_len(''.join(residual_words), max_len)
        # 剩下的句子
        if cur_sub_sentence:
            sub_sentences.append(''.join(cur_sub_sentence))
        return sub_sentences

    def clean_text(self, text, lang='cn'):
        text = text.strip()
        cleaned_text = ''
        # 书名号中的标点全部保留
        text_list: list = self.split_text_by_symbol_pairs(text, {'》': '《', })

        for sub_text in text_list:
            if not sub_text:
                continue
            if sub_text[0] == '《' and sub_text[-1] == '》':
                cleaned_text += sub_text
            else:
                cleaned_text += self.clean_en_text(sub_text) if lang == 'en' else self.clean_cn_text(sub_text)
        return cleaned_text.strip()

    def calculate_text_duration(self, text_list: list, languages: list, token_idx_dur_map: dict):
        # 根据每个字的时间，计算每个小句的时间
        text_duration = []
        text_len = -1
        for i, (text, lang) in enumerate(zip(text_list, languages)):
            start_time = token_idx_dur_map[text_len + 1][0]
            text_len += len(text)
            end_time = token_idx_dur_map[max(0, text_len)][1]
            text = self.clean_text(text, lang)
            # if not text:
            #     continue
            text_duration.append({
                "start_time": start_time,
                "end_time": end_time,
                "text": text})
        return text_duration

    def calculate_avg_max_len(self, text, max_len):
        quotient, remainder = divmod(self.get_length(text), max_len)
        if float(remainder) > 0:
            quotient += 1
        else:
            return max_len
        avg_max_len = min((self.get_length(text) // quotient) + 3, max_len)
        return avg_max_len

    def decide_language(self, text):
        if not text.strip():
            return 'cn'

        chinese_characters = re.compile(r'[\u4e00-\u9fa5]').findall(text)
        english_words = re.compile(r'[a-zA-Z]+').findall(text)

        # 计算中文汉字的数量
        chinese_count = len(chinese_characters)
        # 计算英文单词的数量
        english_count = len(english_words)

        # 总字符数（中文汉字 + 英文单词）
        total_characters = chinese_count + english_count
        if total_characters < 1:
            return 'cn'

        english_ratio = english_count / total_characters * 100

        # 全是英文 无中文, 算做英文
        if not is_contains_chinese(text) and re.findall(r'[A-Za-z]', text):
            english_ratio = 100
        return 'en' if english_ratio >= 90 else 'cn'

    def parse(self, char_durations, max_lens=None):
        logger.info(f'subtitle_version: {VERSION}')
        if max_lens is None:
            max_lens = {'cn': 24, 'en': 27}

        if not char_durations:
            return {"subtitle_data": []}

        # 计算每个字符的开始时间，结束时间
        raw_text_list = []
        token_idx_dur_maps = []

        raw_text = ''
        char_idx = -1
        token_idx_dur_map = {}
        # char_durations = [i for item in char_durations for i in item]
        for char_dur in char_durations:
            tag = char_dur['tag']
            text = char_dur['text']
            start_time = char_dur['start_time']
            end_time = char_dur['end_time']
            if tag == 'segment' and raw_text:
                raw_text_list.append(raw_text)
                token_idx_dur_maps.append(token_idx_dur_map)
                raw_text = ''
                char_idx = -1
                token_idx_dur_map = {}
            else:
                raw_text += text
                # 平分一下字符的时间
                avg_time = (end_time - start_time) / len(text) if len(text) > 1 else 0.0
                cur_time = start_time
                for i, c in enumerate(text):
                    char_idx += len(c)
                    real_end_time = end_time if i == len(text) - 1 else cur_time + avg_time
                    token_idx_dur_map[char_idx] = [cur_time, real_end_time]
                    cur_time += avg_time

        # 如果没有segment
        if raw_text and token_idx_dur_map:
            raw_text_list.append(raw_text)
            token_idx_dur_maps.append(token_idx_dur_map)

        if raw_text_list == [] or raw_text_list == ['']:
            return {"subtitle_data": []}

        text_duration_list = []
        for text, token_idx_dur_map in zip(raw_text_list, token_idx_dur_maps):
            text_list, languages = self.parse_singe_text(text, max_lens)
            text_duration: list = self.calculate_text_duration(text_list, languages, token_idx_dur_map)
            text_duration_list.extend(text_duration)

        out_text_duration_list = []
        for item in text_duration_list:
            start_time = item['start_time']
            end_time = item['end_time']
            text = item['text']

            if not text:
                continue

            out_text_duration_list.append(item)

            # 如果是不发音的字符:
            if is_all_punctuation(text):
                if not out_text_duration_list:
                    continue
                out_text_duration_list.pop(-1)
                if out_text_duration_list:
                    out_text_duration_list[-1] = {
                        "start_time": out_text_duration_list[-1]['start_time'],
                        "end_time": end_time,
                        "text": out_text_duration_list[-1]['text']}
        return {"subtitle_data": out_text_duration_list}

    def parse_singe_text(self, raw_text: str, max_lens):
        paragraph_lang = self.decide_language(raw_text)
        max_len = max_lens[paragraph_lang]

        # 《》<>[] 内不允许分开
        symbols_pairs_position = self.find_symbol_pairs(raw_text)
        symbols_pairs_position = [(start, end) for text, start, end in symbols_pairs_position if
                                  raw_text[start:end] == text and end - start <= max_len]

        # 按照。？?！!.分句
        text_list = split_text_by_regex(raw_text, self.text_end_punc_pattern, symbols_pairs_position)

        candidates = []
        languages = []  # 每一句是中文还是英文
        for ful_text in text_list:
            # 以终止符结束的短句
            lang = self.decide_language(ful_text)
            max_len = max_lens[lang]

            symbols_pairs = self.find_symbol_pairs(ful_text)
            symbols_pairs = [(start, end) for text, start, end in symbols_pairs if
                             ful_text[start:end] == text and end - start <= max_len]
            # 按,，分， 成对标点不切开
            sub_texts_list = split_text_by_regex(ful_text, self.text_mid_punc_pattern, symbols_pairs)

            candidate = []
            for sub_text in sub_texts_list:
                if self.get_length(sub_text) <= max_len:
                    candidate.append(sub_text)
                    continue

                symbols_pairs = self.find_symbol_pairs(sub_text)
                symbols_pairs = [(start, end) for text, start, end in symbols_pairs if
                                 sub_text[start:end] == text and end - start <= max_len]
                # 按:：、分， 成对标点不切开
                sub_sents = split_text_by_regex(sub_text, '[:：、]+', symbols_pairs)
                for sub_sent in sub_sents:
                    if self.get_length(sub_sent) <= max_len:
                        candidate.append(sub_sent)
                    else:
                        sub_sentences: list = self.tokenize_text(sub_sent, max_len, lang)
                        candidate.extend(sub_sentences)

            # 短句合并+字数均匀分布
            avg_max_len = self.calculate_avg_max_len(ful_text, max_len)
            candidate = self.combine_sub_sentences(candidate, avg_max_len)
            candidates.extend(candidate)
            languages.extend([lang] * len(candidate))

        return candidates, languages

    def clean_cn_text(self, text):
        text = re.sub('^[、～~。？?！!:；;…，,—…]+', ' ', text)
        text = re.sub('[、～~。？?！!:；;…，,—…“]+$', ' ', text)
        text = text.strip()
        text = re.sub(r'((?<=[^0-9])[，,])|([，,](?=[^0-9+]))', ' ', text)
        text = re.sub(r'[：、]', ' ', text)
        text = re.sub(r'\.{2,}', '', text)
        text = re.sub(r'[～~。？?！!…]', '', text)
        text = re.sub(r'\s+', r' ', text)
        text = re.sub(r'\s*(["”])(?![a-zA-Z])', r'\1', text)
        return text

    def clean_en_text(self, text):
        text = re.sub('^[ ，,、～~。？?！!:；—…]+', ' ', text)
        text = re.sub(r'\s+', r' ', text)
        text = re.sub(r'\s*(["”])(?![a-zA-Z])', r'\1', text)
        return text
