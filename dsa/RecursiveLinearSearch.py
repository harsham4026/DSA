def recLinearSearch(arr, start_index, last_index, element_to_find):
    if last_index < start_index:
        return -1
    elif arr[start_index] == element_to_find:
        return start_index
    elif arr[last_index] == element_to_find:
        return last_index
    else:
        return recLinearSearch(arr, start_index + 1, last_index - 1, element_to_find)


if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5, 6, 7]
    index_of_element = recLinearSearch(arr, 0, len(arr) - 1, 7)
    print(index_of_element)
