import timeManagement

Event_ID = [1235, 1658, 4859, 7468, 7146, 7469]

Title = ['COMP 3608 A1', 'INFO 2606 A2', 'INFO 3606 A4', 'COMP 3601 A3', 'COMP 3602 A5', 'INFO 2604 A2']

durations = [5, 3, 7, 4, 1, 6]

priorities = [5, 1, 4, 2, 1, 3]

start_dates = ['2022-04-11', '2022-04-09', '2022-04-03', '2022-04-17', '2022-04-18', '2022-04-19']

end_dates = ['2022-04-20', '2022-04-18', '2022-04-17', '2022-04-30', '2022-05-03', '2022-05-05']

scheduled_tasks = timeManagement.get_scheduled_tasks(Event_ID, Title, durations, priorities, start_dates, end_dates)

for i in scheduled_tasks:
    print(i)


