include "globals.mzn";   

int: num_tasks;
int: num_slots;
int: num_days;

set of int: slots = 1..num_slots;
set of int: tasks = 1..num_tasks+1;
set of int: days  = 1..num_days;

array[slots,days] of var tasks: schedule;
                             
array[tasks] of  int: duration; 
array[tasks] of  int: priority;
array[tasks] of  int: start_date;
array[tasks] of  int: end_date;

% Returns the number of occurrences of y in x .
function int: count(array[$X] of int: x, int: y);

constraint count(schedule,num_tasks + 1) = duration[num_tasks + 1];

constraint forall(c in 1..num_tasks)(count([schedule[i,j] | i in slots, j in days where j >= start_date[c] /\ j < end_date[c]], c) = duration[c]);

var set of tasks: s;
s = array2set(array1d(schedule));
var int: cost = sum([priority[i] |  i in s]);

solve maximize cost;

output[show2d(schedule)];