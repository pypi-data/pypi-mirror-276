import re

import matplotlib.axes as maxes


def split_into_paragraphs(text, collapse_whites=True):
    if collapse_whites:
        text = re.sub(r' +', ' ', text)

    ret = [para.strip().replace("\n", " ") for para in re.split('\n\n+', text)]
    return ret


def mix_borders(limit, x0, w0, left1, right1):
    right = x0 + w0
    left = max(left1, x0)
    ww = min(right, right1) - left
    return limit, left, ww


def finish_with_top(x, w,
                    x_left, x_right,
                    y_top, y_bottom):

    return [(y_top, x, w),
            mix_borders(y_bottom, x, w, x_left, x_right),
            (None, x, w),
            ]

    pass


def finish_with_bottom(x, w,
                       x_left, x_right,
                       y_bottom):

    return [mix_borders(y_bottom, x, w, x_left, x_right),
            (None, x, w)]


def write_line(ax, xy, words,
               length, width,
               fontsize, color,
               justify, widths):

    x, y = xy

    if justify == 'left' or justify == 'right':
        ax.text(x, y + (justify == 'right') * (width - length), ' '. join(words),
                fontsize=fontsize, color=color)

    elif justify == 'full':
        extra_spacing = (width - length) / (len(words) - 1)
        for word in words:
            ax.text(x, y, word,
                    fontsize=fontsize, color=color)
            x += extra_spacing + widths[word]


def parse_avoid(original_borders,
                avoid_left_of, avoid_right_of,
                height):

    if avoid_left_of is None:
        avoid_left_of = (None, (None, None))
    if avoid_right_of is None:
        avoid_right_of = (None, (None, None))

    if not isinstance(avoid_right_of, list):
        avoid_right_of = [avoid_right_of]
    if not isinstance(avoid_left_of, list):
        avoid_left_of = [avoid_left_of]

    _, xx, width = original_borders[0]

    avoids = []
    for x, (y1, y2) in avoid_left_of:
        if y2 < y1:
            y1, y2 = y2, y1
        if x is not None:
            avoids.append((x, xx + width, y1 - height, y2))
    for x, (y1, y2) in avoid_right_of:
        if y2 < y1:
            y1, y2 = y2, y1
        if x is not None:
            avoids.append((xx, x, y1 - height, y2))

    borders = original_borders

    for x_left, x_right, y_top, y_bottom in avoids:
        if y_top < y_bottom:
            y_top, y_bottom = y_bottom, y_top

        borders = add_avoid_to_borders(borders, x_left, x_right, y_top, y_bottom)

    return borders


def add_avoid_to_borders(incoming_borders, x_left, x_right, y_top, y_bottom):

    # todo: fix whenever y_top/bottom equals a value already in incoming_borders... currenlty it just adds a new field which produces misalignments

    old_borders = incoming_borders.copy()
    borders = []

    l, x, w = old_borders.pop(0)
    if l is None:
        return borders + finish_with_top(x, w, x_left, x_right, y_top, y_bottom)

    while l > y_top:
        borders.append((l, x, w))
        l, x, w = old_borders.pop(0)
        if l is None:
            return borders + finish_with_top(x, w, x_left, x_right, y_top, y_bottom)

    borders.append((y_top, x, w))
    if l > y_bottom:
        borders.append(mix_borders(l, x, w, x_left, x_right))

        l, x, w = old_borders.pop(0)
        if l is None:
            return borders + finish_with_bottom(x, w, x_left, x_right, y_bottom)

        while l > y_bottom:
            borders.append(mix_borders(l, x, w, x_left, x_right))
            l, x, w = old_borders.pop(0)
            if l is None:
                return borders + finish_with_bottom(x, w, x_left, x_right, y_bottom)

        borders.append(mix_borders(y_bottom, x, w, x_left, x_right))
        borders.append((l, x, w))
        l, x, w = old_borders.pop(0)

    else:
        borders.append((mix_borders(y_bottom, x, w, x_left, x_right)))

    while l is not None:
        borders.append((l, x, w))
        l, x, w = old_borders.pop(0)

    return borders + [(l, x, w)]
