def is_balanced(expression):
    opening = tuple('{[(')
    closing = tuple('}])')
    mapping = dict(zip(opening, closing))

    queue = []

    for let in expression:
        if let in opening:
            queue.append(mapping[let])
        elif let in closing:
            if len(queue) == 0 or let != queue.pop():
                return False
    return len(queue) == 0

if __name__ == '__main__':
    balanced_state = is_balanced('{{{}}}')
    print(balanced_state)