from datetime import datetime, timedelta
from minizinc import Instance, Model, Solver

schedule = Model("./Schedule 5.0.mzn")

chuffed = Solver.lookup("chuffed")

instance = Instance(chuffed, schedule)


def get_num_days(start_date, end_date):
    date_format = "%Y-%m-%d"
    start = datetime.strptime(min(start_date), date_format)
    end = datetime.strptime(max(end_date), date_format)
    num_tasks = abs((end - start).days) + 1
    return num_tasks


def get_timeline(start_date, end_date, timeline):
    date_format = "%Y-%m-%d"
    start = datetime.strptime(min(start_date), date_format)
    end = datetime.strptime(max(end_date), date_format)
    step = timedelta(days=1)
    while start <= end:
        timeline.append(str(start.date()))
        start += step
    return timeline


def get_date_numbers(start_date, end_date, timeline, start_index, end_index):
    for i in start_date:
        s = timeline.index(i)
        start_index.append(s + 1)
    for j in end_date:
        e = timeline.index(j)
        end_index.append(e + 1)
    start_index.append(0)
    end_index.append(0)
    return start_index, end_index


def set_data(duration, priority, start_date, end_date):
    num_tasks = len(duration)
    duration.append(0)
    priority.append(0)
    timeline = []
    start = []
    end = []
    timeline = get_timeline(start_date, end_date, timeline)
    start, end = get_date_numbers(start_date, end_date, timeline, start, end)
    num_days = get_num_days(start_date, end_date)
    num_slots = 10
    return timeline, duration, priority, start, end, num_days, num_tasks, num_slots


def get_remainder_slots(num_days, num_slots, duration, tasks):
    total_time = sum(duration)
    available_slots = num_slots * num_days
    remainder_slots = available_slots - total_time
    if total_time < available_slots:
        duration[tasks] = remainder_slots
    return duration


def assignment_handler(duration, priority, start_date, end_date):
    timeline, duration, priority, start, end, num_days, num_tasks, num_slots = set_data(duration, priority, start_date,
                                                                                        end_date)
    duration = get_remainder_slots(num_days, num_slots, duration, num_tasks)
    instance["num_tasks"] = num_tasks
    instance["num_slots"] = num_slots
    instance["num_days"] = num_days
    instance["duration"] = duration
    instance["priority"] = priority
    instance["start_date"] = start
    instance["end_date"] = end
    result = instance.solve()
    result = result["schedule"]
    return timeline, result, num_tasks


def print_scheduled_tasks(timeline, results, num_tasks, title):
    for x in range(0, num_tasks):
        for i, j in enumerate(results):
            for k, l in enumerate(j):
                if l == x:
                    print(title[x], 'is scheduled on time slot ', i, ' and date ', timeline[k])


def get_scheduled_tasks(event_id, title, duration, priority, start_date, end_date):
    time_slots = ['8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM']
    scheduled_tasks = []
    timeline, results, num_tasks = assignment_handler(duration, priority, start_date, end_date)
    for x in range(0, num_tasks):
        for i, j in enumerate(results):
            for k, l in enumerate(j):
                if l == x:
                    scheduled_tasks.append({'id': event_id[x],
                                            'title': title[x],
                                            'start_time': time_slots[i],
                                            'end_time': time_slots[i+1],
                                            'date': timeline[k]})
    return scheduled_tasks
