close all;
clear all;
clc

formatSpec = '%f';
fsz = 6;

fileID_1 = fopen('results_no_atk_sensor.txt','r');
dif_attack_no_def= fscanf(fileID_1,formatSpec)


%%%%%%%%%%%%%%%%%%%%%%%%% IDS DEFENSE %%%%%%%%%%%%%%%%%%%%%%%%

% h1=figure(1)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5 ); 
% plot(plant_time,tank_1, '-.k', 'linewidth', 1.5);

% hold on;
% plot(plant_time,attack_tank_1, '--r', 'linewidth', 1.5);
% plot(plant_time,defense_tank_1, '-b', 'linewidth', 1.5)
% lg = legend('Normal Operation','Attack and No Defense ', 'With SDN Defense', 'FontSize', 8, 'Location','southwest');

% axis([0 120 0 1.2])
% grid on;

% plot([42 42],[0 1.2], '--k')
% axis([0 120 0 1.2])

%annotation('textarrow',[0.55,0.45],[0.37,0.37],'String','Attack');

% xlabel('Time (min)')
% ylabel('Tank 1 Level (m)')
% title('Water Tank 1 Level Behavior With Attack and IDS');
% 
% matlab2tikz('defense_1.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');

