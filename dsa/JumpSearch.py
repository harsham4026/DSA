"""Time complexity of jump searech algo is O(sqrt(n))"""

import math


def jump_search(arr, element_to_find):
    low = 0
    jump_interval = int(math.sqrt(len(arr)))
    for i in range(0, len(arr), jump_interval):
        if arr[i] < element_to_find:
            low = i
        elif arr[i] == element_to_find:
            return i
        else:
            break
    c = low
    for i in arr[low:]:
        if i == element_to_find:
            return c
        c += 1
    return -1


if __name__ == '__main__':
    arr = [10, 20, 30, 50, 60, 80, 110, 120, 150, 180, 200]
    index_of_the_element = jump_search(arr, 80)
    print("jump searched index of existing element {index_of_the_element}".format(
        index_of_the_element=index_of_the_element))
    index_of_unlisted_ele = jump_search(arr, 201)
    print("jump searched element's index which doesn't exist {index_of_unlisted_ele}".format(
        index_of_unlisted_ele=index_of_unlisted_ele))
