'''Merge sort is basically divide and conquer algorithm. Divide the list into half and make them to left and right arrays
and split them until the length becomes 1 and sort them and merge finally.
Time complexity of O(n * log(n))'''


def merge(left, right):
    result = []
    i, j = 0, 0
    while i< len(left) and j< len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result += left[i:]
    result +=  right[j:]
    return result


def merge_sort(x):
    if len(x) <= 1:
        return x
    mid = int(len(x)/2)
    #print(mid)
    left = x[:mid]
    print(left)
    right = x[mid:]
    print(right)
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)


alist = [54, 26, 93, 17, 77, 31, 44, 55, 20]
print(merge_sort(alist))