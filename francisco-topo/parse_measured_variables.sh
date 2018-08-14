cat faulty_model/def_3_0.txt | grep 'PH Level'| awk '{print $4}' > faulty_model/ph_def_3_0.txt
cat faulty_model/def_3_0.txt | grep 'Tank 1'| awk '{print $6}' > faulty_model/tank_1_def_3_0.txt
cat faulty_model/def_3_0.txt | grep 'Tank 2'| awk '{print $6}' > faulty_model/tank_2_def_3_0.txt

