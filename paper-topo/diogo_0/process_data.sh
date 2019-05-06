cat lit101.txt | grep time | grep -v 0-0 | grep -v = | grep : > lit_101.data
cat lit301.txt | grep time | grep -v 0-0 | grep -v = | grep : > lit_301.data
cat mv101.txt | grep command | grep -v 0-0 | grep -v = | grep : > mv_101.data
cat p101.txt | grep received | grep -v 0-0 | grep -v = > p_101.data
