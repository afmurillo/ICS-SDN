close all;
clear all;
clc

formatSpec = '%f';
fsz = 10;

reference_value(1:50)=0.40; reference_value(51:350)=0.45; reference_value(351:501)=0.40;
reference_value_2(1:70)=0.20; reference_value_2(71:400)=0.225; reference_value_2(351:501)=0.20;

ref_vector = reference_value';
ref_vector_2 = reference_value_2';

%%%%%%%%%%%%%%%%%%%%%%%%% DATA READING %%%%%%%%%%%%%%%%%%%%%%%%
% Differential Attack, no Defense
dif_attack_no_def = csvread('attack_no_def_socket/def/results_no_def_0_2.txt');
time_diff_no_def = dif_attack_no_def(:, [1]);
lit101_diff_no_def = dif_attack_no_def(:, [2]);
lit102_diff_no_def = dif_attack_no_def(:, [3]);
lit103_diff_no_def = dif_attack_no_def(:, [4]);

% Diferential Attack, Defense
dif_attack_def = csvread('atk_def_socket/def/results_def_0_2.txt');
time_diff_def = dif_attack_def(:, [1]);
lit101_diff_def = dif_attack_def(:, [2]);
lit102_diff_def = dif_attack_def(:, [3]);
lit103_diff_def = dif_attack_def(:, [4]);

% No attack
no_attack = csvread('no_attack_socket/results_thread_no_atk_socket.txt');
time_no_attack = no_attack(:, [1]);
lit101_no_attack = no_attack(:, [2]);
lit102_no_attack = no_attack(:, [3]);
lit103_no_attack = no_attack(:, [4]);

%%%%%%%%%%%%%%%%%%%%%%%% Bias parameter changes %%%%%%%%
dif_attack_0_1_no_def = csvread('attack_no_def_socket/def/results_no_def_0_1.txt');
time_diff_0_1_no_def = dif_attack_0_1_no_def(:, [1]);
lit101_diff_0_1_no_def = dif_attack_0_1_no_def(:, [2]);
lit102_diff_0_1_no_def = dif_attack_0_1_no_def(:, [3]);
lit103_diff_0_1_no_def = dif_attack_0_1_no_def(:, [4]);

dif_attack_0_3_no_def = csvread('attack_no_def_socket/def/results_no_def_0_3.txt');
time_diff_0_3_no_def = dif_attack_0_3_no_def(:, [1]);
lit101_diff_0_3_no_def = dif_attack_0_3_no_def(:, [2]);
lit102_diff_0_3_no_def = dif_attack_0_3_no_def(:, [3]);
lit103_diff_0_3_no_def = dif_attack_0_3_no_def(:, [4]);

dif_attack_0_4_no_def = csvread('attack_no_def_socket/def/results_no_def_0_4.txt');
time_diff_0_4_no_def = dif_attack_0_4_no_def(:, [1]);
lit101_diff_0_4_no_def = dif_attack_0_4_no_def(:, [2]);
lit102_diff_0_4_no_def = dif_attack_0_4_no_def(:, [3]);
lit103_diff_0_4_no_def = dif_attack_0_4_no_def(:, [4]);

dif_attack_0_5_no_def = csvread('attack_no_def_socket/def/results_no_def_0_5.txt');
time_diff_0_5_no_def = dif_attack_0_5_no_def(:, [1]);
lit101_diff_0_5_no_def = dif_attack_0_5_no_def(:, [2]);
lit102_diff_0_5_no_def = dif_attack_0_5_no_def(:, [3]);
lit103_diff_0_5_no_def = dif_attack_0_5_no_def(:, [4]);


%%%%%%%%%%%%%%% Defense %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
dif_attack_0_1_def = csvread('atk_def_socket/def/results_def_0_1.txt');
time_diff_0_1_def = dif_attack_0_1_def(:, [1]);
lit101_diff_0_1_def = dif_attack_0_1_def(:, [2]);
lit102_diff_0_1_def = dif_attack_0_1_def(:, [3]);
lit103_diff_0_1_def = dif_attack_0_1_def(:, [4]);

dif_attack_0_3_def = csvread('atk_def_socket/def/results_def_0_3.txt');
time_diff_0_3_def = dif_attack_0_3_def(:, [1]);
lit101_diff_0_3_def = dif_attack_0_3_def(:, [2]);
lit102_diff_0_3_def = dif_attack_0_3_def(:, [3]);
lit103_diff_0_3_def = dif_attack_0_3_def(:, [4]);

dif_attack_0_4_def = csvread('atk_def_socket/def/results_def_0_4.txt');
time_diff_0_4_def = dif_attack_0_4_def(:, [1]);
lit101_diff_0_4_def = dif_attack_0_4_def(:, [2]);
lit102_diff_0_4_def = dif_attack_0_4_def(:, [3]);
lit103_diff_0_4_def = dif_attack_0_4_def(:, [4]);

dif_attack_0_5_def = csvread('atk_def_socket/def/results_def_0_5.txt');
time_diff_0_5_def = dif_attack_0_5_def(:, [1]);
lit101_diff_0_5_def = dif_attack_0_5_def(:, [2]);
lit102_diff_0_5_def = dif_attack_0_5_def(:, [3]);
lit103_diff_0_5_def = dif_attack_0_5_def(:, [4]);



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
title({'Plant Behavior without Attack'});
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
title({'Plant Behavior with Bias Attack without Defense'});
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
title({'Plant Behavior with Bias Attack with Defense'});
matlab2tikz('tikz/diff_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
matlab2tikz('tikz/std_diff_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');

%%%%%%%%%%%%%%%%%%%%%%%% Errors %%%%%%%%%%%%%%%%%%%%%%%%%%%
lit_101_error_no_atk = ref_vector - lit101_no_attack;
lit_102_error_no_atk = ref_vector_2 - lit102_no_attack;

lit_101_error_diff_0_1_no_def = ref_vector - lit101_diff_0_1_no_def;
lit_102_error_diff_0_1_no_def = ref_vector_2 - lit102_diff_0_1_no_def;

lit_101_error_diff_0_2_no_def = ref_vector - lit101_diff_no_def;
lit_102_error_diff_0_2_no_def = ref_vector_2 - lit102_diff_no_def;

lit_101_error_diff_0_3_no_def = ref_vector - lit101_diff_0_3_no_def;
lit_102_error_diff_0_3_no_def = ref_vector_2 - lit102_diff_0_3_no_def;

lit_101_error_diff_0_4_no_def = ref_vector - lit101_diff_0_4_no_def;
lit_102_error_diff_0_4_no_def = ref_vector_2 - lit102_diff_0_4_no_def;

lit_101_error_diff_0_5_no_def = ref_vector - lit101_diff_0_5_no_def;
lit_102_error_diff_0_5_no_def = ref_vector_2 - lit102_diff_0_5_no_def;

% Def
lit_101_error_diff_0_1_def = ref_vector - lit101_diff_0_1_def;
lit_102_error_diff_0_1_def = ref_vector_2 - lit102_diff_0_1_def;

lit_101_error_diff_0_2_def = ref_vector - lit101_diff_def;
lit_102_error_diff_0_2_def = ref_vector_2 - lit102_diff_def;

lit_101_error_diff_0_3_def = ref_vector - lit101_diff_0_3_def;
lit_102_error_diff_0_3_def = ref_vector_2 - lit102_diff_0_3_def;

lit_101_error_diff_0_4_def = ref_vector - lit101_diff_0_4_def;
lit_102_error_diff_0_4_def = ref_vector_2 - lit102_diff_0_4_def;

lit_101_error_diff_0_5_def = ref_vector - lit101_diff_0_5_def;
lit_102_error_diff_0_5_def = ref_vector_2 - lit102_diff_0_5_def;

mean_error_no_def = zeros(1,5);
mean_error_no_def(1) = mean(lit_101_error_diff_0_1_no_def);
mean_error_no_def(2) = mean(lit_101_error_diff_0_2_no_def);
mean_error_no_def(3) = mean(lit_101_error_diff_0_3_no_def);
mean_error_no_def(4) = mean(lit_101_error_diff_0_4_no_def);
mean_error_no_def(5) = mean(lit_101_error_diff_0_5_no_def);
mean_error_no_def.*-1

mean_error_def = zeros(1,5);
mean_error_def(1) = mean(lit_101_error_diff_0_1_def);
mean_error_def(2) = mean(lit_101_error_diff_0_2_def);
mean_error_def(3) = mean(lit_101_error_diff_0_3_def);
mean_error_def(4) = mean(lit_101_error_diff_0_4_def);
mean_error_def(5) = mean(lit_101_error_diff_0_5_def);
mean_error_def.*-1

error_vector=[0.001, 0.002, 0.003, 0.004, 0.005];

h15=figure(15)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
plot(error_vector, abs(mean_error_no_def),'-.r', 'linewidth', 1.5);
hold on
plot(error_vector, abs(mean_error_def), '-b', 'linewidth', 1.5);

g = legend('Error without Defense','Error with Defense','Location','northwest');
g.FontSize = 14;
grid on
%axis([0 500 0 0.06])
grid on;
xlabel('Attack Value of Bias Attack (m)')
ylabel('Average Error(m)')
title({'Plant Mean Error with Bias Attack'});
matlab2tikz('tikz/mean_error_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
matlab2tikz('tikz/std_mean_error_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');



%%%%%%%%%%%%%%%%%%%%%%% No Defense Error Plots %%%%%%%%%%%%%%%%%%%%%%%
% h4=figure(4)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
% plot(time_diff_def, lit_101_error_no_atk,'-b', 'linewidth', 1.5);
% hold on
% plot(time_diff_def, lit_102_error_no_atk, '-.r', 'linewidth', 1.5);
% 
% g = legend('Lit101 Error','Lit102 Error','Location','northeast');
% g.FontSize = 14;
% grid on
% axis([0 500 0 0.06])
% grid on;
% xlabel('Time (s)')
% ylabel('Tank Level (m)')
% title({'Virtual Environment', 'Error without Attack'});
% matlab2tikz('tikz/error_no_atk.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% matlab2tikz('tikz/std_error_no_atk.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');
% 
% % 0.1
% h5=figure(5)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
% plot(time_diff_0_1_no_def, lit_101_error_diff_0_1_no_def,'-b', 'linewidth', 1.5);
% hold on
% plot(time_diff_0_1_no_def, lit_102_error_diff_0_1_no_def, '-.r', 'linewidth', 1.5);
% 
% g = legend('Lit101 Error','Lit102 Error','Location','northeast');
% g.FontSize = 14;
% grid on
% axis([0 500 0 0.06])
% grid on;
% xlabel('Time (s)')
% ylabel('Tank Level (m)')
% title({'Virtual Environment', 'Error with Bias Attack of 0.001 and No Defense'});
% matlab2tikz('tikz/error_0_1_no_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% matlab2tikz('tikz/std_error_0_1_no_atk.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');
% 
% 
% % 0.2
% h6=figure(6)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
% plot(time_diff_0_1_no_def, lit_101_error_diff_0_2_no_def,'-b', 'linewidth', 1.5);
% hold on
% plot(time_diff_0_1_no_def, lit_102_error_diff_0_2_no_def, '-.r', 'linewidth', 1.5);
% 
% g = legend('Lit101 Error','Lit102 Error','Location','northeast');
% g.FontSize = 14;
% grid on
% axis([0 500 0 0.06])
% grid on;
% xlabel('Time (s)')
% ylabel('Tank Level (m)')
% title({'Virtual Environment', 'Error with Bias Attack of 0.002 and No Defense'});
% matlab2tikz('tikz/error_0_2_no_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% matlab2tikz('tikz/std_error_0_2_no_atk.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');
% 
% 
% % 0.3
% h7=figure(7)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
% plot(time_diff_0_3_no_def, lit_101_error_diff_0_3_no_def,'-b', 'linewidth', 1.5);
% hold on
% plot(time_diff_0_3_no_def, lit_102_error_diff_0_3_no_def, '-.r', 'linewidth', 1.5);
% 
% g = legend('Lit101 Error','Lit102 Error','Location','northeast');
% g.FontSize = 14;
% grid on
% axis([0 500 0 0.06])
% grid on;
% xlabel('Time (s)')
% ylabel('Tank Level (m)')
% title({'Virtual Environment', 'Error with Bias Attack of 0.003 and No Defense'});
% matlab2tikz('tikz/error_0_3_no_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% matlab2tikz('tikz/std_error_0_3_no_atk.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');
% 
% 
% % 0.4
% h8=figure(8)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
% plot(time_diff_0_4_no_def, lit_101_error_diff_0_4_no_def,'-b', 'linewidth', 1.5);
% hold on
% plot(time_diff_0_4_no_def, lit_102_error_diff_0_4_no_def, '-.r', 'linewidth', 1.5);
% 
% g = legend('Lit101 Error','Lit102 Error','Location','northeast');
% g.FontSize = 14;
% grid on
% axis([0 500 0 0.06])
% grid on;
% xlabel('Time (s)')
% ylabel('Tank Level (m)')
% title({'Virtual Environment', 'Error with Bias Attack of 0.004 and No Defense'});
% matlab2tikz('tikz/error_0_4_no_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% matlab2tikz('tikz/std_error_0_4_no_atk.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');
% 
% % 0.5
% h9=figure(9)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
% plot(time_diff_0_5_no_def, lit_101_error_diff_0_5_no_def,'-b', 'linewidth', 1.5);
% hold on
% plot(time_diff_0_5_no_def, lit_102_error_diff_0_5_no_def, '-.r', 'linewidth', 1.5);
% 
% g = legend('Lit101 Error','Lit102 Error','Location','northeast');
% g.FontSize = 14;
% grid on
% axis([0 500 0 0.06])
% grid on;
% xlabel('Time (s)')
% ylabel('Tank Level (m)')
% title({'Virtual Environment', 'Error with Bias Attack of 0.005 and No Defense'});
% matlab2tikz('tikz/error_0_5_no_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% matlab2tikz('tikz/std_error_0_5_no_atk.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');
% 
% 
% 
% 
% 
% 
% %%%%%%%%%%%%%%%%%%%%%%% Defense Error Plots %%%%%%%%%%%%%%%%%%%%%%%
% % 0.1
% h10=figure(10)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
% plot(time_diff_0_1_def, lit_101_error_diff_0_1_def,'-b', 'linewidth', 1.5);
% hold on
% plot(time_diff_0_1_def, lit_102_error_diff_0_1_def, '-.r', 'linewidth', 1.5);
% 
% g = legend('Lit101 Error','Lit102 Error','Location','northeast');
% g.FontSize = 14;
% grid on
% axis([0 500 0 0.06])
% grid on;
% xlabel('Time (s)')
% ylabel('Tank Level (m)')
% title({'Virtual Environment', 'Error with Bias Attack of 0.001 and Defense'});
% matlab2tikz('tikz/error_0_1_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% matlab2tikz('tikz/std_error_0_1_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');
% 
% 
% 
% % 0.2
% h11=figure(11)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
% plot(time_diff_def, lit_101_error_diff_0_2_def,'-b', 'linewidth', 1.5);
% hold on
% plot(time_diff_def, lit_102_error_diff_0_2_def, '-.r', 'linewidth', 1.5);
% 
% g = legend('Lit101 Error','Lit102 Error','Location','northeast');
% g.FontSize = 14;
% grid on
% axis([0 500 0 0.06])
% grid on;
% xlabel('Time (s)')
% ylabel('Tank Level (m)')
% title({'Virtual Environment', 'Error with Bias Attack of 0.002 and Defense'});
% matlab2tikz('tikz/error_0_2_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% matlab2tikz('tikz/std_error_0_2_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');
% 
% 
% 
% % 0.3
% h12=figure(12)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
% plot(time_diff_def, lit_101_error_diff_0_3_def,'-b', 'linewidth', 1.5);
% hold on
% plot(time_diff_def, lit_102_error_diff_0_3_def, '-.r', 'linewidth', 1.5);
% 
% g = legend('Lit101 Error','Lit102 Error','Location','northeast');
% g.FontSize = 14;
% grid on
% axis([0 500 0 0.06])
% grid on;
% xlabel('Time (s)')
% ylabel('Tank Level (m)')
% title({'Virtual Environment', 'Error with Bias Attack of 0.003 and Defense'});
% matlab2tikz('tikz/error_0_3_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% matlab2tikz('tikz/std_error_0_3_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');
% 
% % 0.4
% h13=figure(13)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
% plot(time_diff_def, lit_101_error_diff_0_4_def,'-b', 'linewidth', 1.5);
% hold on
% plot(time_diff_def, lit_102_error_diff_0_4_def, '-.r', 'linewidth', 1.5);
% 
% g = legend('Lit101 Error','Lit102 Error','Location','northeast');
% g.FontSize = 14;
% grid on
% axis([0 500 0 0.06])
% grid on;
% xlabel('Time (s)')
% ylabel('Tank Level (m)')
% title({'Virtual Environment', 'Error with Bias Attack of 0.004 and Defense'});
% matlab2tikz('tikz/error_0_4_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% matlab2tikz('tikz/std_error_0_4_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');
% 
% 
% % 0.5
% h14=figure(14)
% set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
% plot(time_diff_def, lit_101_error_diff_0_5_def,'-b', 'linewidth', 1.5);
% hold on
% plot(time_diff_def, lit_102_error_diff_0_5_def, '-.r', 'linewidth', 1.5);
% 
% g = legend('Lit101 Error','Lit102 Error','Location','northeast');
% g.FontSize = 14;
% grid on
% axis([0 500 0 0.06])
% grid on;
% xlabel('Time (s)')
% ylabel('Tank Level (m)')
% title({'Virtual Environment', 'Error with Bias Attack of 0.005 and Defense'});
% matlab2tikz('tikz/error_0_5_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
% matlab2tikz('tikz/std_error_0_5_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height','0.5\columnwidth', 'width', '0.8\columnwidth');
% 
