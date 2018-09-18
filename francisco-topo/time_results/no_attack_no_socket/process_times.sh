cat results_no_attack_no_socket.txt | grep lit | awk 'NR%2==0' | awk '{print $4}' > lit_rec_times.txt
cat results_no_attack_no_socket.txt | grep control | awk 'NR%2==0' | awk '{print $3}' > control_times.txt
cat results_no_attack_no_socket.txt | grep btw | awk 'NR%2==0' | awk '{print $3}' > between_cycles_times.txt





