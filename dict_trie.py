#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-7-23 下午10:02
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com


class DictTrie:

    def __init__(self):
        self.trie_tree = None

    def train(self, words_list):
        """构造Trie（用dict登记结点信息和维持子结点集合）"""
        trie = {}
        for word in words_list:
            t = trie
            for c in word:
                c1 = ord(c)
                if c1 not in t:
                    t[c1] = {}
                t = t[c1]
            t[None] = None
        self.trie_tree = trie

    @staticmethod
    def decode(code):
        code = list(code)
        tmp = [chr(int(i)) for i in code]
        return "".join(tmp)

    def fuzzy_search(self, word, tol=1):
        candidate = list()
        word = [ord(x) for x in word]
        if not word:
            return candidate
        q = deque([(self.trie_tree, word, '', tol)])
        while q:
            trie, word, path, tol = q.popleft()
            if not word:
                if None in trie:
                    if path not in candidate:
                        candidate.append(path)
                if tol > 0:
                    for k in trie:
                        if k is not None:
                            q.appendleft((trie[k], '', path + chr(k), tol - 1))
            else:
                if word[0] in trie:
                    q.appendleft((trie[word[0]], word[1:], path + chr(word[0]), tol))
                if tol > 0:
                    for k in trie.keys():
                        if k is not None and k != word[0]:
                            q.append((trie[k], word[1:], path + chr(k), tol - 1))
                            q.append((trie[k], word, path + chr(k), tol - 1))
                    q.append((trie, word[1:], path, tol - 1))
                    if len(word) > 1:
                        q.append((trie, list([word[1]]) + list([word[0]]) + word[2:], path, tol - 1))
        return candidate
