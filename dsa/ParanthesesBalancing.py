def is_balanced(expression):
    opening = tuple('{[(')
    closing = tuple('}])')
    mapping = dict(zip(opening, closing))

    queue = []

    for let in expression:
        if let in opening:
            queue.append(mapping[let])
            print(queue)
        elif let in closing:
            if not queue or let != queue.pop():
                return False
    return not queue

if __name__ == '__main__':
    balanced_state = is_balanced('{{{}}}')
    print(balanced_state)