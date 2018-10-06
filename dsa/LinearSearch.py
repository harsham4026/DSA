def linear_search(arr, search_element):
    for i in range(len(arr)):
        if arr[i] == search_element:
            return i
    return -1


if __name__ == '__main__':
    arr = [10, 20, 80, 30, 60, 50, 110, 100, 130, 170]
    index_of_the_element = linear_search(arr, 80)
    print("linear searched element's index {index_of_the_element}".format(index_of_the_element=index_of_the_element))
    index_of_unlisted_ele = linear_search(arr, 180)
    print("linear searched element's index which doesn't exist {index_of_unlisted_ele}".format(
        index_of_unlisted_ele=index_of_unlisted_ele))
