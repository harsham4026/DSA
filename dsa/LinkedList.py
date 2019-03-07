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

        return slow.data

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

    def if_node_exists(self, node):
        head = self.head
        while head is not None:
            if head.data == node:
                return True
            head = head.next
        return False

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
        elif temp is not None and temp.data == node and temp.next is not None:
            self.head = temp.next
            temp = None
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
                temp = None

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

    def sort_linked_list(self):
        temp = self.head
        new_list = []
        while temp is not None:
            new_list.append(temp.data)
            temp = temp.next
        new_list = sorted(new_list)
        return new_list

    def is_palindrome(self):
        head = self.head
        new_list = []

        while head is not None:
            new_list.append(head.data)
            head = head.next

        head = self.head
        size = self.size
        counter = 0
        while head is not None:
            if len(new_list) >= 1 and head.data == new_list.pop():
                counter += 1
                head = head.next
            else:
                break
        return counter == size

    def merge_sorted_linked_lists(self, list1, list2):
        if list1 is None:
            return list2
        elif list2 is None:
            return list1
        elif list1.data < list2.data:
            print(list1.data)
            list1.next = self.merge_sorted_linked_lists(list1.next, list2)
            return list1
        else:
            print(list2.data)
            list2.next = self.merge_sorted_linked_lists(list1, list2.next)
            return list2

        # print(type(l1))
        # print(type(l2))
        #
        # curr = dummy = Node(0)
        # while l1 and l2:
        #     if l1.data < l2.data:
        #         curr.next = l1
        #         l1 = l1.next
        #     else:
        #         curr.next = l2
        #         l2 = l2.next
        #     curr = curr.next
        # curr.next = l1 or l2
        # return dummy.next

if __name__ == '__main__':
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
    llist.append(8)
    llist.append(7)
    llist.print_llist()

    # node deletion from a linkedlist
    print("after deletion of an element from linked list")
    llist.delete_node(13)
    llist.print_llist()

    # print middle element of linked list
    print("middle element of linked list : {}".format(str(llist.print_middle_element())))
    print("size : {}".format(str(llist.size)))

    # duplicates removal from linked list
    llist.remove_duplicates()
    print("after duplicates removal")
    llist.print_llist()
    sorted_llist = llist.sort_linked_list()

    # sorting the linked list
    print("sorted linked list is ")
    llist2 = SLinkedList()
    for i in sorted_llist:
        llist2.append(i)
    llist2.print_llist()

    # palindrome check for linked list
    llist3 = SLinkedList()
    llist3.append(1)
    llist3.append(1)
    llist3.append(2)

    print(llist3.is_palindrome())

    # merge two sorted lists
    llist4 = SLinkedList()
    llist5 = SLinkedList()

    llist4.append(1)
    llist4.append(2)
    llist4.append(3)

    llist5.append(4)
    llist5.append(5)
    llist5.append(6)

    llist6 = SLinkedList()
    merged_linked_list = llist6.merge_sorted_linked_lists(llist4.head, llist5.head)
