from minizinc import Instance, Model, Solver

'''
Task    : 1 2 3 4 5 6 7
         --------------
Duration: 5 3 7 4 1 6 0
priority: 5 1 4 2 1 3 0
Start   : 1 2 4 5 3 3 0
End     : 3 4 7 7 5 6 0
'''

schedule = Model("./Schedule 5.0.mzn")

chuffed = Solver.lookup("chuffed")

instance = Instance(chuffed, schedule)

num_tasks = 6
num_slots = 10
num_days = 7
duration = [5, 3, 7, 4, 1, 6, 0]

total_time = sum(duration)
available_slots = num_slots * num_days
remainder_slots = available_slots - total_time

if total_time < available_slots:
    duration[num_tasks] = remainder_slots


instance["num_tasks"] = num_tasks
instance["num_slots"] = num_slots
instance["num_days"] = num_days

instance["duration"] = duration
instance["priority"] = [5, 1, 4, 2, 1, 3, 0]
instance["start_date"] = [1, 2, 4, 5, 3, 3, 0]
instance["end_date"] = [3, 4, 7, 7, 5, 6, 0]

result = instance.solve()
result = result["schedule"]

for i in result:
    print(i)
