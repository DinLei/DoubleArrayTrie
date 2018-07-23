#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/7/23 9:14
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

if __name__ == "__main__":

    from trie_obj import DoubleArrayTrieImp1

    examples = ["hello", "world", "a", "beautiful", "day",
                "see", "you", "tomorrow", "goodbye", "tonight",
                "win", "a", "big", "prize"]

    dat = DoubleArrayTrieImp1(examples)

    dat.add2trie("today")
    dat.add2trie("swim")
    dat.add2trie("swimming")
    dat.add2trie("hate")
    dat.add2trie("win")

    print(dat.fuzzy_search("win", tol=2))


