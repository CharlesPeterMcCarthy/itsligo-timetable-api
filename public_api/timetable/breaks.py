def FindBreaks(timetable):
    for day in timetable:
        modules = day['modules']
        if modules is None:
            day['breaks'] = None
            continue

        breaks = []
        for i in range(len(modules)):
            curModule = modules[i]
            nextModule = modules[i + 1] if i + 1 < len(modules) else None
            if nextModule and curModule['times']['end'] != nextModule['times']['start'] and curModule['times']['end'] < nextModule['times']['start']:
                breaks.append({'times': {'start': curModule['times']['end'], 'end': nextModule['times']['start']}})
        day['breaks'] = breaks
    return timetable
