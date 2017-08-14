def hex_to_rgb(color):
    rgb = list(int(color[i:i+2], 16) for i in (0, 2, 4))
    return rgb


def rgb_to_hex(rgb):
    rgb_int = []
    for elem in rgb:
        rgb_int.append(int((elem + 0.002) * 255))
    rgb_int = tuple(rgb_int)
    hex_result = '%02x%02x%02x' % rgb_int
    return hex_result
