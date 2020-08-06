%% Procedure Kalman(N)
clear all;
close all;

% Nombre de points
N = 3 * 500;

% Declaration de variables
P(1:N, 1:N) = 0.0;      %
X(1:N, 1:N) = 0.0;      % Estimation des mesures
K(1:N)      = 0.0;      % Gain

% Definition de la fonction à estimer, et de son bruit
C   = 1;      % Constante a estimer
s   = 0.7;      % Ecart type du bruit

% Fonction à estimer
W(1:N)          = C;
W(N/3+1: 2*N/3) = 3;
W(2*N/3+1: N)   = 2;

% Génération des mesures bruitées
Z   = W + s * randn(1,N);

% Définition des paramètres
Q   = 1e-4;
R   = 1;

% Initialisation de l'algorithme
A       = C * ones(1, N);
P(1, 1) = 1 + Q;
X(1, 1) = C + s * randn();

% Execution de l'algorithme
t = 1;
while t < N
    X(t+1, t)   = X(t, t);
    P(t+1, t)   = P(t, t) + Q;
    t = t + 1;
    K(t)        = P(t, t-1) / (R + P(t,t-1));
    X(t, t)     = X(t, t-1) + K(t) * (Z(t) - X(t, t-1));
    P(t, t)     = P(t, t-1) - K(t) * P(t, t-1);
end

% Selection des données à afficher
Y(1:N-2)    = 0;
for i=1:N
    Y(i) = X(i, i);
end

% Affichage des résultats
figure(1);
clf;
hold on;

% Affichage des mesures
plot(1:N, Z, 'g:');

% Affichage de l'estimateur
plot(1:N, Y, 'b');

% Affichage de la consigne = fonction a estimer
plot(1:N, W, 'r');




