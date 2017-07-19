close all;
clear all;
clc

formatSpec = '%f';

%%% Experiment 1

fileID_3 = fopen('no_attack_experiment/tank_1.txt','r');
tank_1= fscanf(fileID_3,formatSpec);

fileID_2 = fopen('no_attack_experiment/tank_2.txt','r');
tank_2= fscanf(fileID_2,formatSpec);

fileID_1 = fopen('no_attack_experiment/ph.txt','r');
ph = fscanf(fileID_1,formatSpec);

%%% IDS

fileID_4 = fopen('no_attack_experiment/received.txt','r');
received = fscanf(fileID_4,formatSpec);

fileID_5 = fopen('no_attack_experiment/estimated.txt','r');
estimated = fscanf(fileID_5,formatSpec);

%%% Experiment 2

fileID_6 = fopen('attack_experiment/attack_tank_1.txt','r');
attack_tank_1 = fscanf(fileID_6,formatSpec);

fileID_7 = fopen('attack_experiment/attack_tank_2.txt','r');
attack_tank_2= fscanf(fileID_7,formatSpec);

fileID_8 = fopen('attack_experiment/defense_tank_1.txt','r');
defense_tank_1= fscanf(fileID_8,formatSpec);

for i=1:length(defense_tank_1)
    defense_tank_1(i) = defense_tank_1(i) - 0.4;
end

fileID_9 = fopen('attack_experiment/defense_tank_2.txt','r');
defense_tank_2= fscanf(fileID_9,formatSpec);

fsz = 6;
 

%%%%%%%%%%%%%%%%%%%%% Experiment 1 no atacck %%%%%%%%%%%%%%%%%%%%%%%%%%%%

h1=figure(1);
set(gca, 'FontSize', fsz, 'LineWidth', 2.0 ); 

subplot(2,1,1)
plot(tank_1(1:4000))
grid on;

xlabel('Time (s)')
ylabel('Water Tank Level')


subplot(2,1,2)
plot(tank_2(1:4000))
grid on;


suptitle('Water Tank Level Behavior Without Attack');
xlabel('Time (s)')
ylabel('Water Tank Level')

matlab2tikz('tank_levels.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');


%%%%%%%%%%%%%%%%%%%%% IDS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

h2=figure(2)
plot(received(1:1000),'k')
hold on
plot(estimated(1:1000),'r')
grid on;

xlabel('Time (s)')
ylabel('Water Tank Level')

suptitle('Luerenberg Observer');

matlab2tikz('ids_observer.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');


%%%%%%%%%%%%%%%%%%%%% Experiment 3 Attack and Defense %%%%%%%%%%%%%%%%%%%%%

h3=figure(3)
set(gca, 'FontSize', fsz, 'LineWidth', 2.0 ); 

subplot(2,1,1)
plot(attack_tank_1(1:4000), '-r')
hold on
plot(defense_tank_1(1:4000), '-b')
grid on;

xlabel('Time (s)')
ylabel('Water Tank Level')


subplot(2,1,2)
plot(attack_tank_2(1:4000), '-r')
hold on
plot(defense_tank_2(1:4000), '-b')
grid on;

xlabel('Time (s)')
ylabel('Water Tank Level')

suptitle('Water Tanks Level Behavior With Attack and IDS');

matlab2tikz('attack_experiment.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
