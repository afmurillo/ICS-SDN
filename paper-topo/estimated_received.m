close all;
clear all;
clc

formatSpec = '%f';

fileID_3 = fopen('experiment_no_attack/tank_1.txt','r');
tank_1= fscanf(fileID_3,formatSpec);

fileID_2 = fopen('experiment_no_attack/tank_2.txt','r');
tank_2= fscanf(fileID_2,formatSpec);

fileID_1 = fopen('experiment_no_attack/ph.txt','r');
ph = fscanf(fileID_1,formatSpec);

fileID_4 = fopen('received.txt','r');
received = fscanf(fileID_4,formatSpec);

fileID_5 = fopen('estimated.txt','r');
estimated = fscanf(fileID_5,formatSpec);

fileID_6 = fopen('attack_no_defense_sensor/attack_tank_1.txt','r');
attack_tank_1 = fscanf(fileID_6,formatSpec);

 for i=1:length(attack_tank_1)
     if (attack_tank_1(i)) > 1.0
         attack_tank_1(i) = 1.0;
     end
 end

fileID_7 = fopen('attack_no_defense_sensor/attack_tank_2.txt','r');
attack_tank_2= fscanf(fileID_7,formatSpec);

fileID_8 = fopen('defense_experiment_compromised_sensor/defense_tank_1.txt','r');
defense_tank_1 = fscanf(fileID_8,formatSpec);

fileID_9 = fopen('defense_experiment_compromised_sensor/defense_tank_2.txt','r');
defense_tank_2= fscanf(fileID_9,formatSpec);

fileID_10 = fopen('random_no_def_tank_1.txt','r');
random_no_def_tank_1= fscanf(fileID_10,formatSpec);

fileID_11 = fopen('random_def_tank_1.txt','r');
random_def_tank_1= fscanf(fileID_11,formatSpec);

fileID_12 = fopen('second_gaussian/tank_1_no_def_0_0_2.txt','r');
                                   
noise_no_def_0_0_2= fscanf(fileID_12,formatSpec);

fileID_13 = fopen('second_gaussian/tank_1_def_0_0_2.txt','r');
noise_def_0_0_2= fscanf(fileID_13,formatSpec);
 
fileID_14 = fopen('second_gaussian/tank_1_no_def_0_0_4.txt','r');
noise_no_def_0_0_4= fscanf(fileID_14,formatSpec);

fileID_15 = fopen('second_gaussian/tank_1_def_0_0_4.txt','r');
noise_def_0_0_4= fscanf(fileID_15,formatSpec);

fileID_16 = fopen('second_gaussian/tank_1_no_def_0_0_6.txt','r');
noise_no_def_0_0_6= fscanf(fileID_16,formatSpec);

fileID_17 = fopen('second_gaussian/tank_1_def_0_0_6.txt','r');
noise_def_0_0_6= fscanf(fileID_17,formatSpec);

fileID_18 = fopen('second_gaussian/tank_1_no_def_0_0_8.txt','r');
noise_no_def_0_0_8= fscanf(fileID_18,formatSpec);

fileID_19 = fopen('second_gaussian/tank_1_def_0_0_8.txt','r');
noise_def_0_0_8= fscanf(fileID_19,formatSpec);

fileID_20 = fopen('second_gaussian/tank_1_no_def_0_1_2.txt','r');
noise_no_def_0_1_2= fscanf(fileID_20,formatSpec);

fileID_21 = fopen('second_gaussian/tank_1_def_0_1_2.txt','r');
noise_def_0_1_2= fscanf(fileID_21,formatSpec);

fileID_22 = fopen('second_gaussian/tank_1_no_def_0_1_4.txt','r');
noise_no_def_0_1_4= fscanf(fileID_22,formatSpec);

fileID_23 = fopen('second_gaussian/tank_1_def_0_1_4.txt','r');
noise_def_0_1_4= fscanf(fileID_23,formatSpec);

fileID_24 = fopen('second_gaussian/tank_1_no_def_0_1_6.txt','r');
noise_no_def_0_1_6 = fscanf(fileID_24,formatSpec);

fileID_25 = fopen('second_gaussian/tank_1_def_0_1_6.txt','r');
noise_def_0_1_6= fscanf(fileID_25,formatSpec);

fileID_26 = fopen('second_gaussian/tank_1_no_def_0_1_8.txt','r');
noise_no_def_0_1_8= fscanf(fileID_26,formatSpec);

fileID_27 = fopen('second_gaussian/tank_1_def_0_1_8.txt','r');
noise_def_0_1_8= fscanf(fileID_27,formatSpec);

fileID_28 = fopen('second_gaussian/tank_1_no_def_0_1.txt','r');
noise_no_def_0_1= fscanf(fileID_28,formatSpec);

fileID_29 = fopen('second_gaussian/tank_1_def_0_1.txt','r');
noise_def_0_1= fscanf(fileID_29,formatSpec);

fileID_30 = fopen('gaussian_noise_experiments/tank_1_no_def_0_2.txt','r');
noise_no_def_0_2= fscanf(fileID_30,formatSpec);

fileID_31 = fopen('gaussian_noise_experiments/tank_1_def_0_2.txt','r');
noise_def_0_2= fscanf(fileID_31,formatSpec);

fileID_30 = fopen('faulty_model/tank_1_def_2_0.txt','r');
faulty_def_2_0= fscanf(fileID_30,formatSpec);

fileID_31 = fopen('faulty_model/tank_1_def_2_1.txt','r');
faulty_def_2_1= fscanf(fileID_31,formatSpec);

fileID_32 = fopen('faulty_model/tank_1_def_2_2.txt','r');
faulty_def_2_2= fscanf(fileID_32,formatSpec);

fileID_33 = fopen('faulty_model/tank_1_def_2_3.txt','r');
faulty_def_2_3= fscanf(fileID_33,formatSpec);

fileID_34 = fopen('faulty_model/tank_1_def_2_4.txt','r');
faulty_def_2_4= fscanf(fileID_34,formatSpec);

% fileID_35 = fopen('faulty_model/tank_1_def_2_5.txt','r');
% faulty_def_2_5= fscanf(fileID_35,formatSpec);

fileID_36 = fopen('faulty_model/tank_1_def_2_6.txt','r');
faulty_def_2_6= fscanf(fileID_36,formatSpec);

fileID_36 = fopen('faulty_model/tank_1_def_2_7.txt','r');
faulty_def_2_7= fscanf(fileID_36,formatSpec);

fileID_37 = fopen('faulty_model/tank_1_def_2_8.txt','r');
faulty_def_2_8= fscanf(fileID_37,formatSpec);

fileID_38 = fopen('faulty_model/tank_1_def_2_9.txt','r');
faulty_def_2_9= fscanf(fileID_38,formatSpec);

fileID_39 = fopen('faulty_model/tank_1_def_3_0.txt','r');
faulty_def_3_0= fscanf(fileID_39,formatSpec);

%%%%%%%%%%%%%%%%%% Gaussian between 0.1 and 1.0 %%%%%%%%%%%%%%%%%%%%%%%%%

fileID_40 = fopen('gaussian_noise_experiments/tank_1_no_def_0_1.txt','r');                                
noise_no_def_0_1= fscanf(fileID_40,formatSpec);

fileID_41 = fopen('gaussian_noise_experiments/tank_1_def_0_1.txt','r');
noise_def_0_1= fscanf(fileID_41,formatSpec);
 
fileID_42 = fopen('gaussian_noise_experiments/tank_1_no_def_0_2.txt','r');
noise_no_def_0_2= fscanf(fileID_42,formatSpec);

fileID_43 = fopen('gaussian_noise_experiments/tank_1_def_0_2.txt','r');
noise_def_0_2= fscanf(fileID_43,formatSpec);

fileID_44 = fopen('gaussian_noise_experiments/tank_1_no_def_0_3.txt','r');
noise_no_def_0_3= fscanf(fileID_44,formatSpec);

fileID_45 = fopen('gaussian_noise_experiments/tank_1_def_0_3.txt','r');
noise_def_0_3= fscanf(fileID_45,formatSpec);

fileID_46 = fopen('gaussian_noise_experiments/tank_1_no_def_0_4.txt','r');
noise_no_def_0_4= fscanf(fileID_46,formatSpec);

fileID_47 = fopen('gaussian_noise_experiments/tank_1_def_0_4.txt','r');
noise_def_0_4= fscanf(fileID_47,formatSpec);

fileID_48 = fopen('gaussian_noise_experiments/tank_1_no_def_0_5.txt','r');
noise_no_def_0_5= fscanf(fileID_48,formatSpec);

fileID_49 = fopen('gaussian_noise_experiments/tank_1_def_0_5.txt','r');
noise_def_0_5= fscanf(fileID_49,formatSpec);

fileID_50 = fopen('gaussian_noise_experiments/tank_1_no_def_0_6.txt','r');
noise_no_def_0_6= fscanf(fileID_50,formatSpec);

fileID_51 = fopen('gaussian_noise_experiments/tank_1_def_0_6.txt','r');
noise_def_0_6= fscanf(fileID_51,formatSpec);

fileID_52 = fopen('gaussian_noise_experiments/tank_1_no_def_0_7.txt','r');
noise_no_def_0_7 = fscanf(fileID_52,formatSpec);

fileID_53 = fopen('gaussian_noise_experiments/tank_1_def_0_7.txt','r');
noise_def_0_7= fscanf(fileID_53,formatSpec);

fileID_54 = fopen('gaussian_noise_experiments/tank_1_no_def_0_8.txt','r');
noise_no_def_0_8= fscanf(fileID_54,formatSpec);

fileID_55 = fopen('gaussian_noise_experiments/tank_1_def_0_8.txt','r');
noise_def_0_8= fscanf(fileID_55,formatSpec);

fileID_56 = fopen('gaussian_noise_experiments/tank_1_no_def_0_9.txt','r');
noise_no_def_0_9= fscanf(fileID_56,formatSpec);

fileID_57 = fopen('gaussian_noise_experiments/tank_1_def_0_9.txt','r');
noise_def_0_9= fscanf(fileID_57,formatSpec);

fileID_58 = fopen('gaussian_noise_experiments/tank_1_no_def_1_0.txt','r');
noise_no_def_1_0= fscanf(fileID_58,formatSpec);

fileID_59 = fopen('gaussian_noise_experiments/tank_1_def_1_0.txt','r');
noise_def_1_0= fscanf(fileID_59,formatSpec);


% 
% fileID_32 = fopen('random_control_commands.txt','r');
% random_control_commands= fscanf(fileID_32,formatSpec);


plant_time = ([1:4001]*0.2/360)*60; % Rescaling 10
%defense_time= ([1:8001]*0.39995001249687578105473631592102/360)*15; % Rescaling 5

%ids_time = (([1:2264]*0.113171707/360)*60)*3;

fsz = 6;
fsz2 = 6;


%%%%%%%%%%%%%%%%%%%%%%%%% NORMAL OPERATION %%%%%%%%%%%%%%%%%%%%%%%%

% h1=figure(1);
% set(gca, 'FontSize', fsz, 'LineWidth', 2.0 ); 
% 
% subplot(2,1,1)
% plot(plant_time,tank_1)
% axis([0 120 0 1.25])
% grid on;
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level')
% 
% 
% subplot(2,1,2)
% plot(plant_time,tank_2)
% axis([0 120 0 1.25])
% grid on;
% 
% xlabel('Time (min)');
% ylabel('Tank 2 Level');
% 
% suptitle('Water Tank Level');
% 
% matlab2tikz('tank_levels.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');


%%%%%%%%%%%%%%%%%%%%%%%%% ATTACK NO DEFENSE %%%%%%%%%%%%%%%%%%%%%%%%

% h3=figure(3)
% set(gca, 'FontSize', fsz, 'LineWidth', 2.0 ); 
% 
% subplot(2,1,1)
% plot(plant_time,attack_tank_1)
% axis([0 120 0 1.25])
% grid on;
% 
% xlabel('Time (min)')
% ylabel('Tank 2 Level')
% 
% 
% subplot(2,1,2)
% plot(plant_time,attack_tank_2)
% axis([0 120 0 1.25])
% grid on;
% 
% xlabel('Time (min)')
% ylabel('Level')
% 
% suptitle('Water Tank 2 Level');
% 
% matlab2tikz('attack_no_defense.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');


%%%%%%%%%%%%%%%%%%%%%%%%% IDS DEFENSE %%%%%%%%%%%%%%%%%%%%%%%%

h4=figure(4)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);

hold on;
plot(plant_time,attack_tank_1, '--r', 'linewidth', 1.5);
plot(plant_time,defense_tank_1, '-b', 'linewidth', 1.5)
lg = legend('Normal Operation','Attack and No Defense ', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');

axis([0 120 0 1.2])
grid on;

plot([42 42],[0 1.2], '--k')
axis([0 120 0 1.2])

xlabel('Time (min)')
ylabel('Tank 1 Level (m)')
title('Water Tank 1 Level Behavior With Attack and IDS');

matlab2tikz('defense_1.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
saveas(h4, 'defense_1.png')
saveas(h4, 'defense_1.fig')

% h5=figure(5)
% 
% 
% %subplot(2,1,2)
% plot(plant_time,defense_tank_2)
% axis([0 120 0 1.25])
% grid on;
% 
% xlabel('Time (min)')
% ylabel('Tank 2 Level (m)')
% 
% title('Water Tank 2 Level Behavior With Attack and IDS');
% 
% 
% 
% matlab2tikz('defense_2.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');



%%%%%%%%%%%%%%%%%%%%%%%%% IDS DATA %%%%%%%%%%%%%%%%%%%%%%%%

%  h5=figure(5)
%  set(gca, 'FontSize', fsz, 'LineWidth', 2.0 ); 
%  
% plot(estimated, 'k')
% grid on;
% plot(received, 'r')
% axis([0 120 0 1.25])
% xlabel('Time (min)')
% ylabel('Tank 1 Level')
% 
% xlabel('Time (min)')
% ylabel('Tank 2 Level')
% 
% suptitle('Water Tanks Level Behavior With Attack and IDS');
% 
% matlab2tikz('ids_data.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');


%%%%%%%%%%%%%%%%%%%%%%%%% RANDOM CONTROL %%%%%%%%%%%%%%%%%%%%%%%%

h5=figure(5)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
%set(h(4),'linewidth',2.0);

%subplot(2,1,1)
%plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
plot(plant_time,random_no_def_tank_1, '-.k', 'linewidth', 1.5);

hold on;
plot(plant_time,random_def_tank_1, '--b', 'linewidth', 1.5);

axis([0 120 0 1.2])
grid on;


lg = legend('Normal Operation', 'With False Alarms', 'FontSize', 8, 'Location','southwest');
xlabel('Time (min)')
ylabel('Tank 1 Level (m)')
title('Water Tank 1 Level Behavior With Random Control Actions');

matlab2tikz('random.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
saveas(h5, 'random_experiment/random.png')
saveas(h5, 'random_experiment/random.fig')

h17=figure(17)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
delta_random = abs(random_no_def_tank_1 - random_def_tank_1);
plot(plant_time,delta_random, '-b', 'linewidth', 1.5)
 
axis([0 120 0 0.5])
grid on;
% 
xlabel('Time (min)')
ylabel('Tank 1 Level (m)')
title('Difference between Water Tank Level with and without the Defense');
 
% matlab2tikz('random_delta.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h17, 'random_experiment/random_delta.png')
% saveas(h17, 'random_experiment/random_delta.fig')

%%%%%%%%%%%%%%%%%%%%%%%%% GAUSIAN NOISE ON THE LIT101 0.12%%%%%%%%%%%%%%%%%%%%%%%%

% h6=figure(6)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% 
% plot(plant_time,noise_no_def_0_1_2, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,noise_def_0_1_2, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Gausian Noise 0.12');
% 
% matlab2tikz('second_gaussian/noise_0_1_2.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h6, 'second_gaussian/noise_0_1_2.png')
% saveas(h6, 'second_gaussian/noise_0_1_2.fig')
% 
% %%%%%%%%%%%%%%%%%%%%%%%%% GAUSIAN NOISE ON THE LIT101 0.1 %%%%%%%%%%%%%%%%%%%%%%%%
% 
% h7=figure(7)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% %plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% plot(plant_time,noise_no_def_0_1, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,noise_def_0_1, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With False Alarm', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Gausian Noise 0.1');
% 
% matlab2tikz('second_gaussian/noise_0_1.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h7, 'second_gaussian/noise_0_1.png')
% saveas(h7, 'second_gaussian/noise_0_1.fig')
% 
% % %%%%%%%%%%%%%%%%%%%%%%%% GAUSIAN NOISE ON THE LIT101 0.16 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h8=figure(8)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% %plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% plot(plant_time,noise_no_def_0_1_6, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,noise_def_0_1_6, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With False Alarm', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Gausian Noise 0.16');
% 
% matlab2tikz('second_gaussian/noise_0_1_6.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h8, 'second_gaussian/noise_0_1_6.png')
% saveas(h8, 'second_gaussian/noise_0_1_6.fig')
% 
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% GAUSIAN NOISE ON THE LIT101 0.08 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h9=figure(9)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% %plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% plot(plant_time,noise_no_def_0_0_8, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,noise_def_0_0_8, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With False Alarm', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Gausian Noise 0.08');
% 
% matlab2tikz('second_gaussian/noise_0_0_8.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h9, 'second_gaussian/noise_0_0_8.png')
% saveas(h9, 'second_gaussian/noise_0_0_8.fig')
% 
% % 
% % %%%%%%%%%%%%%%%%%%%%%%%%% GAUSIAN NOISE ON THE LIT101 0.14 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h10=figure(10)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% %plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% plot(plant_time,noise_no_def_0_1_4, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,noise_def_0_1_4, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With False Alarm', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Gausian Noise 0.14');
% 
% matlab2tikz('second_gaussian/noise_0_1_4.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h10, 'second_gaussian/noise_0_1_4.png')
% saveas(h10, 'second_gaussian/noise_0_1_4.fig')
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% GAUSIAN NOISE ON THE LIT101 0.06 %%%%%%%%%%%%%%%%%%%%%%%%
% 
% h11=figure(11)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% %plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% plot(plant_time,noise_no_def_0_0_6, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,noise_def_0_0_6, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With False Alarm', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Gausian Noise 0.06');
% 
% matlab2tikz('second_gaussian/noise_0_0_6.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h11, 'second_gaussian/noise_0_0_6.png')
% saveas(h11, 'second_gaussian/noise_0_0_6.fig')
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% GAUSIAN NOISE ON THE LIT101 0.04 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h12=figure(12)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% %plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% plot(plant_time,noise_no_def_0_0_4, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,noise_def_0_0_4, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With False Alarm', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Gausian Noise 0.04');
% 
% matlab2tikz('second_gaussian/noise_0_0_4.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h12, 'second_gaussian/noise_0_0_4.png')
% saveas(h12, 'second_gaussian/noise_0_0_4.fig')
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% GAUSIAN NOISE ON THE LIT101 0.18 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h13=figure(13)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% %plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% plot(plant_time,noise_no_def_0_1_8, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,noise_def_0_1_8, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With False Alarm', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Gausian Noise 0.18');
% 
% matlab2tikz('second_gaussian/noise_0_1_8.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h13, 'second_gaussian/noise_0_1_8.png')
% saveas(h13, 'second_gaussian/noise_0_1_8.fig')
% 
% %%%%%%%%%%%%%%%%%%%%%%%%% GAUSIAN NOISE ON THE LIT101 0.02 %%%%%%%%%%%%%%%%%%%%%%%%
% 
% h14=figure(14)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% %plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% plot(plant_time,noise_no_def_0_0_2, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,noise_def_0_0_2, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With False Alarm', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Gausian Noise 0.02');
% 
% matlab2tikz('second_gaussian/noise_0_0_2.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h14, 'second_gaussian/noise_0_0_2.png')
% saveas(h14, 'second_gaussian/noise_0_0_2.fig')
% 
% 
% % 
% % %%%%%%%%%%%%%%%%%%%%%%%%% GAUSIAN NOISE ON THE LIT101 0.2 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h15=figure(15)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% %plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% plot(plant_time,noise_no_def_0_2, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,noise_def_0_2, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With False Alarm', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Gausian Noise 0.2');
% 
% matlab2tikz('second_gaussian/noise_0_2.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h15, 'second_gaussian/noise_0_2.png')
% saveas(h15, 'second_gaussian/noise_0_2.fig')


% %%%%%%%%%%%%%%%%%%%%%%%%% FINAL GAUSSIAN NOISE FIGURE %%%%%%%%%%%%%%%%%%%%%%%%
% 
% delta=zeros(10,1)
% 
% delta(1) = mean(abs(noise_no_def_0_0_2 - noise_def_0_0_2 ));
% delta(2) = mean(abs(noise_no_def_0_0_4 - noise_def_0_0_4 ));
% delta(3) = mean(abs(noise_no_def_0_0_6 - noise_def_0_0_6 ));
% delta(4) = mean(abs(noise_no_def_0_0_8 - noise_def_0_0_8 ));
% delta(5) = mean(abs(noise_no_def_0_1 - noise_def_0_1 ));
% delta(6) = mean(abs(noise_no_def_0_1_2- noise_def_0_1_2 ));
% delta(7) = mean(abs(noise_no_def_0_1_4 - noise_def_0_1_4 ));
% delta(8) = mean(abs(noise_no_def_0_1_6 - noise_def_0_1_6 ));
% delta(9) = mean(abs(noise_no_def_0_1_8 - noise_def_0_1_8 ));
% delta(10) = mean(abs(noise_no_def_0_2 - noise_def_0_2));
% 
% sigma = [0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]
% 
% h16=figure(16)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% %plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% plot(sigma,delta, '-.k', 'linewidth', 1.5);
% 
% %lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Standard Deviation of Gaussian Noise on Sensor LIT101')
% ylabel('Water Level Error')
% title('Water Level Error between System with and without SDN Defense');
% 
% matlab2tikz('second_gaussian/total_gaussian_noise.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h16, 'second_gaussian/total_gaussian_noise.png')
% saveas(h16, 'second_gaussian/total_gaussian_noise.fig')



% %%%%%%%%%%%%%%%%%%%%%%%%% Faulty Model inlet 1 2.0 %%%%%%%%%%%%%%%%%%%%%%%%
% 
% h17=figure(17)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,faulty_def_2_0, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Faulty IDS Obersver: Inlet 2.0');
% 
% matlab2tikz('faulty_model/faulty_2_0.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h17, 'faulty_model/faulty_2_0.png')
% saveas(h17, 'faulty_model/faulty_2_0.fig')
% 
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% Faulty Model inlet 1 2.1 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h18=figure(18)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,faulty_def_2_1, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Faulty IDS Observer: Inlet 2.1');
% 
% matlab2tikz('faulty_model/faulty_2_1.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h18, 'faulty_model/faulty_2_1.png')
% saveas(h18, 'faulty_model/faulty_2_1.fig')
% 
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% Faulty Model inlet 1 2.2 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h19=figure(19)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,faulty_def_2_2, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Faulty IDS Observer: Inlet 2.2');
% 
% matlab2tikz('faulty_model/faulty_2_2.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h19, 'faulty_model/faulty_2_2.png')
% saveas(h19, 'faulty_model/faulty_2_2.fig')
% 
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% Faulty Model inlet 1 2.3 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h20=figure(20)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,faulty_def_2_3, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Faulty IDS Observer: Inlet 2.3');
% 
% matlab2tikz('faulty_model/faulty_2_3.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h20, 'faulty_model/faulty_2_3.png')
% saveas(h20, 'faulty_model/faulty_2_3.fig')
% 
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% Faulty Model inlet 1 2.4 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h21=figure(21)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,faulty_def_2_4, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Faulty IDS Observer: Inlet 2.4');
% 
% matlab2tikz('faulty_model/faulty_2_4.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h21, 'faulty_model/faulty_2_4.png')
% saveas(h21, 'faulty_model/faulty_2_4.fig')
% 
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% Faulty Model inlet 1 2.6 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h22=figure(22)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,faulty_def_2_6, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Faulty IDS Observer: Inlet 2.6');
% 
% matlab2tikz('faulty_model/faulty_2_6.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h22, 'faulty_model/faulty_2_6.png')
% saveas(h22, 'faulty_model/faulty_2_6.fig')
% 
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% Faulty Model inlet 1 2.7 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h23=figure(23)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,faulty_def_2_7, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Faulty IDS Observer: Inlet 2.7');
% 
% matlab2tikz('faulty_model/faulty_2_7.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h23, 'faulty_model/faulty_2_7.png')
% saveas(h23, 'faulty_model/faulty_2_7.fig')
% 
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% Faulty Model inlet 1 2.8 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h24=figure(24)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,faulty_def_2_8, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Faulty IDS Observer: Inlet 2.8');
% 
% matlab2tikz('faulty_model/faulty_2_8.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h24, 'faulty_model/faulty_2_8.png')
% saveas(h24, 'faulty_model/faulty_2_8.fig')
% 
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% Faulty Model inlet 1 2.9 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h25=figure(25)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,faulty_def_2_9, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Faulty IDS Observer: Inlet 2.9');
% 
% matlab2tikz('faulty_model/faulty_2_9.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h25, 'faulty_model/faulty_2_9.png')
% saveas(h25, 'faulty_model/faulty_2_9.fig')
% 
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%% Faulty Model inlet 1 3.0 %%%%%%%%%%%%%%%%%%%%%%%%
% % 
% h26=figure(26)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% %set(h(4),'linewidth',2.0);
% 
% %subplot(2,1,1)
% plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
% 
% hold on;
% plot(plant_time,faulty_def_3_0, '--b', 'linewidth', 1.5);
% 
% lg = legend('Normal Operation', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');
% 
% axis([0 120 0 1.2])
% grid on;
% 
% %plot([42 42],[0 1.2], '--k')
% %axis([0 120 0 1.2])
% 
% %annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');
% 
% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Faulty IDS Observer: Inlet 3.0');
% 
% matlab2tikz('faulty_model/faulty_3_0.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h26, 'faulty_model/faulty_3_0.png')
% saveas(h26, 'faulty_model/faulty_3_0.fig')



% %%%%%%%%%%%%%%%%%%%%%%%%% GAUSIAN NOISE ON THE LIT101 0.08 %%%%%%%%%%%%%%%%%%%%%%%%
% 
h27=figure(27)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
plot(plant_time,noise_no_def_0_1, '-.k', 'linewidth', 1.5);

hold on;
plot(plant_time,noise_def_0_1, '--b', 'linewidth', 1.5);

lg = legend('Normal Operation', 'With False Alarm', 'FontSize', 8, 'Location','southwest');

axis([0 120 0 1.2])
grid on;

xlabel('Time (min)')
ylabel('Tank 1 Level (m)')
title('Water Tank 1 Level Behavior With Gausian Noise 0.1');

% matlab2tikz('gaussian_noise_experiments/noise_0_1.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% saveas(h27, 'gaussian_noise_experiments/noise_0_1.png')
% saveas(h27, 'gaussian_noise_experiments/noise_0_1.fig')
% 


% %%%%%%%%%%%%%%%%%%%%%%%%% FINAL GAUSSIAN NOISE FIGURE %%%%%%%%%%%%%%%%%%%%%%%%
% 
delta=zeros(10,1)

delta(1) = mean(abs(noise_no_def_0_1 - noise_def_0_1 ));
delta(2) = mean(abs(noise_no_def_0_2 - noise_def_0_2 ));
delta(3) = mean(abs(noise_no_def_0_3 - noise_def_0_3 ));
delta(4) = mean(abs(noise_no_def_0_4 - noise_def_0_4 ));
delta(5) = mean(abs(noise_no_def_0_5 - noise_def_0_5 ));
delta(6) = mean(abs(noise_no_def_0_6- noise_def_0_6 ));
delta(7) = mean(abs(noise_no_def_0_7 - noise_def_0_7 ));
delta(8) = mean(abs(noise_no_def_0_8 - noise_def_0_8 ));
delta(9) = mean(abs(noise_no_def_0_9 - noise_def_0_9 ));
delta(10) = mean(abs(noise_no_def_1_0 - noise_def_1_0));

sigma = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

h50=figure(50)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
plot(sigma,delta, '-.k', 'linewidth', 1.5);

grid on;

xlabel('Standard Deviation of Gaussian Noise on Sensor LIT101')
ylabel('Delta / t ')
title('System Normal Behavior VS System Behavior with False Alarm');

matlab2tikz('gaussian_noise_experiments/gaussian_noise.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
saveas(h50, 'gaussian_noise_experiments/gaussian_noise.png')
saveas(h50, 'gaussian_noise_experiments/gaussian_noise.fig')