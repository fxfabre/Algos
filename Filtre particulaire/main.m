clear all;
close all;

%%
%chargement des données
load data.mat
temps = t;
clear t;

N = size (temps,2);
w = randn(N,1);
v = sqrt(10)*randn(N,1);

%x(0)=10*randn(1);

%% Question 1 Likewood
% z = g(w) + w,
% w ~ N(0, 1)
% d'ou z|x ~ N( g(x), 1)
z   = zeros(N, 1);
for i = 1:N
    z(i)= g(x(i)) + w(i);
end

%% Question 2
% De même p(x(t+1))|x(t)) suit la loi N( f(x,t), 1)

%% Question 3
% Algo PF, bootstrap

N_part  = 50;
xt      = sqrt(10)*randn(N_part,1);
xtplus1 = zeros(N_part,1);
N_lim   = N_part / 2;
wt      = ones(N_part,1)./N_part;
wtplus1 = zeros(N_part,1);

position= zeros(N, 1);

for t = 1:N
    for i=1:N_part
        xtplus1(i) = f(xt(i), temps(t))+ sqrt(10) * randn(1);
        wtplus1(i)  = abs(wt(i)*( g( xtplus1(i) ) + randn(1) ));
    end
    
    W = sum(wtplus1);
    wtplus1 = wtplus1./W;
    Ntplus1 = 1/norm(wtplus1);

    if Ntplus1 < N_lim
        xtplus1 = resample(xtplus1, wtplus1, N_part);
    end

    xt=xtplus1;
    wt=wtplus1;

    position(t) = mean( xt );
end
fprintf('Algorithme PF, bootstrap terminé \n');

%%
figure (1);
clf;
plot(xt,wt, '.');

%%
figure(2);
plot(temps, x, 'r');
hold on;
plot(temps, position, 'b');

%%
% L'algo marche pas trop mal, mais les poids sont tous nuls, sauf un qui
% vaut 1. L'algorithme de resampling n'a donc pas l'air de fonctionner
% correctement.
% On obtient quand même un résultat satisfaisant. On remarque quand meme
% que les données traitées restent très bruitées, et que l'algorithme est
% un peu long à suivre la trajectoire lors d'une variation brusque. 

%%
% On va essayer de modifier les poids avec une fonction non linéaire, qui
% augmente les petites valeurs, et réduit les différences entre 2 valeurs
% pour les valeurs > 1  => fonction racine.

N_part  = 500;
xt      = sqrt(10)*randn(N_part,1);
xtplus1 = zeros(N_part,1);
N_lim   = N_part / 50.0;
wt      = ones(N_part,1)./N_part;
wtplus1 = zeros(N_part,1);

position= zeros(N, 1);

for t = 1:N
    for i=1:N_part
        xtplus1(i) = f(xt(i), temps(t))+ sqrt(10) * randn(1);
        wtplus1(i)  = abs(wt(i)*( g( xtplus1(i) ) + randn(1) ));
        
        % Correction des poids...
%        wtplus1(i)  = sqrt( wtplus1(i) );
        wtplus1(i)  = ( wtplus1(i) )^(0.9);
    end
    
    W = sum(wtplus1);
    wtplus1 = wtplus1./W;
    Ntplus1 = 1/norm(wtplus1);

    if (Ntplus1 < N_lim)
%        fprintf('Resampling at iter %d, N = %f \n', t, Ntplus1);
        xtplus1 = resample(xtplus1, wtplus1, N_part);
    end

    xt=xtplus1;
    wt=wtplus1;

    position(t) = mean( xt );
end
fprintf('Algorithme PF, bootstrap (modifié) terminé \n');

%%
figure (3);
clf;
plot(xt,wt, '.');

%%
figure(4);
plot(temps, x, 'r');
hold on;
plot(temps, position, 'b');


%%
% Par rapport à ce que l'on a eu avant, les poids sont beaucoup mieux
% distribués.
% Les données traitées on l'air beaucoup moins bruitées, voir même trés 
% (trop ?) bien débruitées. On remarque que l'on anticipe même parfois
% les fortes variations de position !
% 





