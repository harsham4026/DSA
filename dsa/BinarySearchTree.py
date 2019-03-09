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


def minValueNode(node):
    current = node

    # loop down to find the leftmost leaf
    while current.left is not None:
        current = current.left

    return current


# Given a binary search tree and a key, this function
# delete the key and returns the new root
def deleteNode(root, key):
    # Base Case
    if root is None:
        return root

        # If the key to be deleted is smaller than the root's
    # key then it lies in  left subtree
    if key < root.data:
        root.left = deleteNode(root.left, key)

        # If the kye to be delete is greater than the root's key
    # then it lies in right subtree
    elif (key > root.data):
        root.right = deleteNode(root.right, key)

        # If key is same as root's key, then this is the node
    # to be deleted
    else:

        # Node with only one child or no child
        if root.left is None:
            temp = root.right
            root = None
            return temp

        elif root.right is None:
            temp = root.left
            root = None
            return temp

            # Node with two children: Get the inorder successor
        # (smallest in the right subtree)
        temp = minValueNode(root.right)

        # Copy the inorder successor's content to this node
        root.data = temp.data

        # Delete the inorder successor
        root.right = deleteNode(root.right, temp.data)

    return root


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

    # root = deleteNode(root, 50)
    # print(
    # "Inorder traversal of the modified tree")
    # printInorder(root)
