cat lit101.txt | grep time | grep -v 0-0 | grep -v = | grep : | awk '{print $5}' > lit_101.data
