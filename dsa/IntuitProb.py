pairs_list = []

def get_the_pairs_with_i_lessthanj_and_arrayof_i_greater_than_arrayof_j(array_):
    length = len(array_)
    for i in range(0, length-1):
        for j in range(i+1, length-1):
            if i< j and array_[i]>array_[j]:
                pairs_list.append((array_[i], array_[j]))

    return pairs_list


ar = [5, 2, 4, 1, 3, 5]
pairs_l = get_the_pairs_with_i_lessthanj_and_arrayof_i_greater_than_arrayof_j(ar)
print(pairs_l)