# take the counter and iterate over the array and see if the element not equals to 0 then at the index of count put the
# value of arr[i]. In the next for loop the number of zeros we have in array is calculated as len(arr) - count.
# In the next for loop

def segregate_zeros_and_ones(arr):
    count = 0

    for i in range(len(arr)):
        if arr[i] != 0:
            arr[count] = arr[i]
            count += 1

    for i in range(count, len(arr)):
        arr[i] = 0

    return arr

def segragate_zeros_to_left_(arr):
    count = 0
    for i in range(0, len(arr)):
        if arr[i] != 0:
            arr[i] = 0
            count += 1

    print(count)
    print(len(arr))
    print(len(arr) - count)
    for i in range(len(arr) - count, len(arr)):
        arr[i] = 1

    return arr

def segragate_zeros_to_left(arr) :
    count = 0

    length = len(arr)
    new_array = [None] * length

    for i in range(length) :
        if arr[i] == 0 :
            count += 1

    for i in range(0, count) :
        new_array[i] = 0

    for i in range(length) :
        if arr[i] != 0 :
            new_array[count] = arr[i]
            count += 1

    return new_array


if __name__ == '__main__':
    arr = [0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1]
    print(segregate_zeros_and_ones(arr))
    print(segragate_zeros_to_left_(arr))

    # arr2 = [1, 2, 0, 4, 5, 0, 6, 0, 0, 0]
    # print(segragate_zeros_to_left(arr2))
