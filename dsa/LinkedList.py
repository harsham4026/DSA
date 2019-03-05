class Node():
    def __init__(self, data):
        self.data = data
        self.next = None


class SLinkedList():
    def __init__(self):
        self.head = None
        self.size = 0

    def print_llist(self):
        cur = self.head
        while cur is not None:
            print(cur.data)
            cur = cur.next

    # instead of traversing the entire linked list here we use to pointers to find the middle element.
    # first pointer will be moving one step at a time and second pointer would be moving 2 steps at a time. So when the
    # second pointer reached last element first element will be at middle element.
    def print_middle_element(self):
        slow = self.head
        fast = self.head
        while fast is not None:
            fast = fast.next
            if fast is not None:
                slow = slow.next
                fast = fast.next

        print(slow.data)

    def prepend(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.size = self.size + 1
            return

        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def append(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.size = self.size + 1
            return

        last = self.head
        while last.next is not None:
            last = last.next

        last.next = new_node
        self.size = self.size + 1

    def insert_after(self, previous_node, data):
        new_node = Node(data)
        previous_node = Node(previous_node)
        if previous_node is None:
            return

        # point new node's data to previous node's next element
        new_node.next = previous_node.next
        # now point the previous node's next to new_node
        previous_node.next = new_node
        self.size = self.size + 1

    def remove_duplicates(self):
        temp = self.head
        if temp is None:
            return

        while temp.next is not None:
            if temp.data == temp.next.data:
                new_elem = temp.next.next
                temp.next = None
                temp.next = new_elem
            else:
                temp = temp.next


llist = SLinkedList()
# llist.head = Node(1)
# llist.head.next = Node(2)
# llist.head.next.next = Node(3)
# llist.head.next.next.next = Node(4)
# llist.head.next.next.next.next = Node(5)
# llist.head.next.next.next.next.next = Node(6)

llist.append(1)
llist.append(1)
llist.append(2)
llist.append(3)
llist.append(4)
llist.append(5)
llist.append(6)
llist.append(7)
llist.append(8)

if __name__ == '__main__':
    llist.print_llist()
    llist.print_middle_element()
    print("size : {}".format(str(llist.size)))
    llist.remove_duplicates()
    print("after duplicates removal")
    llist.print_llist()
