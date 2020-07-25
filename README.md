# ICS-SDN

This repository uses MiniCPS to perform different cyber security experiments using Software Defined Networking

MiniCPS uses the make system to run the simulations. In our repository we have a Makefile version with entries for each of the topologies. 
Current working and tested topologies are "paper topo" (make paper) and "francisco-topo" (make fran) 

Paper topo runs the 3 first steps of the SUTD SWaT system. The objective of that topology was testing the use of SDN technologies to mitigate cyber physical attacks on sensors or PLC equipment. That topology is part of the papers: "Leveraging Software-Defined Networking for Incident Response in Industrial Control Systems" (https://www.computer.org/csdl/magazine/so/2018/01/mso2018010044/13rRUy2YLWu) and "Virtual incident response functions in control systems" (https://www.sciencedirect.com/science/article/abs/pii/S1389128618300434)

Francisco topo runs the "3-tank system" (Three-tank System DTS200) and test the use of Luerenberg observers to mitigate cyber physical attacks agains these systems. The 3 tank system is an interesting topology because the system is non linear. That topology is part of the paper: "A Virtual Environment for Industrial Control Systems: A Nonlinear Use-Case in Attack Detection, Identification, and Response" (https://dl.acm.org/doi/10.1145/3295453.3295457)

All the code in this repository was developed during my PhD in Universidad de los Andes, Colombia and my internship at UT Dallas. My research was supported by the Colombian Administrative Department of Science, Technology, and Innovation (Colciencias), Universidad de los Andes, the U.S. Air Force Office of Scientific Research under award number FA9550-17-1-0135, anb the U.S. Department of Commerce by NIST Award 70NANB17H282 

### Running the topologies.

First copy the files of "SDN_controller" to the pox home directory. Then launch the script "run_controller"
Second, in a different console you can run "make paper" or "make fran" to launch a topology.
