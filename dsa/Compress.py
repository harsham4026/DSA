def compress(string):
    prev = None
    cons = 1
    compressed = ''
    for i in string:
        if prev:
            if prev == i:
                cons += 1
            else:
                compressed += prev + str(cons)
                cons = 1
        prev = i
    compressed += prev + str(cons)

    return compressed


def compress_2(word):
    dic_letter = {}
    for letter in word:
        if (dic_letter.get(letter) == None):
            dic_letter[letter] = 0
        else:
            dic_letter[letter] = dic_letter[letter] + 1
    return dic_letter


if __name__ == '__main__':
    string = 'asdasdssss'
    print(compress(string))
    print(compress_2(string))
