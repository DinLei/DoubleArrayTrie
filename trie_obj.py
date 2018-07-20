#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/7/19 16:27
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

from utils.util import TreeSet


class AbstractDoubleArrayTrie:
    LEAF_BASE_VALUE = -2
    ROOT_CHECK_VALUE = -3
    EMPTY_VALUE = -1
    INITIAL_ROOT_BASE = 1
    alphabet_dict = dict()
    index_alphabet = dict()

    def __init__(self, phrase_list):
        self.init_alphabet_dict(phrase_list)

    def init_alphabet_dict(self, phrase_list):
        alphabets = set()
        for phrase in phrase_list:
            alphabets.update(str(phrase))
        for ind, ele in enumerate(alphabets):
            self.alphabet_dict[ele] = ind
            self.index_alphabet[ind] = ele

    def add2trie(self, word):
        changed = False
        state = 0
        i = 0
        words_codes = [self.alphabet_dict[x] for x in word]
        while i < len(words_codes):
            assert state >= 0
            assert self.get_base(state) >= 0
            c = words_codes[i]
            transition = self.get_base(state) + c
            assert transition >= 0
            self.ensure_reachable_index(transition)

            if self.get_check(transition) == self.EMPTY_VALUE:
                self.set_check(transition, state)
                if i == len(word)-1:
                    self.set_base(transition, self.LEAF_BASE_VALUE)
                    changed = True
                else:
                    self.set_base(transition, self.next_available_hop(c))
                    changed = True
            elif self.get_check(transition) != state:
                self.resolve_conflict(state, c)
                changed = True
                continue
            # self.update_insert(state, i-1, words_codes)
            state = transition
            i += 1
        return changed

    def resolve_conflict(self, state, word_code):
        tree_set = TreeSet()
        tree_set.add(word_code)
        for c in self.alphabet_dict.values():
            tmp_next = self.get_base(state) + c
            if tmp_next < self.get_size() and self.get_check(tmp_next) == state:
                tree_set.add(c)
        new_location = self.next_available_move(tree_set.values())
        tree_set.remove(word_code)

        for c in tree_set.values():
            tmp_next = self.get_base(state) + c
            assert self.get_check(new_location+c) == self.EMPTY_VALUE
            self.set_check(new_location+c, state)

            assert self.get_base(new_location+c) == self.EMPTY_VALUE
            self.set_base(new_location+c, self.get_base(tmp_next))
            self.update_child_move(state, c, new_location)

            if self.get_base(tmp_next) != self.LEAF_BASE_VALUE:
                for d in self.alphabet_dict.values():
                    tmp_next_child = self.get_base(tmp_next) + d
                    if tmp_next_child < self.get_size() and self.get_check(tmp_next_child) == tmp_next:
                        self.set_check(tmp_next_child, new_location+c)
                    elif tmp_next_child > self.get_size():
                        break
                self.set_base(tmp_next, self.EMPTY_VALUE)
                self.set_check(tmp_next, self.EMPTY_VALUE)
        self.set_base(state, new_location)
        self.update_state_move(state, new_location)

    def search_with_prefix(self, prefix):
        if not prefix:
            return False
        state = 0
        prefix = str(prefix)
        prefix_codes = [self.alphabet_dict[x] for x in prefix]
        for ind, curr in enumerate(prefix_codes):
            transition = self.get_base(state) + curr
            if transition < self.get_size() and self.get_check(transition) == state:
                if self.get_base(transition) == self.LEAF_BASE_VALUE:
                    if ind == len(prefix)-1:
                        return True
                    else:
                        return False
                state = transition
            else:
                return False
        return True

    def ensure_reachable_index(self, transition):
        pass

    def next_available_hop(self, word_code):
        return 0

    def next_available_move(self, values):
        return 0

    def get_base(self, position):
        return 0

    def get_check(self, position):
        return 0

    def get_size(self):
        return 0

    def set_check(self, position, state):
        pass

    def set_base(self, position, state):
        pass

    def update_insert(self, state, index, words_codes):
        pass

    def update_search(self, state, ind, prefix):
        pass

    def update_state_move(self, state, new_location):
        pass

    def update_child_move(self, state, word_code, new_location):
        pass


class DoubleArrayTrieImp1(AbstractDoubleArrayTrie):
    base = list()
    check = list()

    def __init__(self, phrase_list):
        super(DoubleArrayTrieImp1, self).__init__(phrase_list)
        self.base.append(self.INITIAL_ROOT_BASE)
        self.check.append(self.ROOT_CHECK_VALUE)
        self.free_positions = TreeSet()

        self.ensure_reachable_index(len(self.alphabet_dict))

    def ensure_reachable_index(self, transition):
        if self.get_size() <= transition:
            diff = transition - self.get_size() + 1
            self.base.extend([self.EMPTY_VALUE]*diff)
            self.check.extend([self.EMPTY_VALUE]*diff)
            self.free_positions.add(len(self.base)-1)

    def next_available_hop(self, word_code):
        while self.free_positions.higher(word_code) is None:
            self.ensure_reachable_index(len(self.base)+1)
        return self.free_positions.higher(word_code) - word_code

    def next_available_move(self, values):
        if len(values) == 1:
            return self.next_available_hop(values[0])

        min_val = values[0]
        max_val = values[-1]
        needed_positions = max_val - min_val + 1
        possible = self.find_consecutive_free(needed_positions)
        if possible - min_val >= 0:
            return possible-min_val
        self.ensure_reachable_index(len(self.base) + needed_positions)
        return len(self.base) - needed_positions - min_val

    def find_consecutive_free(self, amount):
        assert amount >= 0
        if self.free_positions.is_empty():
            return -1

        curr_positions = self.free_positions.values()
        the_begin = curr_positions[0]
        previous = the_begin
        consecutive = 1
        for i in range(1, len(curr_positions)):
            current = curr_positions[i]
            if current-previous == 1:
                previous = current
                consecutive += 1
            else:
                the_begin = current
                previous = the_begin
                consecutive = 1
            if consecutive == amount:
                break
        if consecutive == amount:
            return the_begin
        else:
            return -1

    def fuzzy_search(self, chars, tol=1):
        state = 0
        candidates = set()
        if not chars:
            return candidates
        else:
            tmp_queue = list((chars, "", tol, state))
            while tmp_queue:
                chars, path, tol, state = tmp_queue.pop(0)
                if not chars:
                    candidates.add(path)
                    if tol > 0:
                        for e, c in self.alphabet_dict.items():
                            tmp_next = self.get_base(state) + c
                            if tmp_next < self.get_size() and self.get_check(tmp_next) == state:
                                tmp_queue.append(("", path+e, tol-1, tmp_next))
                else:
                    transition = self.get_base(state) + self.alphabet_dict[chars[0]]
                    if transition < self.get_size() and self.get_check(transition) == state:
                        tmp_queue.append((chars[1:], path+chars[0], tol))
                    if tol > 0:
                        for e, c in self.alphabet_dict.items():
                            if e == chars[0]:
                                continue
                            tmp_next = self.get_base(state) + c
                            if tmp_next < self.get_size() and self.get_check(tmp_next) == state:
                                tmp_queue.append((chars[1:], path+e, tol-1, tmp_next))

    def get_size(self):
        return len(self.base)

    def get_base(self, position):
        return self.base[position]

    def get_check(self, position):
        return self.check[position]

    def set_base(self, position, state):
        self.base[position] = state
        if state == self.EMPTY_VALUE:
            self.free_positions.add(position)
        else:
            self.free_positions.remove(position)

    def set_check(self, position, state):
        self.check[position] = state
        if state == self.EMPTY_VALUE:
            self.free_positions.add(position)
        else:
            self.free_positions.remove(position)

    def update_child_move(self, state, word_code, new_location):
        assert self.get_check(self.get_base(state)+word_code) == state
