'''In Insertion sorting algorithm we compare the element like compare the current indexed element with the previous elements and if previous element is greater than
the current indexed element exchange them, repeat this process until j>0 otherwise break the inner while loop and repeat the same process for rest of the elements
in the array. Time complexity of Insertion Sort in best case is Ω(n) and in the worst case is O(n^2)'''

array_to_sort = [12, 14, 13, 15, 17, 11, 10, 9, 13, 19]
length_of_the_array = len(array_to_sort)


def main():
    i = 0

    while i < length_of_the_array:
        j = array_to_sort.index(array_to_sort[i])

        # i is not the first element

        while j > 0:
            if array_to_sort[j - 1] > array_to_sort[j]:
                # swapping the elements
                array_to_sort[j - 1], array_to_sort[j] = array_to_sort[j], array_to_sort[j - 1]
            else:
                break

            j -= 1
        i += 1
    return array_to_sort


if __name__ == '__main__':
    insertion_sorted_array = main()
    print(insertion_sorted_array)
