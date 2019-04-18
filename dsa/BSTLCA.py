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
    print(least_common_ancestor(root, 1, 51))
    print(lca(root, 1, 51, root.data))
    print(lca(root, 3, 4, root.data))
    # printPreorder(root)
