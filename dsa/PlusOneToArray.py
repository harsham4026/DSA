def add_one(arr):
    length = len(arr)
    for i in range(length - 1, -1, -1):
        if arr[i] < 9:
            arr[i] += 1
            return arr
        # print(i)
        arr[i] = 0

    # if all the elements are 9 in the given array then create a new array with the length = len(actual array) + 1
    # then put 1 in the 0'th indec and return the new array
    result = [0] * (length + 1)
    result[0] = 1
    return result


if __name__ == '__main__':
    print(add_one([9, 9, 9]))
    print(add_one([1, 9, 9]))
    print(add_one([2, 0, 2]))
