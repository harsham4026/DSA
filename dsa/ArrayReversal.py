def reverse_array(arr, start, end) :
    while start <= end :
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1

    return arr

def reverse_array_recursion(arr, start, end) :
    if start >= end :
        return
    arr[start], arr[end] = arr[end], arr[start]
    reverse_array_recursion(arr, start + 1, end - 1)

if __name__ == '__main__':
    arr1 = [1, 2, 3, 4, 5]
    print(reverse_array(arr1, 0, len(arr1) - 1))

    arr2 = [5, 6, 7, 8]
    reverse_array_recursion(arr2, 0, len(arr2) - 1)
    print(arr2)
