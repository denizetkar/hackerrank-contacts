#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'contacts' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts 2D_STRING_ARRAY queries as parameter.
#


class Node:
    def __init__(self, val):
        self.val = val
        self.terminal = False
        self.terminal_descendant_cnt = 0
        self.children = {}

    def _add_child(self, child):
        self.children[child.val] = child
        self.terminal_descendant_cnt += child.terminal_descendant_cnt + int(child.terminal)

    def add_name(self, name):
        if len(name) == 0:
            self.terminal = True
            return False
        next_val = name[0]

        if next_val not in self.children:
            new_child = Node(next_val)
            new_child.add_name(name[1:])
            self._add_child(new_child)
            return True

        is_added = self.children[next_val].add_name(name[1:])
        self.terminal_descendant_cnt += int(is_added)
        return is_added

    def get_node(self, name):
        if len(name) == 0:
            return self

        next_val = name[0]
        if next_val not in self.children:
            return None
        child = self.children[next_val]
        return child.get_node(name[1:])


class Trie:
    def __init__(self):
        self.roots = {}

    def add(self, name):
        root_val = name[0]
        if root_val not in self.roots:
            self.roots[root_val] = Node(root_val)
        root = self.roots[root_val]
        root.add_name(name[1:])

    def get_node(self, name):
        root_val = name[0]
        if root_val not in self.roots:
            return None
        root = self.roots[root_val]
        return root.get_node(name[1:])

    def prefix_match_cnt(self, name):
        node = self.get_node(name)
        if node is None:
            return 0
        return node.terminal_descendant_cnt + int(node.terminal)


def contacts(queries):
    trie = Trie()
    terminal_cnts = []
    for query in queries:
        if query[0] == "add":
            name = query[1]
            trie.add(name)
        elif query[0] == "find":
            name = query[1]
            terminal_cnts.append(trie.prefix_match_cnt(name))
    return terminal_cnts


if __name__ == "__main__":
    with open(os.environ["INPUT_PATH"], "r") as f, open(os.environ["OUTPUT_PATH"], "w") as fptr:
        queries_rows = int(f.readline().strip())

        queries = []

        for _ in range(queries_rows):
            queries.append(f.readline().rstrip().split())

        result = contacts(queries)

        fptr.write("\n".join(map(str, result)))
        fptr.write("\n")
