def fib(n, arr) :

    if arr[n] is not None :
        return arr[n]

    if n == 1 or n == 2 :
        result = 1
    elif n<= 0:
        return 0
    else:
        result =  fib(n - 1, arr) + fib(n - 2, arr)

    arr[n] = result

    return result

def fib_optimized(n) :

    a = 1
    b = 1
    if n <= 0 :
        return "invalid"
    elif n == 1 or n == 2 :
        return 1
    else:
        for i in range(3, n + 1) :
            c = a + b
            a = b
            b = c
        return b


if __name__ == '__main__':
    fib_number_of_given_num = 3
    arr = [None] * (fib_number_of_given_num + 1)
    print(fib(fib_number_of_given_num, arr))
    print(fib_optimized(fib_number_of_given_num))
