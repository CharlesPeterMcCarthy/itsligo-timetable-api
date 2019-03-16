def FindBreaks(timetable):
    for day in timetable:
        classes = day['classes']
        if classes is None:
            day['breaks'] = None
            continue

        breaks = []
        for i in range(len(classes)):
            curClass = classes[i]
            nextClass = classes[i + 1] if i + 1 < len(classes) else None
            if nextClass and curClass['times']['end'] != nextClass['times']['start'] and curClass['times']['end'] < nextClass['times']['start']:
                breaks.append({'times': {'start': curClass['times']['end'], 'end': nextClass['times']['start']}})
        day['breaks'] = breaks
    return timetable
