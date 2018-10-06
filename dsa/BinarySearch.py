def binary_search(arr, element_to_find, starting_index, last_index):
    if last_index >= 1:
        mid_index = int(
            (starting_index + last_index + 1) / 2)  # to get the length of the array and take the middle element of it
        if element_to_find > arr[mid_index]:
            return binary_search(arr, element_to_find, mid_index + 1, last_index)
        elif element_to_find < arr[mid_index]:
            return binary_search(arr, element_to_find, starting_index, mid_index - 1)
        elif arr[mid_index] == element_to_find:
            return mid_index
    else:
        return -1


if __name__ == '__main__':
    arr = [1, 2, 5, 7, 8]
    element_to_find = 7
    index_of_element = binary_search(arr, element_to_find, 0, (len(arr) - 1))
    print("index of the element {element_to_find} is {index_of_element}".format(element_to_find=element_to_find,
                                                                                index_of_element=index_of_element))
