def interval_to_tuple(interval: list[int]) -> list[tuple[int, int]]:
    return [(interval[i], interval[i + 1]) for i in range(0, len(interval), 2)]


def strip_interval(interval: list[tuple[int, int]], start: int, end: int) -> list[tuple[int, int]]:
    for i in range(len(interval)):
        start_interval, end_interval = interval[i]
        if start_interval < start:
            start_interval = start
        if end_interval > end:
            end_interval = end
        if end_interval < start_interval:
            start_interval, end_interval = -1, -1
        interval[i] = (start_interval, end_interval)

    interval = [val for val in interval if val[0] != -1 and val[1] != -1]
    return interval


def merge_interval(interval: list[tuple[int, int]]) -> list[tuple[int, int]]:
    out = []
    for pair in interval:
        if not out:
            out.append(pair)
        else:
            last_s, last_e = out[-1]
            if pair[0] <= last_e:
                out[-1] = (last_s, max(last_e, pair[1]))
            else:
                out.append(pair)
    return out


def appearance(intervals: dict[str, list[int]]) -> int:
    count = 0

    pupil_interval = interval_to_tuple(intervals['pupil'])
    tutor_interval = interval_to_tuple(intervals['tutor'])

    start_lesson, end_lesson = intervals['lesson']
    pupil_interval = strip_interval(pupil_interval, start_lesson, end_lesson)
    tutor_interval = strip_interval(tutor_interval, start_lesson, end_lesson)

    pupil_interval = merge_interval(pupil_interval)
    tutor_interval = merge_interval(tutor_interval)

    for p_start, p_end in pupil_interval:
        for t_start, t_end in tutor_interval:
            merge_start = max(p_start, t_start)
            merge_end = min(p_end, t_end)
            if merge_start > merge_end:
                continue
            count += merge_end - merge_start

    return count


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
