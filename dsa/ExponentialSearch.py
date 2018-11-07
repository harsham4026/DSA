"""Time complexity is O(logn)"""

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


def exponential_search(arr, n, element_to_find):
    if arr[0] == element_to_find:
        return 0

    i = 1
    while i < n and arr[i] <= element_to_find:
        i = i * 2
    #print(i)
    return binary_search(arr, element_to_find, i/2, min(i, n))

if __name__ == '__main__':
    arr = [1, 2, 5, 7, 8]
    print(exponential_search(arr, len(arr), 7))
