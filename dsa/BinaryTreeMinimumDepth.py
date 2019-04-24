class Node(object):
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None


def get_minimum_depth(root):
    if root is None:
        return 0
    left_depth = get_minimum_depth(root.left)
    right_depth = get_minimum_depth(root.right)
    return 1 + min(left_depth, right_depth)


def print_paths_from_root_to_leaves(root, stack):
    if root is None:
        return

    stack.append(root.data)

    if root.left is None and root.right is None:
        print('->'.join([str(i) for i in stack]))

    print_paths_from_root_to_leaves(root.left, stack)
    print_paths_from_root_to_leaves(root.right, stack)
    stack.pop()

root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(7)
root.left.right = Node(6)
# root.right.right = Node(4)
# root.right.left = Node(5)

#      1
#     /  \
#    2    3
#  /   \
# 7     6

if __name__ == '__main__':
    print(get_minimum_depth(root))
    print_paths_from_root_to_leaves(root, [])
