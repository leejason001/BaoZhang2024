#coding: utf8

treeLevelBaseSpace = '1'


def printCurrentTree(treeNode, depth):
    print treeNode
    if treeNode.children:
        depth += 1
        for child in treeNode.children:
            print treeLevelBaseSpace * depth
            printCurrentTree( child, depth )