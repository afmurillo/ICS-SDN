cat paper.txt | grep 'PH Level'| awk '{print $4}' > ph.txt
cat paper.txt | grep 'Tank 1'| awk '{print $6}' > tank_1.txt
cat paper.txt | grep 'Tank 2'| awk '{print $6}' > tank_2.txt

cat defense_ids.txt | grep 'PH Level'| awk '{print $4}' > defense_ph.txt
cat defense_ids.txt | grep 'Tank 1'| awk '{print $6}' > defense_tank_1.txt
cat defense_ids.txt | grep 'Tank 2'| awk '{print $6}' > defense_tank_2.txt

cat output_ids.txt | grep "estimated" | awk '{print $4}' > estimated.txt
cat output_ids.txt | grep "received" | awk '{print $4}' > received.txt

cat plc_no_attack.txt |  grep 'PH Level'  |  awk '{print $4}' > plc_no_attack_ph.txt
cat plc_no_attack.txt | grep 'Tank 1'| awk '{print $6}' > plc_no_attack_tank_1.txt
cat plc_no_attack.txt | grep 'Tank 2'| awk '{print $6}' > plc_no_attack_tank_2.txt

cat defense_plc.txt | grep 'PH Level'| awk '{print $4}' > plc_defense_ph.txt
cat defense_plc.txt | grep 'Tank 1'| awk '{print $6}' > plc_defense_tank_1.txt
cat defense_plc.txt | grep 'Tank 2'| awk '{print $6}' > plc_defense_tank_2.txt

cat plc_attack.txt | grep 'PH Level'| awk '{print $4}' > plc_attack_ph.txt
cat plc_attack.txt | grep 'Tank 1'| awk '{print $6}' > plc_attack_tank_1.txt
cat plc_attack.txt | grep 'Tank 2'| awk '{print $6}' > plc_attack_tank_2.txt

cat random_control.txt | grep 'PH Level'| awk '{print $4}' > random_no_def_ph.txt
cat random_control.txt | grep 'Tank 1'| awk '{print $6}' > random_no_def_tank_1.txt
cat random_control.txt | grep 'Tank 2'| awk '{print $6}' > random_no_def_tank_2.txt


cat random_control_def.txt | grep 'PH Level'| awk '{print $4}' > random_def_ph.txt
cat random_control_def.txt | grep 'Tank 1'| awk '{print $6}' > random_def_tank_1.txt
cat random_control_def.txt | grep 'Tank 2'| awk '{print $6}' > random_def_tank_2.txt

cat gaussian_noise_experiments/no_def_0_5.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_no_def_0_5.txt
cat gaussian_noise_experiments/no_def_0_5.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_no_def_0_5.txt
cat gaussian_noise_experiments/no_def_0_5.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_no_def_0_5.txt

cat gaussian_noise_experiments/def_0_5.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_def_0_5.txt
cat gaussian_noise_experiments/def_0_5.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_def_0_5.txt
cat gaussian_noise_experiments/def_0_5.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_def_0_5.txt

cat gaussian_noise_experiments/no_def_1_0.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_no_def_1_0.txt
cat gaussian_noise_experiments/no_def_1_0.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_no_def_1_0.txt
cat gaussian_noise_experiments/no_def_1_0.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_no_def_1_0.txt

cat gaussian_noise_experiments/def_1_0.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_def_1_0.txt
cat gaussian_noise_experiments/def_1_0.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_def_1_0.txt
cat gaussian_noise_experiments/def_1_0.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_def_1_0.txt

cat gaussian_noise_experiments/no_def_0_7.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_no_def_0_7.txt
cat gaussian_noise_experiments/no_def_0_7.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_no_def_0_7.txt
cat gaussian_noise_experiments/no_def_0_7.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_no_def_0_7.txt

cat gaussian_noise_experiments/def_0_7.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_def_0_7.txt
cat gaussian_noise_experiments/def_0_7.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_def_0_7.txt
cat gaussian_noise_experiments/def_0_7.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_def_0_7.txt

cat gaussian_noise_experiments/no_def_0_8.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_no_def_0_8.txt
cat gaussian_noise_experiments/no_def_0_8.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_no_def_0_8.txt
cat gaussian_noise_experiments/no_def_0_8.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_no_def_0_8.txt

cat gaussian_noise_experiments/def_0_8.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_def_0_8.txt
cat gaussian_noise_experiments/def_0_8.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_def_0_8.txt
cat gaussian_noise_experiments/def_0_8.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_def_0_8.txt

cat gaussian_noise_experiments/no_def_0_6.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_no_def_0_6.txt
cat gaussian_noise_experiments/no_def_0_6.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_no_def_0_6.txt
cat gaussian_noise_experiments/no_def_0_6.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_no_def_0_6.txt

cat gaussian_noise_experiments/def_0_6.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_def_0_6.txt
cat gaussian_noise_experiments/def_0_6.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_def_0_6.txt
cat gaussian_noise_experiments/def_0_6.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_def_0_6.txt

cat gaussian_noise_experiments/no_def_0_4.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_no_def_0_4.txt
cat gaussian_noise_experiments/no_def_0_4.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_no_def_0_4.txt
cat gaussian_noise_experiments/no_def_0_4.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_no_def_0_4.txt

cat gaussian_noise_experiments/def_0_4.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_def_0_4.txt
cat gaussian_noise_experiments/def_0_4.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_def_0_4.txt
cat gaussian_noise_experiments/def_0_4.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_def_0_4.txt

cat gaussian_noise_experiments/no_def_0_3.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_no_def_0_3.txt
cat gaussian_noise_experiments/no_def_0_3.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_no_def_0_3.txt
cat gaussian_noise_experiments/no_def_0_3.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_no_def_0_3.txt

cat gaussian_noise_experiments/def_0_3.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_def_0_3.txt
cat gaussian_noise_experiments/def_0_3.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_def_0_3.txt
cat gaussian_noise_experiments/def_0_3.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_def_0_3.txt

cat gaussian_noise_experiments/no_def_0_9.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_no_def_0_9.txt
cat gaussian_noise_experiments/no_def_0_9.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_no_def_0_9.txt
cat gaussian_noise_experiments/no_def_0_9.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_no_def_0_9.txt

cat gaussian_noise_experiments/def_0_9.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_def_0_9.txt
cat gaussian_noise_experiments/def_0_9.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_def_0_9.txt
cat gaussian_noise_experiments/def_0_9.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_def_0_9.txt

cat gaussian_noise_experiments/no_def_0_2.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_no_def_0_2.txt
cat gaussian_noise_experiments/no_def_0_2.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_no_def_0_2.txt
cat gaussian_noise_experiments/no_def_0_2.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_no_def_0_2.txt

cat gaussian_noise_experiments/def_0_2.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_def_0_2.txt
cat gaussian_noise_experiments/def_0_2.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_def_0_2.txt
cat gaussian_noise_experiments/def_0_2.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_def_0_2.txt

cat gaussian_noise_experiments/no_def_0_1.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_no_def_0_1.txt
cat gaussian_noise_experiments/no_def_0_1.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_no_def_0_1.txt
cat gaussian_noise_experiments/no_def_0_1.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_no_def_0_1.txt

cat gaussian_noise_experiments/def_0_1.txt | grep 'PH Level'| awk '{print $4}' > gaussian_noise_experiments/ph_def_0_1.txt
cat gaussian_noise_experiments/def_0_1.txt | grep 'Tank 1'| awk '{print $6}' > gaussian_noise_experiments/tank_1_def_0_1.txt
cat gaussian_noise_experiments/def_0_1.txt | grep 'Tank 2'| awk '{print $6}' > gaussian_noise_experiments/tank_2_def_0_1.txt

# Second Gaussian
cat second_gaussian/def_0_1.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_def_0_1.txt
cat second_gaussian/def_0_1.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_def_0_1.txt
cat second_gaussian/def_0_1.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_def_0_1.txt

cat second_gaussian/no_def_0_2.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_no_def_0_0_2.txt
cat second_gaussian/no_def_0_2.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_no_def_0_0_2.txt
cat second_gaussian/no_def_0_2.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_no_def_0_0_2.txt

cat second_gaussian/def_0_0_2.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_def_0_0_2.txt
cat second_gaussian/def_0_0_2.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_def_0_0_2.txt
cat second_gaussian/def_0_0_2.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_def_0_0_2.txt

cat second_gaussian/no_def_0_0_4.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_no_def_0_0_4.txt
cat second_gaussian/no_def_0_0_4.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_no_def_0_0_4.txt
cat second_gaussian/no_def_0_0_4.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_no_def_0_0_4.txt

cat second_gaussian/def_0_0_4.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_def_0_0_4.txt
cat second_gaussian/def_0_0_4.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_def_0_0_4.txt
cat second_gaussian/def_0_0_4.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_def_0_0_4.txt

cat second_gaussian/no_def_0_0_6.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_no_def_0_0_6.txt
cat second_gaussian/no_def_0_0_6.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_no_def_0_0_6.txt
cat second_gaussian/no_def_0_0_6.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_no_def_0_0_6.txt

cat second_gaussian/def_0_0_6.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_def_0_0_6.txt
cat second_gaussian/def_0_0_6.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_def_0_0_6.txt
cat second_gaussian/def_0_0_6.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_def_0_0_6.txt

cat second_gaussian/no_def_0_0_8.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_no_def_0_0_8.txt
cat second_gaussian/no_def_0_0_8.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_no_def_0_0_8.txt
cat second_gaussian/no_def_0_0_8.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_no_def_0_0_8.txt

cat second_gaussian/def_0_0_8.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_def_0_0_8.txt
cat second_gaussian/def_0_0_8.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_def_0_0_8.txt
cat second_gaussian/def_0_0_8.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_def_0_0_8.txt

cat second_gaussian/no_def_0_1_2.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_no_def_0_1_2.txt
cat second_gaussian/no_def_0_1_2.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_no_def_0_1_2.txt
cat second_gaussian/no_def_0_1_2.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_no_def_0_1_2.txt

cat second_gaussian/def_0_1_2.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_def_0_1_2.txt
cat second_gaussian/def_0_1_2.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_def_0_1_2.txt
cat second_gaussian/def_0_1_2.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_def_0_1_2.txt

cat second_gaussian/no_def_0_1_4.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_no_def_0_1_4.txt
cat second_gaussian/no_def_0_1_4.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_no_def_0_1_4.txt
cat second_gaussian/no_def_0_1_4.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_no_def_0_1_4.txt

cat second_gaussian/def_0_1_4.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_def_0_1_4.txt
cat second_gaussian/def_0_1_4.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_def_0_1_4.txt
cat second_gaussian/def_0_1_4.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_def_0_1_4.txt

cat second_gaussian/no_def_0_1_6.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_no_def_0_1_6.txt
cat second_gaussian/no_def_0_1_6.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_no_def_0_1_6.txt
cat second_gaussian/no_def_0_1_6.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_no_def_0_1_6.txt

cat second_gaussian/def_0_1_6.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_def_0_1_6.txt
cat second_gaussian/def_0_1_6.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_def_0_1_6.txt
cat second_gaussian/def_0_1_6.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_def_0_1_6.txt

cat second_gaussian/no_def_0_1_8.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_no_def_0_1_8.txt
cat second_gaussian/no_def_0_1_8.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_no_def_0_1_8.txt
cat second_gaussian/no_def_0_1_8.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_no_def_0_1_8.txt

cat second_gaussian/def_0_1_8.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_def_0_1_8.txt
cat second_gaussian/def_0_1_8.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_def_0_1_8.txt
cat second_gaussian/def_0_1_8.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_def_0_1_8.txt

cat second_gaussian/no_def_0_1.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_no_def_0_1.txt
cat second_gaussian/no_def_0_1.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_no_def_0_1.txt
cat second_gaussian/no_def_0_1.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_no_def_0_1.txt

cat second_gaussian/def_0_1.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_def_0_1.txt
cat second_gaussian/def_0_1.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_def_0_1.txt
cat second_gaussian/def_0_1.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_def_0_1.txt

cat second_gaussian/no_def_0_2.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_no_def_0_2.txt
cat second_gaussian/no_def_0_2.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_no_def_0_2.txt
cat second_gaussian/no_def_0_2.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_no_def_0_2.txt

cat second_gaussian/def_0_2.txt | grep 'PH Level'| awk '{print $4}' > second_gaussian/ph_def_0_2.txt
cat second_gaussian/def_0_2.txt | grep 'Tank 1'| awk '{print $6}' > second_gaussian/tank_1_def_0_2.txt
cat second_gaussian/def_0_2.txt | grep 'Tank 2'| awk '{print $6}' > second_gaussian/tank_2_def_0_2.txt

# Faulty Model

cat faulty_model/def_2_0.txt | grep 'PH Level'| awk '{print $4}' > faulty_model/ph_def_2_0.txt
cat faulty_model/def_2_0.txt | grep 'Tank 1'| awk '{print $6}' > faulty_model/tank_1_def_2_0.txt
cat faulty_model/def_2_0.txt | grep 'Tank 2'| awk '{print $6}' > faulty_model/tank_2_def_2_0.txt

cat faulty_model/def_2_1.txt | grep 'PH Level'| awk '{print $4}' > faulty_model/ph_def_2_1.txt
cat faulty_model/def_2_1.txt | grep 'Tank 1'| awk '{print $6}' > faulty_model/tank_1_def_2_1.txt
cat faulty_model/def_2_1.txt | grep 'Tank 2'| awk '{print $6}' > faulty_model/tank_2_def_2_1.txt

cat faulty_model/def_2_2.txt | grep 'PH Level'| awk '{print $4}' > faulty_model/ph_def_2_2.txt
cat faulty_model/def_2_2.txt | grep 'Tank 1'| awk '{print $6}' > faulty_model/tank_1_def_2_2.txt
cat faulty_model/def_2_2.txt | grep 'Tank 2'| awk '{print $6}' > faulty_model/tank_2_def_2_2.txt

cat faulty_model/def_2_3.txt | grep 'PH Level'| awk '{print $4}' > faulty_model/ph_def_2_3.txt
cat faulty_model/def_2_3.txt | grep 'Tank 1'| awk '{print $6}' > faulty_model/tank_1_def_2_3.txt
cat faulty_model/def_2_3.txt | grep 'Tank 2'| awk '{print $6}' > faulty_model/tank_2_def_2_3.txt

cat faulty_model/def_2_4.txt | grep 'PH Level'| awk '{print $4}' > faulty_model/ph_def_2_4.txt
cat faulty_model/def_2_4.txt | grep 'Tank 1'| awk '{print $6}' > faulty_model/tank_1_def_2_4.txt
cat faulty_model/def_2_4.txt | grep 'Tank 2'| awk '{print $6}' > faulty_model/tank_2_def_2_4.txt

cat faulty_model/def_2_6.txt | grep 'PH Level'| awk '{print $4}' > faulty_model/ph_def_2_6.txt
cat faulty_model/def_2_6.txt | grep 'Tank 1'| awk '{print $6}' > faulty_model/tank_1_def_2_6.txt
cat faulty_model/def_2_6.txt | grep 'Tank 2'| awk '{print $6}' > faulty_model/tank_2_def_2_6.txt

cat faulty_model/def_2_7.txt | grep 'PH Level'| awk '{print $4}' > faulty_model/ph_def_2_7.txt
cat faulty_model/def_2_7.txt | grep 'Tank 1'| awk '{print $6}' > faulty_model/tank_1_def_2_7.txt
cat faulty_model/def_2_7.txt | grep 'Tank 2'| awk '{print $6}' > faulty_model/tank_2_def_2_7.txt

cat faulty_model/def_2_8.txt | grep 'PH Level'| awk '{print $4}' > faulty_model/ph_def_2_8.txt
cat faulty_model/def_2_8.txt | grep 'Tank 1'| awk '{print $6}' > faulty_model/tank_1_def_2_8.txt
cat faulty_model/def_2_8.txt | grep 'Tank 2'| awk '{print $6}' > faulty_model/tank_2_def_2_8.txt

cat faulty_model/def_2_9.txt | grep 'PH Level'| awk '{print $4}' > faulty_model/ph_def_2_9.txt
cat faulty_model/def_2_9.txt | grep 'Tank 1'| awk '{print $6}' > faulty_model/tank_1_def_2_9.txt
cat faulty_model/def_2_9.txt | grep 'Tank 2'| awk '{print $6}' > faulty_model/tank_2_def_2_9.txt

cat faulty_model/def_3_0.txt | grep 'PH Level'| awk '{print $4}' > faulty_model/ph_def_3_0.txt
cat faulty_model/def_3_0.txt | grep 'Tank 1'| awk '{print $6}' > faulty_model/tank_1_def_3_0.txt
cat faulty_model/def_3_0.txt | grep 'Tank 2'| awk '{print $6}' > faulty_model/tank_2_def_3_0.txt

