class Node:
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


def print_the_tree_inorder(root):
    if root is not None:
        print_the_tree_inorder(root.left)
        print(root.data)
        print_the_tree_inorder(root.right)


def print_the_tree_preorder(root):
    if root is not None:
        print(root.data)
        print_the_tree_preorder(root.left)
        print_the_tree_preorder(root.right)


def print_the_tree_postorder(root):
    if root is not None:
        print_the_tree_postorder(root.left)
        print_the_tree_postorder(root.right)
        print(root.data)


def print_at_given_level(root, level):
    if root is None:
        return
    elif level == 1:
        print(root.data)
    elif level > 1:
        print_at_given_level(root.left, level - 1)
        print_at_given_level(root.right, level - 1)


def breadth_first_search_or_level_order_tree_traversal(root):
    height = max_depth_of_a_bst(root)
    for i in range(1, height+1):
        print_at_given_level(root, i)

def max_depth_of_a_bst(root):
    if root is None:
        return 0
    else:
        ldepth = max_depth_of_a_bst(root.left)
        rdepth = max_depth_of_a_bst(root.right)

        if ldepth > rdepth:
            return ldepth + 1
        else:
            return rdepth + 1


def max_value_in_the_tree(root):
    if root is None:
        return 0

    res = root.data

    lres = max_value_in_the_tree(root.left)
    rres = max_value_in_the_tree(root.right)

    # if lres > res:
    #     res = lres
    # if rres > res:
    #     res = rres
    # return res
    return max(lres, rres, res)


def find_max(root):
    current = root

    while current.right is not None:
        current = current.right

    return current.data


def find_min(root):
    current = root

    while current.left is not None:
        current = current.left

    return current.data


def delete_the_node(root, key):
    if root is None:
        return root

    if key > root.data:
        root.right = delete_the_node(root.right, key)

    elif key < root.data:
        root.left = delete_the_node(root.left, key)

    else:
        if root.right is None:
            temp = root.left
            root = None
            return temp
        elif root.left is None:
            temp = root.right
            root = None
            return temp

            # Node with two children: Get the inorder successor
            # (smallest in the right subtree)

        temp = find_min(root.right)

        # Copy the inorder successor's content to this node
        root.data = temp.data

        # Delete the inorder successor
        root.right = delete_the_node(root.right, temp.data)

        return root


r = Node(50)
insert(r, Node(30))
insert(r, Node(20))
insert(r, Node(40))
insert(r, Node(70))
insert(r, Node(60))
insert(r, Node(80))

if __name__ == '__main__':
    print_the_tree_inorder(r)
    print_the_tree_preorder(r)
    print_the_tree_postorder(r)

    print("height of the tree : " + str(max_depth_of_a_bst(r)))
    print("diameter of the tree : " + str(max_depth_of_a_bst(r)))

    print(max_value_in_the_tree(r))

    print(find_max(r))
    print(find_min(r))

    print("BFS Tree")
    breadth_first_search_or_level_order_tree_traversal(r)
