cat results_no_attack_times_socket.txt | grep send | awk '{print $4}' > send_act_times.txt
cat results_no_attack_times_socket.txt | grep control | awk '{print $3}' > control_times.txt
cat results_no_attack_times_socket.txt | grep btw | awk '{print $3}' > between_cycles_times.txt





