line = input()
intervals = []

while line != "":
    a, b = map(int, line.split())
    intervals.append((a, b))
    line = input()

def connect_intervals(intervals):
    if not intervals:
        return []
    
    intervals.sort()
    res = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = res[-1]
        if start <= last_end:
            res[-1] = (last_start, max(last_end, end))
        else:
            res.append((start, end))

    return res

print(connect_intervals(intervals))