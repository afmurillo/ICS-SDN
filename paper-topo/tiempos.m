close all;
clear all;
clc

formatSpec = '%f';

fileID_1 = fopen('actuator_results.txt','r');
actuator = fscanf(fileID_1,formatSpec);

fileID_2 = fopen('control_results.txt','r');
control = fscanf(fileID_2, formatSpec);
j=1;

for i=1:length(actuator)
       if actuator(i) < 150    
          new_actuador(j) = actuator(i);
          j=j+1;
       end 
end


j=1;
for i=2:length(actuator)-1
   dif_actuador(j) = actuator(i+1) - actuator(i);
   j=j+1;
end

mean_act = mean(dif_actuador) 
dev_act = std(dif_actuador)


for i=1:length(control)
       if actuator(i) < 150    
          new_control(j) = control(i);
          j=j+1;
       end 
end


j=1;
for i=2:1:length(control)-1
   dif_control(j) = control(i+1) - control(i);
   j=j+1;
end