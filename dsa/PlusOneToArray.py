def add_one(arr):
    length = len(arr)
    for i in range(length - 1, -1, -1):
        # if the last element is not 9 then add 1 to it and return the array
        if arr[i] < 9:
            arr[i] += 1
            return arr
        # if it's 9 then put 0 in that position. For the next iteration the one added array will be returned if the next element is also not 9
        arr[i] = 0
    
    #if all the elements are 9 in the given array then create a new array with the length = len(actual array) + 1
    # then put 1 in the 0'th indec and return the new array
    result = [0] * (length + 1)
    result[0] = 1
    return result


if __name__ == '__main__':
    print(add_one([9, 9, 9]))
