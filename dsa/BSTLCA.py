class Node():
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def insert(root, node):
    if root is None:
        root = node
    else:
        if node.data < root.data:
            if root.left is None:
                root.left = node
            else:
                insert(root.left, node)
        else:
            if root.right is None:
                root.right = node
            else:
                insert(root.right, node)


def least_common_ancestor(root, a, b):
    while root:
        if a == root.data or b == root.data:
            return root.data
        elif a < root.data and b > root.data:
            return root.data
        elif a > root.data and b < root.data:
            return root.data
        elif a < root.data and b < root.data:
            root = root.left
        else:
            root = root.right


def lca(root, n1, n2, root_data):
    if root is None:
        return None
    elif root.left is None and root.right is None:
        return "one of the element doesn't exist in tree"
    elif n1 < root.data and n2 < root.data:
        return lca(root.left, n1, n2, root_data)
    elif n1 > root.data and n2 > root.data:
        return lca(root.right, n1, n2, root_data)

    return None if root_data == root.data else root.data

def bstElementPresenceUtil(root, var1):
    if root is None:
        return False
    elif root.data == var1:
        return True
    elif root.data < var1:
        return bstElementPresenceUtil(root.right, var1)
    else:
        return bstElementPresenceUtil(root.left, var1)

def find_lca(root, elem1, elem2, n1, n2):
    if elem1 & elem2:
        if root is None:
            return None
        elif n1 < root.data and n2 < root.data:
            return find_lca(root.left, elem1, elem2, n1, n2)
        elif n2 > root.data and n2 < root.data:
            return find_lca(root.right, elem1, elem2, n1, n2)
        return root.data
    else:
        print("one or more element(s) doesn't exist in bst")

def printPreorder(root):
    if root:
        # First print the data of node
        print(root.data),

        # Then recur on left child
        printPreorder(root.left)

        # Finally recur on right child
        printPreorder(root.right)


root = Node(2)
insert(root, Node(5))
insert(root, Node(1))
insert(root, Node(3))
insert(root, Node(4))


    #   2
    # /   \
    #1     5
    #     /
    #     3
    #     \
    #      4
if __name__ == '__main__':
    # print(least_common_ancestor(root, 1, 51))
    # print(lca(root, 1, 51, root.data))
    # print(lca(root, 3, 51, root.data))
    # # printPreorder(root)

    ##working solution
    n1 = 3
    n2 = 57
    elem1 = bstElementPresenceUtil(root, n1)
    elem2 = bstElementPresenceUtil(root, n2)
    print(find_lca(root, elem1, elem2, n1, n2))


