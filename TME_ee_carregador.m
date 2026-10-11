% TME_ee_carregador.m
%
% Carregador amb cilindre hidràulic: el cilindre AD (longitud s) fa girar la
% manovella BD (angle phi) i el cos DE es mou en translació circular.
%
%     s(phi)   = 2 L cos(phi/2)
%     phidot   = -sdot / (L sin(phi/2))
%     V_G      = V_D = L phidot (-sin(phi) i + cos(phi) j)
%
% El cilindre es retrau a velocitat constant (sdot < 0), de manera que phi
% augmenta i el temps és proporcional a la variació de s.
%
% El programa:
%   1) escriu la taula de valors en format LaTeX (amb coma decimal),
%   2) dibuixa l'evolució de posicions i velocitats en funció de phi, amb
%      l'escala de temps a l'eix superior,
%   3) dibuixa el mecanisme en diverses posicions.
%
% Genera: TME_ee_carregador.pdf (cilindre i manovella),
%         TME_ee_carregador_G.pdf (centre de gravetat) i
%         TME_ee_carregador_posicions.pdf (dibuix del mecanisme)
%
% Requereix MATLAB R2016b o posterior (funcions locals al final de l'script).

clear; close all;

%% ------------------------------------------------------------ paràmetres
P.L    = 2.0;        % m
P.a    = 0.4;        % m, alçada del CDG sobre DE
P.b    = 0.2;        % m, distància horitzontal del CDG a l'esquerra d'E
P.sdot = -0.25;      % m/s, constant (negativa: el cilindre es retrau)
P.phi_min = 60;  P.phi_max = 120;   % graus, recorregut
phi_taula  = [60 90 120];           % graus, punts de la taula
phi_dibuix = [60 90 120];           % graus, posicions del dibuix del mecanisme

%% ------------------------------------------------------------ taula LaTeX
disp('\begin{tabular}{c|ccccc}');
disp(['$\varphi$ & $s$ [m] & $\dot\varphi$ [rad/s] & $\vec r_G$ [m] & ' ...
      '$\vec V_G$ [m/s] & $|\vec V_G|$ [m/s] \\ \hline']);
for i = 1:numel(phi_taula)
    [s, pd, rG, VG] = cinematica(phi_taula(i), P);
    if i < numel(phi_taula), fi = ' \\'; else, fi = ''; end
    disp(['$' num2str(phi_taula(i)) '^\circ$ & $' coma(s) '$ & $' coma(pd) ...
          '$ & $' vec_ij(rG) '$ & $' vec_ij(VG) '$ & $' coma(norm(VG)) '$' fi]);
end
disp('\end{tabular}');
fprintf('Temps de %d° a %d°: %.2f s\n', P.phi_min, P.phi_max, temps(P.phi_max, P));

%% ------------------------------------------------------------ estil
hex = @(h) sscanf(h(2:end), '%2x%2x%2x', [1 3])/255;
S.CIL  = hex('#6250d6');   % violeta: cilindre (s)
S.ANG  = hex('#2a78d6');   % blau: manovella (phidot)
S.X    = hex('#eb6834');   % taronja: components x del CDG
S.Y    = hex('#1baf7a');   % aqua: components y del CDG
S.INK  = hex('#0b0b0b');
S.INK2 = hex('#52514e');
S.GRID = hex('#e4e3df');
S.COS  = hex('#f1efe9');   % farciment del cos DE

%% ------------------------------------------------------------ evolució
phi = linspace(P.phi_min, P.phi_max, 400);
[s_c, pd, rG, VG] = cinematica(phi, P);
[s_t, pd_t, rG_t, VG_t] = cinematica(phi_taula, P);

% ---- figura 1: cilindre i manovella
fig1 = figure('Color', 'w', 'Units', 'inches', 'Position', [1 1 7 5]);

ax = subplot(2, 2, 1);                                 % longitud del cilindre
corba(ax, phi, s_c, phi_taula, s_t, S.CIL, '', S);
ylabel(ax, '$s$ [m]', 'Interpreter', 'latex');
ylim(ax, [0, 1.1*max(s_c)]);
ax1 = ax;

ax = subplot(2, 2, 3);                                 % velocitat del cilindre (constant)
plot(ax, [P.phi_min P.phi_max], [0 0], 'Color', S.INK2, 'LineWidth', 0.6); hold(ax, 'on');
corba(ax, phi, P.sdot*ones(size(phi)), phi_taula, P.sdot*ones(size(phi_taula)), S.CIL, '', S);
ylabel(ax, '$\dot s$ [m/s]', 'Interpreter', 'latex');
ylim(ax, [1.3*min(P.sdot, 0), 1.3*max(P.sdot, 0) + 0.05*abs(P.sdot)]);
ax3 = ax;

ax = subplot(2, 2, 2);                                 % angle de la manovella
corba(ax, phi, phi, phi_taula, phi_taula, S.ANG, '', S);
ylabel(ax, '$\varphi$ [$^\circ$]', 'Interpreter', 'latex');
ylim(ax, [0, 1.1*P.phi_max]);
ax2 = ax;

ax = subplot(2, 2, 4);                                 % velocitat angular
corba(ax, phi, pd, phi_taula, pd_t, S.ANG, '', S);
ylabel(ax, '$\dot\varphi$ [rad/s]', 'Interpreter', 'latex');
ylim(ax, [0, 1.1*max(pd)]);
ax4 = ax;

format_eixos([ax1 ax2 ax3 ax4], P, phi_taula, S);
for ax = [ax3 ax4]
    xlabel(ax, '$\varphi$ [$^\circ$]', 'Interpreter', 'latex');
end
for ax = [ax1 ax2]
    set(ax, 'XTickLabel', []);
end
drawnow;
for ax = [ax1 ax2]
    eix_temps(ax, P, S);
end
desa(fig1, 'TME_ee_carregador.pdf');

% ---- figura 2: centre de gravetat del cos
fig3 = figure('Color', 'w', 'Units', 'inches', 'Position', [1 1 7 2.8]);

ax = subplot(1, 2, 1);                                 % posició del CDG
hx = corba(ax, phi, rG(1,:), phi_taula, rG_t(1,:), S.X, '$x_G$', S);
hy = corba(ax, phi, rG(2,:), phi_taula, rG_t(2,:), S.Y, '$y_G$', S);
ylabel(ax, '$\vec r_G$ [m]', 'Interpreter', 'latex');
ylim(ax, [0, 1.1*max([rG(1,:) rG(2,:)])]);
legend(ax, [hx hy], {'$x_G$', '$y_G$'}, 'Interpreter', 'latex', ...
       'Location', 'southwest', 'Box', 'off', 'FontSize', 9);
axG1 = ax;

ax = subplot(1, 2, 2);                                 % velocitat del CDG
plot(ax, [P.phi_min P.phi_max], [0 0], 'Color', S.INK2, 'LineWidth', 0.6); hold(ax, 'on');
hx = corba(ax, phi, VG(1,:), phi_taula, VG_t(1,:), S.X, '$V_{G,x}$', S);
hy = corba(ax, phi, VG(2,:), phi_taula, VG_t(2,:), S.Y, '$V_{G,y}$', S);
ylabel(ax, '$\vec V_G$ [m/s]', 'Interpreter', 'latex');
legend(ax, [hx hy], {'$V_{G,x}$', '$V_{G,y}$'}, 'Interpreter', 'latex', ...
       'Location', 'northeast', 'Box', 'off', 'FontSize', 9);
axG2 = ax;

format_eixos([axG1 axG2], P, phi_taula, S);
for ax = [axG1 axG2]
    xlabel(ax, '$\varphi$ [$^\circ$]', 'Interpreter', 'latex');
end
drawnow;
for ax = [axG1 axG2]
    eix_temps(ax, P, S);
end
desa(fig3, 'TME_ee_carregador_G.pdf');

fprintf('Carregador, L = %g m, sdot = %g m/s constant (el cilindre es retrau).\n', ...
        P.L, P.sdot);

%% ------------------------------------------------------------ posicions del mecanisme
% Forma del cos en coordenades relatives a D (en unitats de L); DE és el costat inferior
FORMA = [-0.12 0.00; 1.12 0.00; 1.12 0.78; 0.80 0.78; 0.55 0.40; 0.30 0.27; -0.12 0.20];
L_CAMISA = 1.2;   % m, longitud de la camisa del cilindre (ha de ser < s mínima)

phi_arc = linspace(P.phi_min, P.phi_max, 100);
G_arc = zeros(numel(phi_arc), 2);
for k = 1:numel(phi_arc)
    [~, ~, ~, ~, ~, G] = geometria(phi_arc(k), P);
    G_arc(k, :) = G;
end

fig2 = figure('Color', 'w', 'Units', 'inches', 'Position', [1 1 11 3.4]);
n = numel(phi_dibuix);
for k = 1:n
    ph = phi_dibuix(k);
    ax = subplot(1, n, k);  hold(ax, 'on');
    [A, B, C, D, E, G] = geometria(ph, P);

    % cos DE (translació: la forma només es desplaça)
    cos_xy = D + P.L*FORMA;
    fill(ax, cos_xy(:,1), cos_xy(:,2), S.COS, 'EdgeColor', S.INK2, 'LineWidth', 1);

    % trajectòria de G
    plot(ax, G_arc(:,1), G_arc(:,2), '--', 'Color', S.X, 'LineWidth', 0.8);

    % cilindre: tija prima de A a D i camisa gruixuda des de A
    u = (D - A)/norm(D - A);
    plot(ax, [A(1) D(1)], [A(2) D(2)], 'Color', S.INK2, 'LineWidth', 2);
    Q = A + L_CAMISA*u;
    plot(ax, [A(1) Q(1)], [A(2) Q(2)], 'Color', S.CIL, 'LineWidth', 7);

    % manovelles
    plot(ax, [B(1) D(1)], [B(2) D(2)], 'Color', S.INK, 'LineWidth', 3.5);
    plot(ax, [C(1) E(1)], [C(2) E(2)], 'Color', S.INK, 'LineWidth', 3.5);

    for Pt = {A, B, C}
        suport(ax, Pt{1}, 0.13, S);
    end
    for Pt = {A, B, C, D, E}
        plot(ax, Pt{1}(1), Pt{1}(2), 'o', 'MarkerSize', 6, ...
             'MarkerFaceColor', 'w', 'MarkerEdgeColor', S.INK2, 'LineWidth', 1.2);
    end
    plot(ax, G(1), G(2), 'o', 'MarkerSize', 7, ...
         'MarkerFaceColor', S.X, 'MarkerEdgeColor', 'w');            % CDG

    if k == 1                                  % etiquetes només al primer panell
        noms = {'A', 'B', 'C', 'D', 'E', 'G'};
        pts  = {A, B, C, D, E, G};
        offs = [-0.35 0.05; -0.35 0.05; -0.35 0.05; -0.30 0.05; 0.12 -0.18; 0.12 0.05];
        for j = 1:numel(noms)
            text(ax, pts{j}(1) + offs(j,1), pts{j}(2) + offs(j,2), noms{j}, ...
                 'FontSize', 16, 'Color', S.INK, 'Interpreter', 'latex');
        end
    end

    s_i = cinematica(ph, P);
    title(ax, sprintf('$\\varphi=%d^\\circ$, $s=%.2f$ m, $t=%.2f$ s', ph, s_i, temps(ph, P)), ...
          'Interpreter', 'latex', 'FontSize', 16, 'Color', S.INK);
    daspect(ax, [1 1 1]);
    xlim(ax, [-2.6 3.6]);  ylim(ax, [-0.5 3.8]);
    axis(ax, 'off');
end
desa(fig2, 'TME_ee_carregador_posicions.pdf');


%% ============================================================ funcions locals

function [s, phidot, rG, VG] = cinematica(phi_graus, P)
    % Accepta un vector d'angles; rG i VG tenen una columna per angle.
    ph = deg2rad(phi_graus(:)');
    s = 2*P.L*cos(ph/2);
    phidot = -P.sdot ./ (P.L*sin(ph/2));
    rG = [P.L + P.L*cos(ph) - P.b;  P.L*sin(ph) + P.a];
    VG = P.L*phidot .* [-sin(ph); cos(ph)];
end

function t = temps(phi_graus, P)
    % Temps des de phi_min (s varia linealment amb el temps)
    s0 = 2*P.L*cosd(P.phi_min/2);
    t = (s0 - 2*P.L*cosd(phi_graus/2)) / abs(P.sdot);
end

function ph = angle_t(t, P)
    % Inversa de temps(): angle phi [graus] per a un temps t
    s0 = 2*P.L*cosd(P.phi_min/2);
    x = min(max((s0 - abs(P.sdot)*t)/(2*P.L), -1), 1);
    ph = 2*acosd(x);
end

function txt = coma(v, n)
    if nargin < 2, n = 3; end
    txt = strrep(sprintf('%.*f', n, v), '.', '{,}');
end

function txt = vec_ij(v)
    % Vector en notació i, j, sense termes nuls
    u = {'\vec\imath', '\vec\jmath'};
    txt = '';
    for k = 1:2
        if abs(v(k)) < 5e-4, continue; end
        if v(k) < 0
            signe = '- ';
        elseif isempty(txt)
            signe = '';
        else
            signe = '+ ';
        end
        txt = [txt, ' ', signe, coma(abs(v(k))), '\,', u{k}]; %#ok<AGROW>
    end
    if isempty(txt), txt = '0'; end
end

function h = corba(ax, x, y, xt, yt, c, et, S)
    hold(ax, 'on');
    h = plot(ax, x, y, 'Color', c, 'LineWidth', 2);
    plot(ax, xt, yt, 'o', 'MarkerSize', 6, 'MarkerFaceColor', c, ...
         'MarkerEdgeColor', 'w', 'LineWidth', 1.2, 'Clipping', 'off');
    if ~isempty(et)                          % etiqueta directa al final de la corba
        text(ax, x(end) + 0.02*(x(end) - x(1)), y(end), et, 'Interpreter', 'latex', ...
             'FontSize', 10, 'Color', S.INK, 'VerticalAlignment', 'middle');
    end
end

function format_eixos(axs, P, phi_taula, S)
    for ax = axs
        set(ax, 'XLim', [P.phi_min P.phi_max], 'XTick', phi_taula, ...
                'XGrid', 'on', 'YGrid', 'on', 'GridColor', S.GRID, 'GridAlpha', 1, ...
                'Box', 'off', 'TickDir', 'out', ...
                'XColor', S.INK2, 'YColor', S.INK2, 'FontSize', 10, ...
                'TickLabelInterpreter', 'latex');
        set(get(ax, 'YLabel'), 'Color', S.INK);
        set(get(ax, 'XLabel'), 'Color', S.INK);
    end
end

function eix_temps(ax, P, S)
    % Escala de temps a l'eix superior: eix transparent superposat
    t_max = temps(P.phi_max, P);
    tt = 0:floor(t_max);
    etiquetes = arrayfun(@num2str, tt, 'UniformOutput', false);
    ax2 = axes('Position', get(ax, 'Position'), 'Color', 'none', 'XAxisLocation', 'top', ...
               'XLim', get(ax, 'XLim'), 'XTick', angle_t(tt, P), 'XTickLabel', etiquetes, ...
               'YTick', [], 'YColor', 'none', 'XColor', S.INK2, 'Box', 'off', ...
               'TickDir', 'out', 'FontSize', 10, 'TickLabelInterpreter', 'latex', ...
               'HitTest', 'off');
    xlabel(ax2, '$t$ [s]', 'Interpreter', 'latex', 'Color', S.INK2);
    % si es redimensiona la figura, l'eix del temps segueix l'eix principal
    try
        addlistener(ax, 'SizeChanged', @(~, ~) set(ax2, 'Position', get(ax, 'Position')));
    catch
    end
end

function [A, B, C, D, E, G] = geometria(phi_graus, P)
    % Coordenades dels punts amb l'origen a B
    A = [-P.L 0];  B = [0 0];  C = [P.L 0];
    D = P.L*[cosd(phi_graus) sind(phi_graus)];
    E = C + D;
    G = E + [-P.b P.a];
end

function suport(ax, Pt, mida, S)
    % Articulació fixa: triangle i ratllat a sota
    x = Pt(1);  y = Pt(2);
    fill(ax, [x, x - mida, x + mida], [y, y - 1.6*mida, y - 1.6*mida], 'w', ...
         'EdgeColor', S.INK2, 'LineWidth', 1);
    plot(ax, [x - 1.6*mida, x + 1.6*mida], (y - 1.6*mida)*[1 1], 'Color', S.INK2, 'LineWidth', 1);
    for k = linspace(-1.4, 1.2, 6)
        plot(ax, [x + k*mida, x + (k + 0.4)*mida], [y - 2.2*mida, y - 1.6*mida], ...
             'Color', S.INK2, 'LineWidth', 0.6);
    end
end

function desa(fig, fitxer)
    if exist('exportgraphics', 'file')            % MATLAB R2020a o posterior
        exportgraphics(fig, fitxer, 'ContentType', 'vector');
    else
        pos = get(fig, 'Position');
        set(fig, 'PaperUnits', 'inches', 'PaperSize', pos(3:4), ...
                 'PaperPosition', [0 0 pos(3:4)]);
        print(fig, fitxer, '-dpdf');
    end
end
