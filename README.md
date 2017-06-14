# HoneyMiniCPS

- Running the example- 
MiniCPS uses the make system to run the simulations. In our repository we have a Makefile version that adds the "final-topo" example. To make it work, copy the 'final-topo' directory into the examples directory and run 'make flowfence-cps' from the minicps directory. The controller IP is hardwired in the code (we will fix that), for now, you may change it to the address of your computer
Nevertheless, you probably wanna run the simulation running the controller in the mininet virtual machine, in that case, you would have to leave empty the IP of the controller and run pox in another terminal in the mininet virtual machine. 

- Running the controller -
To run the controller:
  2. Copy the dynamic_controller.py into the /pox/ext directory
  1. Copy the 'controller.sh' file into the pox/ directory and run './controller.sh' from the /pox directory
  
  
