def area_of_intersecting_triangle(interesecting_bottom_left_x, interesecting_bottom_left_y,
                                  interesecting_top_right_x, interesecting_top_right_y):
    return abs(interesecting_top_right_y - interesecting_bottom_left_y) * abs(
        interesecting_top_right_x - interesecting_bottom_left_x)


def find_intersection_rectangle_coordinates(bottom_left_1_x, bottom_left_1_y, top_right_1_x, top_right_1_y,
                                            bottom_left_2_x, bottom_left_2_y, top_right_2_x, top_right_2_y):
    # bottom left of intersection triangle
    interesecting_bottom_left_x = max(bottom_left_1_x, bottom_left_2_x)
    interesecting_bottom_left_y = max(bottom_left_1_y, bottom_left_2_y)


    # top right of intersection triangle
    interesecting_top_right_x = min(top_right_1_x, top_right_2_x)
    interesecting_top_right_y = min(top_right_1_y, top_right_2_y)

    if interesecting_bottom_left_x > interesecting_top_right_x or interesecting_bottom_left_y > interesecting_top_right_y:
        print("given rectangles don't intersect")
        return

    print(interesecting_bottom_left_x, interesecting_bottom_left_y)  # bottom left coordinates
    print(interesecting_top_right_x, interesecting_top_right_y)  # top right coordinates

    # bottom right cordinates
    print(interesecting_bottom_left_x, interesecting_top_right_y)
    # top left cordinates
    print(interesecting_top_right_x, interesecting_bottom_left_y)

    print("are of intersecting triangle : " + str(
        area_of_intersecting_triangle(interesecting_bottom_left_x, interesecting_bottom_left_y,
                                      interesecting_top_right_x, interesecting_top_right_y)))


if __name__ == '__main__':
    # when bottom left cordinate and top right cordinates are given for two rectangles need to find if those
    # two rectangles intersect

    bottom_left_1_x = 0
    bottom_left_1_y = 0
    top_right_1_x = 10
    top_right_1_y = 8

    bottom_left_2_x = 2
    bottom_left_2_y = 3
    top_right_2_x = 7
    top_right_2_y = 9

    find_intersection_rectangle_coordinates(bottom_left_1_x, bottom_left_1_y, top_right_1_x, top_right_1_y,
                                            bottom_left_2_x, bottom_left_2_y, top_right_2_x, top_right_2_y)
