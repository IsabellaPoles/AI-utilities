#CS 411 - Artificial Intelligence: Assignment 10
#Isabella Poles
#UIN: 673937460

import numpy as np
import pandas as pd
from scipy.stats import chi2

class DecisionTree:
    def __init__(self, att, children, depth, label, subset):
        self.att = att
        self.children = children
        self.depth = depth
        self.label = label
        self.subset = subset
        self.accepted = False

    def __str__(self):
        if self.att is None:
            return '\t' * (self.depth * 2 - 1) + 'Label: ' + self.label + '\n'
        else:
            temp = '\t' * (self.depth * 2 - 1)  + '- ' + self.att + ':\n'
            for key, value in self.children.items():
                temp += '\t' * (self.depth * 2) + '- ' + key + ': \n' + str(value)
            return temp

    def is_leaf(self):
        return self.att is None

    def is_testable(self):
        if self.is_leaf() or self.accepted:
            return False
        for v in self.children.values():
            if not v.is_leaf():
                return False
        return True

    # checks if any node in the tree is testable
    def has_testables(self):
        if self.is_testable():
            return True
        elif self.is_leaf() or self.accepted:
            return False
        else:
            for c in self.children.values():
                if c.has_testables():
                    return True
            return False


def entropy(examples, att):
    # print(att)
    temp = 0
    for val in examples[att].unique():
        P = (examples[examples[att] == val].shape[0]) / (examples.shape[0])
        #print(val + ': ' + str(P))
        temp -= P * np.log2(P)
    return float('%.2f'%(temp))


def importance(examples, att, values, goal):
    gain = entropy(examples, goal)
    # print(gain)
    for val in values:
        subset = examples[examples[att] == val]
        gain -= entropy(subset, goal) * subset.shape[0] / examples.shape[0]
    return float('%.2f'%(gain))


def plurality_value(examples, goal):
    count = {}
    for val in examples[goal].unique():
        count[val] = examples[examples[goal] == val].shape[0]
    return max(count, key=count.get)


def decision_tree_learning(examples, attributes, parent_examples, goal, depth):
    if examples.shape[0] == 0:
        return DecisionTree(None, None, depth + 1, plurality_value(parent_examples, goal), examples)
    elif len(examples[goal].unique()) == 1:
        return DecisionTree(None, None, depth + 1, examples[goal].unique()[0], examples)
    elif len(attributes) == 0:
        return DecisionTree(None, None, depth + 1, plurality_value(examples, goal), examples)
    else:
        print('Depth: ' + str(depth))
        print(attributes.keys())
        gains = {}
        for a, val in attributes.items():
            gains[a] = importance(examples, a, val, goal)
        print(gains.values())
        best = max(gains, key=gains.get)
        print('Best: ' + best)
        print('\n')
        tree = DecisionTree(best, {}, depth + 1, None, examples)
        values = attributes[best]
        del attributes[best]
        for val in values:
            tree.children[val] = decision_tree_learning(examples[examples[best] == val], attributes, examples, goal, depth + 1)
        return tree


def significance_test(tree, goal):
    delta = 0
    examples = tree.subset
    p = examples.loc[examples[goal] == 'Yes', goal].count()
    n = examples.loc[examples[goal] == 'No', goal].count()
    df = len(tree.children) - 1
    for c in tree.children.values():
        ex_k = c.subset
        p_k = ex_k.loc[ex_k[goal] == 'Yes', goal].count()
        n_k = ex_k.loc[ex_k[goal] == 'No', goal].count()
        p_hat = p * ex_k.shape[0] / examples.shape[0]
        n_hat = n * ex_k.shape[0] / examples.shape[0]
        delta += ((p_k - p_hat) ** 2) / p_hat + ((n_k - n_hat) ** 2) / n_hat

    if delta >= chi2.isf(0.05, df):
        return True
    else:
        return False


def chi_pruning(tree, goal):
    while tree.has_testables():
        if tree.is_testable():
            if significance_test(tree, goal):
                tree.accepted = True
            else:
                tree.att = None
                tree.label = plurality_value(tree.subset, goal)
        else:
            for c in tree.children.values():
                chi_pruning(c, goal)

file = input("Insert file name: ")
examples = pd.read_csv(file)
goal = input("Target attribute: ")
print(examples)
print('\n\n')
attributes = {}
for att in examples.columns:
    if att != goal:
        attributes[att] = examples[att].unique()
tree = decision_tree_learning(examples, attributes, None, goal, 0)
print('Full tree: ')
print(tree)

print('\n\n')
chi_pruning(tree, goal)
print('Pruned tree: ')
print(tree)