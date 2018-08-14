%% Parameters value of three-tank system (nonlinear)
% Hassan Noura Book page 112
mu13 = 0.5;   mu20 = 0.675; mu32 = 0.5;
S = 0.0154;   Sn = 5e-5;    W = sqrt(2*9.81);
g = 9.81;

% Output operating points (m)
Y10 = 0.400;  Y20 = 0.200;  Y30 = 0.300;

% Input operating points (m3/s)
U10 = 0.350e-004;      U20 = 0.375e-004;
Q1o = mu13*Sn*sqrt(2*g*(Y10-Y30));
%Q1o means Q1_operation = 3.5018e-5
Q2o = mu20*Sn*sqrt(2*g*Y20)-mu32*Sn*sqrt(2*g*(Y30-Y20));
%Q2o means Q2_operation = 3.1838e-5

% Initial level of tanks
% It is important to remember that linear model is a good 
% approximation, only near to the operation point
L1_ini = 0.4;     L2_ini = 0.2;     L3_ini = 0.3;
%L1_ini = 0.45;  L2_ini = 0.25;  L3_ini = 0.35;

% Tracking controller parameters
K1 = 1e-4*[21.6 3 -5; 2.9 19 -4];
K2 = 1e-4*[-0.95 -0.32; -0.30 -0.91];

% Sampling Time
Ts = 1;

%% Luenberger Current Observer Design (Only two outputs)
load('model3tmat17.mat', 'clss1')
model = clss1;

Aobsv = model.A;
Bobsv = model.B;
Cobsv = model.C([1,2],:);  %There are only two measurements available

poles_obs = 0.001*eig(model.A); % estimator poles
G = place(Aobsv',Aobsv'*Cobsv',poles_obs).';


%% UIO Bank Design (Observer without y1)
% For the design is required a model of the system (estimated)
% The design is done with the obtained model from identification

%load('model3tmat17.mat', 'clss1')
ssmod = ss(clss1.A, clss1.B, clss1.C([1,2],:), clss1.D([1,2],:), Ts);

% Procedure for UIO for output 1 and inputs 1 and 2
% C^j = C but deleting row (j=1) = Csp1
Csp1=ssmod.C(2,:); % Deleting row 1, 
E1=[1.0e-4; 1.0; 1.0e-4]; % For decoupling of sensor 1 !!! Check values!!!
C = Csp1;
Fd = E1;
A = ssmod.A;
B = ssmod.B;

% 1 a) The number of ouputs (row of C) must be greater
% than the number of unknown inputs (Column of Fd)
nb_Fd=size(Fd); nb_C=size(C); nb_row_C=nb_C(1); nb_column_Fd=nb_Fd(2);
% if (nb_column_Fd > nb_row_C),
% error(['The number of ouputs (row of C) must be ',...
%       'greater than the number of unknown inputs ',...
%       '(column of Fd)']), return
% end

% 1 b) Check the rank condition for Fd and CFd
% if (rank(C*Fd) ~= rank(Fd)),
% error('rank(C*Fd)==rank(Fd)'), return
% end


% 2) Compute H, T, and A1
nb_A=size(A); H=Fd*inv ((C*Fd)' * (C*Fd)) * (C*Fd )';
T=eye(nb_A(1))-(H*C) ; A1=T*A;

% 3) Check the observability: If (C, A1) observable,
% a UIO exists and K1 can be computed using pole placement
% if (rank(obsv(A1,C)) ~= nb_A(1)),
% error('(C, A1) should be observable' ), return
% end

% 4) Observability Similarity Transformation
[ABAR,BBAR,CBAR,TOM,KnO] = obsvf(A1,B,C); % If it is necessary
P = TOM; % similarity transformation 
Ao = ABAR(3,3);
Cstar = CBAR(1,3);
pd = 0.001;
Kpsp1 = (Ao - pd)/Cstar;
Ku1 = inv(P)*[1  1 Kpsp1]';
F1 = A1 - Ku1 * C;
Ksp1 = Ku1 + F1 * H;
Hsp1 = H;
T1 = T;

%% UIO Bank Design (Observer without y2)
% For the design is required a model of the system (estimated)
% The design is done with the obtained model from identification

%load('models3t.mat', 'clss1')
ssmod = ss(clss1.A, clss1.B, clss1.C([1,2],:), clss1.D([1,2],:), Ts);

% Procedure for UIO for output 2 and inputs 1 and 2
% C^j = C but deleting row (j=1) = Csp1
Csp2=ssmod.C(1,:); % Deleting row 2
E2=[1.0; 1.0e-4; 1.0e-4]; % For decoupling of sensor 1 !!! Check values!!!
C = Csp2;
Fd = E2;
A = ssmod.A;
B = ssmod.B;

% 1 a) The number of ouputs (row of C) must be greater
% than the number of unknown inputs (Column of Fd)
nb_Fd=size(Fd); nb_C=size(C); nb_row_C=nb_C(1); nb_column_Fd=nb_Fd(2);
% if (nb_column_Fd > nb_row_C),
% error(['The number of ouputs (row of C) must be ',...
%       'greater than the number of unknown inputs ',...
%       '(column of Fd)']), return
% end

% 1 b) Check the rank condition for Fd and CFd
% if (rank(C*Fd) ~= rank(Fd)),
% error('rank(C*Fd)==rank(Fd)'), return
% end


% 2) Compute H, T, and A1
nb_A=size(A); H=Fd*inv ((C*Fd)' * (C*Fd)) * (C*Fd )';
T=eye(nb_A(1))-(H*C) ; A1=T*A;

% 3) Check the observability: If (C, A1) observable,
% a UIO exists and K1 can be computed using pole placement
% if (rank(obsv(A1,C)) ~= nb_A(1)),
% error('(C, A1) should be observable' ), return
% end

% 4) Observability Similarity Transformation
[ABAR,BBAR,CBAR,TOM,KnO] = obsvf(A1,B,C); % If it is necessary
P = TOM; % similarity transformation 
Ao = ABAR(3,3);
Cstar = CBAR(1,3);
pd = 0.001;
Kpsp2 = (Ao - pd)/Cstar;
Ku2 = inv(P)*[1  1 Kpsp2]';
F2 = A1 - Ku2 * C;
Ksp2 = Ku2 + F2 * H;
Hsp2 = H;
T2 = T;

%%
Th_det = 6.5e-8;
Th_uio_on = 3e-3;
Th_uio_off = 1e-5;
