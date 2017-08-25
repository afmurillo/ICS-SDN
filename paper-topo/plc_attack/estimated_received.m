close all;
clear all;
clc

formatSpec = '%f';

fileID_3 = fopen('no_attack_plc/plc_no_attack_tank_1.txt','r');
tank_1= fscanf(fileID_3,formatSpec);

fileID_2 = fopen('no_attack_plc/plc_no_attack_tank_2.txt','r');
tank_2= fscanf(fileID_2,formatSpec);

fileID_1 = fopen('no_attack_plc/plc_no_attack_ph.txt','r');
ph = fscanf(fileID_1,formatSpec);

% fileID_4 = fopen('received.txt','r');
% received = fscanf(fileID_4,formatSpec);
% 
% fileID_5 = fopen('estimated.txt','r');
% estimated = fscanf(fileID_5,formatSpec);

fileID_6 = fopen('attack/plc_attack_tank_1.txt','r');
attack_tank_1 = fscanf(fileID_6,formatSpec);
fileID_7 = fopen('attack/plc_attack_tank_2.txt','r');
attack_tank_2 = fscanf(fileID_7,formatSpec);

% 
  for i=1:length(attack_tank_2)
      if (attack_tank_2(i)) > 1.0
          attack_tank_2(i) = 1.0;
      end
  end
% 

fileID_8 = fopen('defense/plc_defense_tank_1.txt','r');
defense_tank_1 = fscanf(fileID_8,formatSpec);

fileID_9 = fopen('defense/plc_defense_tank_2.txt','r');
defense_tank_2= fscanf(fileID_9,formatSpec);

plant_time = ([1:4001]*0.2/360)*60; % Rescaling 10
%defense_time= ([1:8001]*0.39995001249687578105473631592102/360)*15; % Rescaling 5

%ids_time = (([1:2264]*0.113171707/360)*60)*3;

fsz = 6;

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
%set(h(4),'linewidth',2.0);

%subplot(2,1,1)
%plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);
plot(plant_time,tank_2, '-.k', 'linewidth', 1.5);

hold on;
plot(plant_time,attack_tank_2, '--r', 'linewidth', 1.5);
plot(plant_time,defense_tank_2, '-b', 'linewidth', 1.5)
lg = legend('Normal Operation','Attack and No Defense ', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');

axis([0 120 0 1.2])
grid on;

plot([16 16],[0 1.2], '--k')
axis([0 120 0 1.2])

%annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');

xlabel('Time (min)')
ylabel('Tank 301 Level (m)')
title('Water Tank 301 Level Behavior With Attack and IDS');

matlab2tikz('defense_plc.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');

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
