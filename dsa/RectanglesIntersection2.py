def area_of_intersecting_triangle(interesecting_bottom_right_x, interesecting_bottom_right_y,
                                  interesecting_top_left_x, interesecting_top_left_y):
    return abs(interesecting_bottom_right_x - interesecting_top_left_x) * abs(
        interesecting_bottom_right_y - interesecting_top_left_y)


def find_intersection_rectangle_coordinates(x1, y1, x2, y2,
                                            x3, y3, x4, y4):
    # bottom right coordinates
    x5 = min(x1, x3)
    y5 = min(y1, y3)

    # top left coordinates
    x6 = max(x2, x4)
    y6 = max(y2, y4)

    if x5 < x6 or y6 < y5:
        print("rectangles don't intersect")
        return

    print("bottom right")
    print(x5, y5)  # bottom right coordinates
    print("\ntop left")
    print(x6, y6)  # top left coordinates

    # bottom left coordinates
    print("\nbottom left")
    print(x5, y6)
    # top right coordinates
    print("\ntop right")
    print(x6, y5)

    # print("are of intersecting rectangles is : " + str(
    #     area_of_intersecting_triangle(intersecting_bottom_right_x, intersecting_bottom_right_y, intersecting_top_left_x,
    #                                   intersecting_top_left_y)))


if __name__ == '__main__':
    # when bottom right cordinates and top left cordinates are given for two rectangles need to find if those
    # two rectangles intersect

    x1 = 8
    y1 = 0
    x2 = 0
    y2 = 10

    x3 = 7
    y3 = 0
    x4 = 2
    y4 = 12

    # x1 = 2
    # y1 = 0
    # x2 = 2
    # y2 = 2
    #
    # x3 = 2
    # y3 = 1
    # x4 = 2
    # y4 = 3

    find_intersection_rectangle_coordinates(x1, y1, x2, y2, x3, y3, x4, y4)
