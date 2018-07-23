#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/3/26 18:36
# @Author  : BigDin
# @Contact : dinglei_1107@outlook.com

class TreeSet:
    def __init__(self):
        self.__set = set()

    def values(self):
        return sorted(self.__set)

    def add(self, val):
        self.__set.add(val)

    def remove(self, val):
        if val in self.__set:
            self.__set.remove(val)

    def higher(self, val):
        if self.the_max() < val:
            return None
        if self.the_min() > val:
            return self.the_min()
        vals = self.values()
        low = 0
        up = self.size()-1
        while low <= up:
            mid = (low + up) // 2
            if vals[mid] <= val:
                low = mid + 1
            elif vals[mid-1] <= val:
                return vals[mid]
            else:
                up = mid - 1

    def the_max(self):
        if not self.__set:
            return -1
        return max(self.__set)

    def the_min(self):
        if not self.__set:
            return -1
        return min(self.__set)

    def size(self):
        return len(self.__set)

    def is_empty(self):
        return self.size() == 0

