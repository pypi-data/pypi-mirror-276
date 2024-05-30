class TrieNode:
    """Trie 树的节点"""

    def __init__(self, ch):
        self.ch = ch  # 保存字符
        self.children = dict()  # 保存子节点，key 为字，value 为节点
        self.is_end = False  # 是否是一个词的终止字


class Trie(object):
    """Trie 树"""

    def __init__(self):
        """根节点，空的，不保存任何字符"""
        self.root = TrieNode('')

    def reset(self):
        """重置trie树"""
        self.__init__()

    def add(self, word):
        """插入词，构建 Trie 树"""
        tree = self.root
        # 插入到合适的节点中
        for w in word:
            if w in tree.children:
                tree = tree.children[w]
            else:
                new_tree = TrieNode(w)
                tree.children[w] = new_tree
                tree = new_tree
        # 词的最后一个字所对应的节点
        tree.is_end = True

    def fmm(self, text):
        """正向最大匹配(forward maximum matching)算法"""
        results = []
        i = 0
        while i < len(text):
            tree = self.root
            word = ''
            for j in range(i, len(text)):
                token = text[j]
                if token in tree.children:
                    tree = tree.children[token]
                    word += token
                    if tree.is_end and j == len(text) - 1:
                        # 如果匹配出一个词，则从该词的结束位置开始下一次匹配
                        results.append(word)
                        i = j
                        break
                else:
                    if tree.is_end:
                        # 如果匹配出一个词，则从该词的结束位置开始下一次匹配
                        results.append(word)
                        i = j - 1
                    break
            i += 1
        return results
