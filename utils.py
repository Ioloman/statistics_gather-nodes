def parse_time(time: str|int) -> int:
    """
    Parses string representation of a time interval
    :param time: string of integer followed (or not) by literal "m", "s", "h", "d"
    :return:
    """
    if type(time) is int:
        return time

    if time.isdigit():
        return int(time)

    if time[-1].isalpha() and time[:-1].isdigit():
        letter = time[-1]
        multiplier = 1
        if letter == 'm':
            multiplier = 60
        elif letter == 'h':
            multiplier = 60 * 60
        elif letter == 'd':
            multiplier = 60 * 60 * 24
        return int(time[:-1]) * multiplier
