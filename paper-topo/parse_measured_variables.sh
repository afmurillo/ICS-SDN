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
cat plc_attack.txt | grep 'Tank 2'| awk '{print $6}' > plc_attack__tank_2.txt


