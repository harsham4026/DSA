'''In Bubble sorting algorithm we compare the elements at the indexes i and i+1 and if the element at index i is greater
than i+1 then swap the elements and set the swapped flag to True. Initially swapped flag is declared as False.
Once this iteration is over then repeat the same action until the complete list is sorted and we check if the swapped
flag is False that is when all the list is sorted then break the loop and return the sorted array.
Time complexity in best case is Ω(n) and in the worst case is	O(n^2)'''

array_to_sort = [12, 14, 13, 15, 17, 11, 10, 9, 13, 19]
length_of_the_array = len(array_to_sort)


def main():
  i = 0

  while i < length_of_the_array - 1:
    swapped = False
    j = 0

    while j < length_of_the_array - 1:
      if array_to_sort[j] > array_to_sort[j + 1]:
        # swap the elemets and set the swapped flag to true
        array_to_sort[j], array_to_sort[j + 1] = array_to_sort[j + 1], array_to_sort[j]
        swapped = True
      j += 1

    if swapped == False:
      break

    i += 1

  return array_to_sort


if __name__ == '__main__':
  sorted_array = main()
  print(sorted_array)
