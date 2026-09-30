"""
hit_detection: figures out whether a click landed on a target.
"""


def check_hit(targets, click_pos):
    """
    Returns the target that was clicked, or None if the click missed
    every target.
    """

    click_x, click_y = click_pos

    for target in targets:
        dx = click_x - target.x
        dy = click_y - target.y

        if dx * dx + dy * dy <= target.radius * target.radius:
            return target

    return None