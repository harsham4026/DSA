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


def print_at_given_level(root, level, flag):
    if root is None:
        return
    elif level == 1:
        print(str(root.data) + " ")
    elif level > 1:
        if flag == True:
            print_at_given_level(root.left, level - 1, flag)
            print_at_given_level(root.right, level - 1, flag)
        else:
            print_at_given_level(root.right, level - 1, flag)
            print_at_given_level(root.left, level - 1, flag)


def print_tree_in_spiral_order(root):
    height = height_of_tree(root)

    flag = False
    for i in range(1, height + 1):
        print_at_given_level(root, i, flag)
        flag = not flag


root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(7)
root.left.right = Node(6)
root.right.right = Node(4)
root.right.left = Node(5)

if __name__ == '__main__':
    print_tree_in_spiral_order(root)
