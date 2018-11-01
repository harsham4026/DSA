def substring_search(parent_string, substring):
    flag = False

    if parent_string is None or parent_string == '':
        return flag
    if substring == '':
        flag = True
        return flag
    if substring is None:
        return flag

    counter = 0

    for charac in parent_string:
        if counter < len(substring) and charac == substring[counter]:
            counter += 1

    if counter == len(substring):
        flag = True
        return flag
    return flag


if __name__ == '__main__':
    print(substring_search('geeksforgeeks', 'geeks'))
