%% Simulation program for Three Tanks model via Command Window
%close all
clearvars

ini_main % Initialization variables and observers design

% Signals Definition

Ts = 1; % Sampling time

% Noise definition
rng(17); % Stealthy = 7, Replay = 17, Record = 27 
n_a = 5e-6*randn(2,2001);
rng(18); % Stealthy = 8, Replay = 18, Record = 28
n_s = 5e-4*randn(2,2001)*0.1;


% Signal Input Vector
abs_inp_ref = [Y10 + zeros(1,201), 0.450 * ones(1,1300), Y10 + zeros(1,500);...
               Y20 + zeros(1,401), 0.225 * ones(1,1300), Y20 + zeros(1,300)]; 
inc_inp_ref = abs_inp_ref - [Y10; Y20];

% Attack Signals Definition

attack00 = [zeros(1,length(abs_inp_ref));...
            zeros(1,length(abs_inp_ref));...
            zeros(1,length(abs_inp_ref))];

aux1 = -10e-5 * ones(1,200);
aux2 = [zeros(1,1201),ones(1,200)];
aux3 = conv(aux1,aux2);
aux4 = [aux3(1:1401),zeros(1,600)];
        
attack01 = [zeros(1,601), -20e-3 * ones(1,200),zeros(1,length(abs_inp_ref)-801);...
            aux4;...
            zeros(1,length(abs_inp_ref))];
clear aux*

attack02 = [zeros(1,length(abs_inp_ref));...
            zeros(1,901), -20e-3 * ones(1,200),zeros(1,length(abs_inp_ref)-1101);...
            zeros(1,length(abs_inp_ref))];
        
attack03 = conv(attack01(1,:),attack01(1,:));
attack03 = [attack03(1000:3000);...
            zeros(1,length(abs_inp_ref));...
            zeros(1,length(abs_inp_ref))];

load ('stealth.mat')
att04_tim = [zeros(1,801),ones(1,200),zeros(1,1000);...
             zeros(1,1201),ones(1,200),zeros(1,600)];
% att04_tim = zeros(2,2001);
attack04 = [Scope2.*att04_tim;zeros(1,2001)];
        
% Attack selection
attack = attack04;

% Variables allocation
Scope = zeros(3,2001);
Scope1 = zeros(3,2001);
Scope2 = zeros(2,2001);
Scope3 = zeros(2,2001);
Scope4 = zeros(3,2001);
Scope5 = zeros(3,2001);
Scope6 = zeros(3,2001);
tim_det = zeros(1,2001);
tim_uio1 = zeros(1,2001);
tim_uio2 = zeros(1,2001);
Scope7 = zeros(1,2001);
Scope8 = zeros(1,2001);


% Controller settings
Current_error = [0; 0];
z = [0; 0];
x = [0; 0; 0];
xa = [0; 0; 0];
xhat = [0; 0; 0];
Prev_inc_i = [0; 0];
w1 = [0; 0; 0];
w2 = [0; 0; 0];
Prev_ya = [0; 0];
u_min = [-4e-5; -4e-5];
u_max = [5e-5; 5e-5];
x_min = zeros(3,1) - [Y10; Y20; Y30];
x_max = 0.62*ones(3,1) - [Y10; Y20; Y30];

for i = 1:length(abs_inp_ref)
    
    Current_inc_i = -[K1, K2] * [xhat; z] + n_a(i);
    Current_inc_i = sat_vec(Current_inc_i, u_min, u_max);
    Current_anom_act = [1; 1];
    Current_anom_sen = [0; 0; 0];
    sim('nl_inc_3t.mdl')
    
    Scope(:,i) = y.Data(1,1:3); % y.Data(:,[1:3]) = abs output
    Scope1(:,i) = y.Data(1,4:6); % y.Data(:,[4:6]) = inc output = inc state
    
    % Initial conditions for next simmulation step
    L1_ini = y.Data(2,1); 
    L2_ini = y.Data(2,2);
    L3_ini = y.Data(2,3);
    
    % System variables update
    x = y.Data(1,4:6)' + n_s(i); % state update (3 x 1 vector)
    ym = [1 0 0; 0 1 0] * x + n_s(i); % output update (2 x 1 vector)
    Scope2(:,i) = ym; % y output (physical variable value)
    
    % Attack on sensors
%     xa = x + attack(1:3,i); % (3 x 1 vector)
%     ya = ym + attack(1:2,i); % (2 x 1 vector)
    % Replay attacks
    if  att04_tim(1,i)==1
        xa = x;
        xa(1) = attack(1,i); % replay attack on state 1
        ya = ym;
        ya(1) = attack(1,i); % replay attack on output 1
    elseif att04_tim(2,i)==1
        xa = x;
        xa(2) = attack(2,i); % replay attack on state 2
        ya = ym;
        ya(2) = attack(2,i); % replay attack on output 2
    else
        xa = x;
        ya = ym;
    end
    Scope3(:,i) = ya; % y output with sensor attack included
        
    % Current estimator
    xhat = (Aobsv-G*Cobsv*Aobsv)*xhat + ...
           (Bobsv-G*Cobsv*Bobsv)*Prev_inc_i + G*ya;
    xhat = sat_vec(xhat,x_min,x_max);
    Scope4(:,i) = xhat; % xhat = estimation of x
    
    % UIO 1
    w1 = F1*w1 + T1*B*Prev_inc_i  + Ksp1*Prev_ya(2);
    zhat_uio1 = w1 + Hsp1*ya(2);
    Scope5(:,i) = zhat_uio1; % zhat_uio1 = estimation of x from UIO1  
    
    % UIO 2
     w2 = F2*w2 + T2*B*Prev_inc_i  + Ksp2*Prev_ya(1);
     zhat_uio2 = w2 + Hsp2*ya(1);
     Scope6(:,i) = zhat_uio2; % zhat_uio2 = estimation of x from UIO2
    
    Prev_inc_i = Current_inc_i; % update previous input
    Prev_ya = ya; % update previous ya
    
    % Luenberger residual computation - Detection
    rd = Scope3(:,i) - ssmod.C*Scope4(:,i); % Luenberger residual
    norm_rd = sqrt(rd(1)^2 + rd(2)^2);
    if norm_rd  >= Th_det
        tim_det(i) = 1;
    end
    
    % UIO residual computation - Isolation sensor 1
    ruio1 = Scope3(:,i) - ssmod.C*Scope5(:,i); % UIO1 residual
    if (abs(ruio1(1))  >= Th_uio_on && abs(ruio1(2))  <= Th_uio_off)
        tim_uio1(i) = 1;
    end
    
    % UIO residual computation - Isolation sensor 2
    ruio2 = Scope3(:,i) - ssmod.C*Scope6(:,i); % UIO1 residual
    if (abs(ruio2(1))  <= Th_uio_off && abs(ruio2(2))  >= Th_uio_on)
        tim_uio2(i) = 1;
    end
   
    %  Sensor 1 attack magnitud
    v1 = ssmod.C(1,:)*(zhat_uio1-zhat_uio2)*tim_det(i)*tim_uio1(i);
    Scope7(i) = v1; % negative of sensor 1 attack addition
    
    %  Sensor 2 attack magnitud
    v2 = ssmod.C(2,:)*(zhat_uio2-zhat_uio1)*tim_det(i)*tim_uio2(i);
    Scope8(i) = v2; % negative of sensor 2 attack addition
    
    % Error computing and integral action update
    yr = ya + [v1; v2];   
    Current_error = inc_inp_ref(:,i)  - yr;
    
    % Integral action update
    z = z + Ts * Current_error; % integrator update
    
end


% Plot of figures
n = 0:i-1;
%figure(1), plot(n,Scope(1,:),'g',n,Scope(2,:),'b',n,Scope(3,:),'r'),grid
%figure(2), plot(n,Scope1(1,:),'g',n,Scope1(2,:),'b',n,Scope1(3,:),'r'),grid
figure(3), plot(n,Scope2(1,:),'g',n,Scope2(2,:),'b'),grid
figure(4), plot(n,Scope3(1,:),'g',n,Scope3(2,:),'b'),grid
%figure(5), plot(n,Scope4(3,:),'r',n,Scope4(1,:),'g',n,Scope4(2,:),'b'),grid
%figure(6), plot(n,Scope5(1,:),'g',n,Scope5(2,:),'b',n,Scope5(3,:),'r'),grid
%figure(7), plot(n,Scope6(1,:),'g',n,Scope6(2,:),'b',n,Scope6(3,:),'r'),grid

% Luenberger residual computation off-line 
%rd = Scope3 - ssmod.C*Scope4; % Luenberger residual
%figure(8), plot(n,sqrt((rd(1,:).^2+rd(2,:).^2)),'b')

% UIO1 residual computation off-line
%rUIO1 = Scope3 - ssmod.C*Scope5; % Residual from UIO1
%figure(9), plot(n, abs(rUIO1(1,:)),'b', n, abs(rUIO1(2,:)),'r')

% UIO2 residual computation off-line
%rUIO2 = Scope3 - ssmod.C*Scope6; % Residual from UIO2
%figure(10), plot(n, abs(rUIO2(1,:)),'b', n, abs(rUIO2(2,:)),'r')
%figure(11), plot(n, Scope7,'b'), grid
%figure(12), plot(n, Scope8,'b'), grid

%figure(17), plot(n, tim_det), grid
%figure(18), plot(n, tim_uio1), grid
%figure(19), plot(n, tim_uio2), grid
 


