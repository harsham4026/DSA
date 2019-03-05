def ubiquitous_binary_search(arr, elem_to_find):
    left = 0
    right = len(arr)

    while right - left > 1:
        m = int((left + right) / 2)

        if arr[m] <= elem_to_find:
            left = m
        else:
            right = m

    if arr[left] == elem_to_find:
        return left
    return -1


if __name__ == '__main__':
    arr = [1, 2, 3, 4, 5]
    print(ubiquitous_binary_search(arr, 5))
