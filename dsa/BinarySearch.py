"""Time complexity is O(logn). Number of steps it might take to find the element is n*(1/2)^k = 1
n/2^k = 1,
n = 2^k
k = log(n)"""


def binary_search(arr, element_to_find, starting_index, last_index):
    if last_index >= starting_index:
        mid_index = int((starting_index + last_index) / 2)
        if arr[mid_index] == element_to_find:
            return mid_index
        elif element_to_find > arr[mid_index]:
            return binary_search(arr, element_to_find, mid_index + 1, last_index)
        else:
            return binary_search(arr, element_to_find, starting_index, mid_index - 1)
    else:
        return -1


if __name__ == '__main__':
    arr = [1, 2, 5, 7, 8]
    element_to_find = 7
    element_to_find_test = 10
    index_of_element = binary_search(arr, element_to_find, 0, (len(arr) - 1))
    print("index of the element {element_to_find} is {index_of_element}".format(element_to_find=element_to_find,
                                                                                index_of_element=index_of_element))

    not_existing_element_index = binary_search(arr, element_to_find_test, 0, len(arr) - 1)
    print("not_existing_element_index : " + str(not_existing_element_index))
