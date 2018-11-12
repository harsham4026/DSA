'''In Selection Sort algorithm we iterate over the list and fo each index we'll find the minimum element from the current position
and swap their positions. This continues for the entire array. Time complexity of Selection Sort in best case is Ω(n^2)	and in
worst case is O(n^2)'''

array_to_sort = [12, 14, 13, 15, 17, 11, 10, 9, 13, 19]
length_of_array = len(array_to_sort)


def main():
    i = 0
    while i < length_of_array:
        minimum_element = min(array_to_sort[i:])  # find the minimum element from the current index
        minimum_element_index = array_to_sort.index(
            minimum_element)  # take the index of the smallest element from the current index
        array_to_sort[i], array_to_sort[minimum_element_index] = array_to_sort[minimum_element_index], array_to_sort[
            i]  # swap the elements of current indexed element and the smallest indexed elememnt
        i = i + 1  # repeat it until the lenght of the array to be sorted

    return array_to_sort


if __name__ == '__main__':
    sorted_array = main()
    print(sorted_array)
