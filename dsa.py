from typing import List
from collections import deque

# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []


class Solution:

    def createTree(self,input: List)-> Node:
        if not input:
            return None
        
        root = Node(input[0])
        queue = deque([root])
        i = 2
        parent = queue.popleft()
        
        while i < len(input):
            if input[i] is None:
                i += 1
                if queue:
                    parent = queue.popleft()
                else:
                    break
            else:
                child = Node(input[i])
                parent.children.append(child)
                queue.append(child)
                i += 1
            
        return root

    def postorder(self, root: Node) -> List[int]:
        result = []
        if not root:
            return result
        def traverse(node):
            for child in node.children:
                traverse(child)
            result.append(node.val)
        traverse(root)
        return result

solution = Solution()

"""
Input: root = [1,null,3,2,4,null,5,6]
"""

"""
Input: root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
"""

input = [[1,None,3,2,4,None,5,6],
         [1, None, 2, 3, 4, 5, None, None, 6, 7, None, 8, None, 9, 10, None, None, 11, None, 12, None, 13, None, None, 14]]
for i in input:
    root = solution.createTree(i)
    print("Postorder Traversal :", solution.postorder(root))