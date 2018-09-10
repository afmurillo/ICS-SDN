close all;
clear all;
clc

formatSpec = '%f';
fsz = 10;

reference_value(1:50)=0.40;
reference_value(51:350)=0.45;
reference_value(351:501)=0.40;

reference_value_2(1:70)=0.20;
reference_value_2(71:400)=0.225;
reference_value_2(351:501)=0.20;

ref_vector = reference_value'
ref_vector_2 = reference_value_2'

%%%%%%%%%%%%%%%%%%%%%%%%% DATA READING %%%%%%%%%%%%%%%%%%%%%%%%
% Differential Attack, no Defense
dif_attack_no_def = csvread('no_def_sensor.txt');
time_diff_no_def = dif_attack_no_def(:, [1]);
lit101_diff_no_def = dif_attack_no_def(:, [2]);
lit102_diff_no_def = dif_attack_no_def(:, [3]);
lit103_diff_no_def = dif_attack_no_def(:, [4]);

% Diferential Attack, Defense
dif_attack_def = csvread('atk_def_sensor.txt');
time_diff_def = dif_attack_def(:, [1]);
lit101_diff_def = dif_attack_def(:, [2]);
lit102_diff_def = dif_attack_def(:, [3]);
lit103_diff_def = dif_attack_def(:, [4]);

% No attack
no_attack = csvread('no_atk_sensor.txt');
time_no_attack = no_attack(:, [1]);
lit101_no_attack = no_attack(:, [2]);
lit102_no_attack = no_attack(:, [3]);
lit103_no_attack = no_attack(:, [4]);

% Absolute attack, No Defense
abs_attack_no_def = csvread('abs_atk_no_def_sensor.txt');
time_abs_no_def = abs_attack_no_def(:, [1]);
lit101_abs_no_def = abs_attack_no_def(:, [2]);
lit102_abs_no_def = abs_attack_no_def(:, [3]);
lit103_abs_no_def = abs_attack_no_def(:, [4]);

% Absolute attack, Defense
abs_attack_def = csvread('abs_atk_def_sensor.txt');
time_abs_def = abs_attack_def(:, [1]);
lit101_abs_def = abs_attack_def(:, [2]);
lit102_abs_def = abs_attack_def(:, [3]);
lit103_abs_def = abs_attack_def(:, [4]);

%%%%%%%%%%%%%%%%%%%%%%%%% No Attack %%%%%%%%%%%%%%%%%%%%%%%
h1=figure(1)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
plot(time_no_attack, lit101_no_attack,'-b', 'linewidth', 1.5);
hold on
plot(time_no_attack, lit102_no_attack, '-.r', 'linewidth', 1.5);
plot(time_no_attack, lit103_no_attack, '--m', 'linewidth', 1.5);
plot(time_no_attack, ref_vector, '--k', 'linewidth', 1.5);
plot(time_no_attack, ref_vector_2, '--k', 'linewidth', 1.5);

g = legend('Tank 1 Level','Tank 2 Level','Tank 3 Level','Location','southwest');
g.FontSize = 14;
grid on
axis([20 500 0 0.5])
grid on;
xlabel('Time (s)')
ylabel('Tank Level (m)')
title({'Virtual Environment','Plant Behavior Without Attacks'});
matlab2tikz('tikz/no_attack.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
matlab2tikz('tikz/std_no_attack.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height', '0.5\columnwidth', 'width', '0.8\columnwidth');

%%%%%%%%%%%%%%%%%%%%%%%%% Differential Attack - No Defense %%%%%%%%%%%%%%%%%%%%%%%
h2=figure(2)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
plot(time_diff_no_def, lit101_diff_no_def,'-b', 'linewidth', 1.5);
hold on
plot(time_diff_no_def, lit102_diff_no_def, '-.r', 'linewidth', 1.5);
plot(time_diff_no_def, lit103_diff_no_def, '--m', 'linewidth', 1.5);
plot(time_no_attack, ref_vector, '--k', 'linewidth', 1.5);
plot(time_no_attack, ref_vector_2, '--k', 'linewidth', 1.5);

g = legend('Tank 1 Level','Tank 2 Level','Tank 3 Level','Location','southwest');
g.FontSize = 14;
grid on
axis([20 500 0 0.5])
grid on;
xlabel('Time (s)')
ylabel('Tank Level (m)')
title({'Virtual Environment','Plant Behavior With Stealth Attack without Defense'});
matlab2tikz('tikz/diff_no_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
matlab2tikz('tikz/std_diff_no_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height', '0.5\columnwidth', 'width', '0.8\columnwidth');

% %%%%%%%%%%%%%%%%%%%%%%%%% Differential Attack - Defense %%%%%%%%%%%%%%%%%%%%%%%
h3=figure(3)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
plot(time_diff_def, lit101_diff_def,'-b', 'linewidth', 1.5);
hold on
plot(time_diff_def, lit102_diff_def, '-.r', 'linewidth', 1.5);
plot(time_diff_def, lit103_diff_def, '--m', 'linewidth', 1.5);
plot(time_no_attack, ref_vector, '--k', 'linewidth', 1.5);
plot(time_no_attack, ref_vector_2, '--k', 'linewidth', 1.5);

g = legend('Tank 1 Level','Tank 2 Level','Tank 3 Level','Location','southwest');
g.FontSize = 14;
grid on
axis([20 500 0 0.5])
grid on;
xlabel('Time (s)')
ylabel('Tank Level (m)')
title({'Virtual Environment', 'Plant Behavior With Stealth Attack with Defense'});
matlab2tikz('tikz/diff_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
matlab2tikz('tikz/std_diff_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');

% %%%%%%%%%%%%%%%%%%%%%%%%% Absolute Attack - No Defense %%%%%%%%%%%%%%%%%%%%%%%
h4=figure(4)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
plot(time_abs_no_def, lit101_abs_no_def,'-b', 'linewidth', 1.5);
hold on
plot(time_abs_no_def, lit102_abs_no_def, '-.r', 'linewidth', 1.5);
plot(time_abs_no_def, lit103_abs_no_def, '--m', 'linewidth', 1.5);
plot(time_no_attack, ref_vector, '--k', 'linewidth', 1.5);
plot(time_no_attack, ref_vector_2, '--k', 'linewidth', 1.5);

g = legend('Tank 1 Level','Tank 2 Level','Tank 3 Level','Location','northwest');
g.FontSize = 14;
grid on
axis([20 450 0 0.8])
grid on;
xlabel('Time (s)')
ylabel('Tank Level (m)')
title({'Virtual Environment','Plant Behavior With Replay Attack without Defense'});
matlab2tikz('tikz/abs_no_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
matlab2tikz('tikz/std_abs_no_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height', '0.5\columnwidth', 'width', '0.8\columnwidth');

% %%%%%%%%%%%%%%%%%%%%%%%%% Absolute Attack - Defense %%%%%%%%%%%%%%%%%%%%%%%
h5=figure(5)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
plot(time_abs_def, lit101_abs_def,'-b', 'linewidth', 1.5);
hold on
plot(time_abs_def, lit102_abs_def, '-.r', 'linewidth', 1.5);
plot(time_abs_def, lit103_abs_def, '--m', 'linewidth', 1.5);
plot(time_no_attack, ref_vector, '--k', 'linewidth', 1.5);
plot(time_no_attack, ref_vector_2, '--k', 'linewidth', 1.5);

g = legend('Tank 1 Level','Tank 2 Level','Tank 3 Level','Location','southwest');
g.FontSize = 14;
grid on
axis([0 500 0 0.5])
grid on;
xlabel('Time (s)')
ylabel('Tank Level (m)')
title({'Virtual Environment','Plant Behavior With Replay Attack with Defense'});
matlab2tikz('tikz/abs_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
matlab2tikz('tikz/std_abs_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height', '0.5\columnwidth', 'width', '0.8\columnwidth');

