class Node():
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class DoublyLinkedList():
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.size = self.size + 1
            return

        cur = self.head
        while cur.next:
            cur = cur.next

        cur.next = new_node
        new_node.prev = cur
        self.tail = new_node
        self.size = self.size + 1

    def prepend(self, data):
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.size = self.size + 1
            return

        head = self.head
        new_node.next = head
        head.prev = new_node
        self.head = new_node
        self.size = self.size + 1

    def delete_node(self, node):
        prev = None
        temp = self.head
        if temp is None:
            return
        elif node is None:
            return
        elif node == temp.data and temp.next is None:
            temp = None
            return
        elif temp is not None and temp.data == node and temp.next is not None: # delete head operation
            self.head = temp.next
            temp = None
            head = self.head
            head.prev = None
            return
        else:
            node_exists = False
            while (temp is not None):
                if temp.data == node:
                    node_exists = True
                    break
                prev = temp
                temp = temp.next
            if node_exists:
                prev.next = temp.next
                temp.next.prev = prev
                temp = None

    def print_list(self):
        cur = self.head
        while cur:
            print(cur.data)
            cur = cur.next

    def find_middle(self):
        slow = self.head
        fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow.data


if __name__ == '__main__':
    llist5 = DoublyLinkedList()
    llist5.append(1)
    llist5.append(2)
    llist5.append(3)
    llist5.append(4)
    llist5.prepend(5)
    llist5.prepend(6)

    # print(llist5.find_middle())
    llist5.print_list()
