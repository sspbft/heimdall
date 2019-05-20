T = readtable("data.csv");
nodes = [6,9,12];
req_count = rot90(T{1:height(T),1});

six_exec_time = rot90(T{1:height(T),2});
nine_exec_time = rot90(T{1:height(T),3});
twelve_exec_time = rot90(T{1:height(T),4});

exec_times = [six_exec_time; nine_exec_time; twelve_exec_time;];
figure
contourf(req_count, nodes, exec_times)
colorbar
yticks(6:3:12)
xlabel('Request number')
ylabel('Number of nodes')
zlabel('Execution time')