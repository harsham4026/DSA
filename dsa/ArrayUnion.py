def union_of_arrays(arr1, arr2, m, n):
    result_array = []
    i = j = 0
    while i < m and j < n:
        if arr1[i] < arr2[j]:
            i += 1
        elif arr2[j] < arr1[i]:
            j += 1
        else:
            result_array.append(arr2[j])
            i += 1
            j += 1

    while i < m:
        result_array.append(arr1[i])
        i += 1
    while j < n:
        result_array.append(arr2[j])
        j += 1
    return result_array


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


def union_using_binary_search(arr1, arr2):
    union_array = []
    if (len(arr1) < len(arr2)):
        arr1.sort()
    else:
        arr2.sort()

    if len(arr1) < len(arr2):
        for i in arr1:
            if not i in union_array:
                union_array.append(i)
        for i in arr2:
            if (binary_search(arr1, i, 0, len(arr1) - 1)) == -1:
                union_array.append(i)
    else:
        for i in arr2:
            if not i in union_array:
                union_array.append(i)
        for i in arr1:
            if (binary_search(arr2, i, 0, len(arr2) - 1)) == -1:
                union_array.append(i)

    print(union_array)

if __name__ == '__main__':
    arr1 = [1, 2, 1, 1, 3]
    arr2 = [1, 1, 1, 2]
    print(union_of_arrays(arr1, arr2, len(arr1), len(arr2)))
    union_using_binary_search(arr1, arr2)
