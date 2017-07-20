close all;
clear all;
clc

formatSpec = '%f';

%%% Experiment 1

fileID_3 = fopen('experiment_no_attack/tank_1.txt','r');
tank_1= fscanf(fileID_3,formatSpec);

fileID_2 = fopen('experiment_no_attack/tank_2.txt','r');
tank_2= fscanf(fileID_2,formatSpec);

fileID_1 = fopen('experiment_no_attack/ph.txt','r');
ph = fscanf(fileID_1,formatSpec);
fsz = 6;

fileID_4 = fopen('defense_experiment_compromised_sensor/tank_1.txt','r');
defense_tank_1= fscanf(fileID_4,formatSpec);

fileID_5 = fopen('defense_experiment_compromised_sensor/tank_2.txt','r');
defense_tank_2= fscanf(fileID_5,formatSpec);

fileID_6 = fopen('defense_experiment_compromised_sensor/ph.txt','r');
defense_ph = fscanf(fileID_6,formatSpec);



%%%%%%%%%%%%%%%%%%%%% Experiment 1 no atacck %%%%%%%%%%%%%%%%%%%%%%%%%%%%

h1=figure(1);
set(gca, 'FontSize', fsz, 'LineWidth', 2.0 ); 

subplot(2,1,1)
plot(tank_1)
grid on;

xlabel('Time (s)')
ylabel('Water Tank Level')


subplot(2,1,2)
plot(tank_2)
grid on;


suptitle('Water Tank Level Behavior Without Attack');
xlabel('Time (s)')
ylabel('Water Tank Level')

matlab2tikz('tank_levels.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');


