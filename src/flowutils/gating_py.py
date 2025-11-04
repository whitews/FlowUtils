"""
Temporary implementation of points_in_polygon()
to troubleshoot discrepancies in latest Mac OS
versions where some test events are incorrectly
labelled. This will be removed after a solution
is found but will remain in the repo in the
'mac_num_op_testing' branch in case the issue
occurs again in the future.
"""

def point_is_left(
        point_a_x,
        point_a_y,
        point_b_x,
        point_b_y,
        test_point_x,
        test_point_y
):
    is_left = (point_b_x - point_a_x) * (test_point_y - point_a_y) - \
              (test_point_x - point_a_x) * (point_b_y - point_a_y)
    return is_left


def calc_wind_count(point_x, point_y, vert_count, poly_vertices):
    wind_count = 0

    # loop through all edges of the polygon
    for i, (vert_a_x, vert_a_y) in enumerate(poly_vertices):
        if i >= vert_count - 1:
            vert_b_x = poly_vertices[0][0]
            vert_b_y = poly_vertices[0][1]
        else:
            vert_b_x = poly_vertices[i + 1][0]
            vert_b_y = poly_vertices[i + 1][1]

        if vert_a_y <= point_y:
            if point_y < vert_b_y:
                # point crosses & edge travels upward
                is_left = point_is_left(vert_a_x, vert_a_y, vert_b_x, vert_b_y, point_x, point_y)
                # print("if is_left: %.14f" % is_left)

                if is_left > 0:
                    # point is left of edge
                    wind_count += 1  # valid 'up' intersection
        else:
            if vert_b_y <= point_y:
                # point crosses & edge travels downward
                is_left = point_is_left(vert_a_x, vert_a_y, vert_b_x, vert_b_y, point_x, point_y)
                # print("vert_a_x: %.14f" % vert_a_x)
                # print("vert_a_y: %.14f" % vert_a_y)
                # print("vert_b_x: %.14f" % vert_b_x)
                # print("vert_b_y: %.14f" % vert_b_y)
                # print("point_x: %.14f" % point_x)
                # print("point_y: %.14f" % point_y)
                # print("else is_left: %.14f" % is_left)

                if is_left < 0:
                    # point is right of edge
                    wind_count -= 1  # valid 'down' intersect

    return wind_count


def points_in_polygon(poly_vertices, points):
    """
    Determines whether points in an array are inside a polygon. Points on the
    edge of the polygon are considered inclusive. This function uses the
    winding number method and is robust to complex polygons with crossing
    boundaries, including the presence of 'holes' created by boundary crosses.

    This implementation is based on the C implementation by Dan Sunday.
    Original copyright notice:
        Copyright 2000 softSurfer, 2012 Dan Sunday

    The website containing the above implementation is no longer available,
    but was archived by the Wayback Machine. The last archived version is
    available here:

        https://web.archive.org/web/20210504233957/

    :param poly_vertices: Polygon vertices (array of 2-D points)
    :param points: Points to test for polygon inclusion
    :return: Array of winding counts for each point. True is inside polygon.
    """
    # First, find the polygon's bounding box & store the min/max values
    min_x = poly_vertices[0][0]
    max_x = poly_vertices[0][0]
    min_y = poly_vertices[0][1]
    max_y = poly_vertices[0][1]

    for i, (vert_x, vert_y) in enumerate(poly_vertices):
        if vert_x < min_x:
            min_x = vert_x
        elif vert_x > max_x:
            max_x = vert_x

        if vert_y < min_y:
            min_y = vert_y
        elif vert_y > max_y:
            max_y = vert_y

    wind_counts = []

    for i, (point_x, point_y) in enumerate(points):

        if point_x < min_x or point_x > max_x or point_y < min_y or point_y > max_y:
            wind_count = 0
        else:
            wind_count = calc_wind_count(
                point_x,
                point_y,
                len(poly_vertices),
                poly_vertices
            )

        wind_counts.append(wind_count)

    return wind_counts
