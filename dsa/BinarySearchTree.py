class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def height_of_tree(root):
    if root is None:
        return 0

    lheight = height_of_tree(root.left)
    rheight = height_of_tree(root.right)

    return max(lheight, rheight) + 1


def get_width_of_a_level(root, level):
    if root is None:
        return 0
    elif level == 1:
        return 1
    else:
        return get_width_of_a_level(root.left, level - 1) + get_width_of_a_level(root.right, level - 1)


def max_width_of_tree(root):
    height = height_of_tree(root)
    max_width = 0

    for i in range(1, height + 1):
        width = get_width_of_a_level(root, i)
        if width > max_width:
            max_width = width
    return max_width


# A function to do inorder tree traversal
def printInorder(root):
    if root:
        # First recur on left child
        printInorder(root.left)

        # then print the data of node
        print(root.data),

        # now recur on right child
        printInorder(root.right)

    # A function to do postorder tree traversal


def printPostorder(root):
    if root:
        # First recur on left child
        printPostorder(root.left)

        # the recur on right child
        printPostorder(root.right)

        # now print the data of node
        print(root.val),

    # A function to do preorder tree traversal


def printPreorder(root):
    if root:
        # First print the data of node
        print(root.val),

        # Then recur on left child
        printPreorder(root.left)

        # Finally recur on right child
        printPreorder(root.right)


root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(7)
root.left.right = Node(6)
root.right.right = Node(4)
root.right.left = Node(5)

if __name__ == '__main__':
    print("max width of the given binary tree is : {}".format(str(max_width_of_tree(root))))
    print(root.data)
    printInorder(root)