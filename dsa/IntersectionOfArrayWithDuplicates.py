def intersection_of_arrays(arr1, arr2, m, n):
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
    return result_array


def dict_approach(arr1, arr2, m, n):
    common_list = []
    dict = {}

    for i in range(m):
        if arr1[i] in dict:
            dict[arr1[i]] = dict[arr1[i]] + 1
        else:
            dict[arr1[i]] = 1

    for i in range(n):
        if arr2[i] in dict:
            common_list.append(arr2[i])

    return common_list


if __name__ == '__main__':
    arr1 = [1, 2, 1, 1, 3]
    arr2 = [1, 1, 1, 2]
    print(intersection_of_arrays(arr1, arr2, len(arr1), len(arr2)))
    print(dict_approach(arr1, arr2, len(arr1), len(arr2)))
