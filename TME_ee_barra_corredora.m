% TME_ee_barra_corredora.m
%
% Mecanisme de barra amb corredora: la barra AE (angle theta, coordenada
% independent) mou la dolla E, que llisca per la barra BD (angle alpha).
%
%     s(theta)     = sqrt(lAE^2 + lAB^2 - 2 lAB lAE sin(theta))
%     alpha(theta) = atan2(lAB - lAE sin(theta), lAE cos(theta))
%     alphadot     = -lAE (lAE - lAB sin(theta)) / s^2 * thetadot
%     sdot         = -lAE lAB cos(theta) / s * thetadot
%     |V_D|        = 2 lAE |alphadot|
%
% El programa:
%   1) escriu la taula de valors en format LaTeX (amb coma decimal),
%   2) dibuixa les corbes en tot el recorregut, marcant els punts de la taula,
%   3) dibuixa el mecanisme en les posicions de la taula.
%
% Genera: TME_ee_barra_corredora.pdf i TME_ee_barra_corredora_posicions.pdf
%
% Requereix MATLAB R2016b o posterior (funcions locals al final de l'script).

clear; close all;

%% ------------------------------------------------------------ paràmetres
P.l_AE     = 1.0;        % m
P.l_AB     = 0.8;        % m
P.thetadot = 3.0;        % rad/s, constant
th_min = 0;  th_max = 60;                % graus, recorregut
th_taula = [0 15 30 45 60];              % graus, punts de la taula

%% ------------------------------------------------------------ taula LaTeX
disp('\begin{tabular}{c|ccccc}');
disp(['$\theta$ & $\alpha$ & $s=BE$ [m] & $\dot\alpha$ [rad/s] & ' ...
      '$\dot s$ [m/s] & $|\vec V_D|$ [m/s] \\ \hline']);
for i = 1:numel(th_taula)
    [s, a, ad, sd, vd] = cinematica(th_taula(i), P);
    if i < numel(th_taula), fi = ' \\'; else, fi = ''; end
    disp(['$' num2str(th_taula(i)) '^\circ$ & $' coma(a, 2) '^\circ$ & $' coma(s, 4) ...
          '$ & $' coma(ad, 3) '$ & $' coma(sd, 3) '$ & $' coma(vd, 3) '$' fi]);
end
disp('\end{tabular}');

%% ------------------------------------------------------------ estil
hex = @(h) sscanf(h(2:end), '%2x%2x%2x', [1 3])/255;
S.ANG  = hex('#2a78d6');   % blau: magnituds angulars (alpha, alphadot)
S.LIN  = hex('#eb6834');   % taronja: magnituds lineals de la dolla (s, sdot)
S.D    = hex('#1baf7a');   % aqua: punt D
S.INK  = hex('#0b0b0b');
S.INK2 = hex('#52514e');
S.GRID = hex('#e4e3df');

%% ------------------------------------------------------------ gràfic
th = linspace(th_min, th_max, 400);
[s, a, ad, sd, vd] = cinematica(th, P);
[s_t, a_t, ad_t, sd_t, vd_t] = cinematica(th_taula, P);

fig = figure('Color', 'w', 'Units', 'inches', 'Position', [1 1 7 6]);
panells = { 1,      a,  a_t,  '$\alpha$ [$^\circ$]',   S.ANG;
            2,      s,  s_t,  '$s=BE$ [m]',            S.LIN;
            3,      ad, ad_t, '$\dot\alpha$ [rad/s]',  S.ANG;
            4,      sd, sd_t, '$\dot s$ [m/s]',        S.LIN;
            [5 6],  vd, vd_t, '$|\vec V_D|$ [m/s]',    S.D };

for k = 1:size(panells, 1)
    [pos, v, v_t, et, c] = panells{k, :};
    ax = subplot(3, 2, pos);  hold(ax, 'on');
    plot(ax, [th_min th_max], [0 0], 'Color', S.INK2, 'LineWidth', 0.6);
    plot(ax, th, v, 'Color', c, 'LineWidth', 2);
    plot(ax, th_taula, v_t, 'o', 'MarkerSize', 6, 'MarkerFaceColor', c, ...
         'MarkerEdgeColor', 'w', 'LineWidth', 1.2, 'Clipping', 'off');
    ylabel(ax, et, 'Interpreter', 'latex', 'Color', S.INK);
    xlabel(ax, '$\theta$ [$^\circ$]', 'Interpreter', 'latex', 'Color', S.INK);
    % el zero sempre visible
    lo = min(min(v), 0);  hi = max(max(v), 0);
    marge = 0.08*(hi - lo);
    set(ax, 'XLim', [th_min th_max], 'XTick', th_taula, 'YLim', [lo - marge, hi + marge], ...
            'XGrid', 'on', 'YGrid', 'on', 'GridColor', S.GRID, 'GridAlpha', 1, ...
            'Box', 'off', 'TickDir', 'out', 'XColor', S.INK2, 'YColor', S.INK2, ...
            'FontSize', 10, 'TickLabelInterpreter', 'latex');
end
desa(fig, 'TME_ee_barra_corredora.pdf');

fprintf('Barra amb corredora, l_AE = %g m, l_AB = %g m, thetadot = %g rad/s constant.\n', ...
        P.l_AE, P.l_AB, P.thetadot);

%% ------------------------------------------------------------ posicions del mecanisme
th_arc = linspace(th_min, th_max, 100);
E_arc = zeros(numel(th_arc), 2);  D_arc = E_arc;
for k = 1:numel(th_arc)
    [~, ~, E, D] = geometria(th_arc(k), P);
    E_arc(k, :) = E;  D_arc(k, :) = D;
end

fig2 = figure('Color', 'w', 'Units', 'inches', 'Position', [1 1 10 2.4]);
n = numel(th_taula);
for k = 1:n
    th_i = th_taula(k);
    ax = subplot(1, n, k);  hold(ax, 'on');
    [A, B, E, D] = geometria(th_i, P);

    % trajectòries de E i D en tot el recorregut
    plot(ax, E_arc(:,1), E_arc(:,2), '--', 'Color', S.LIN, 'LineWidth', 0.8);
    plot(ax, D_arc(:,1), D_arc(:,2), '--', 'Color', S.D,   'LineWidth', 0.8);

    suport(ax, A, 0.09, S);
    suport(ax, B, 0.09, S);
    plot(ax, [B(1) D(1)], [B(2) D(2)], 'Color', S.INK2, 'LineWidth', 4);       % barra BD
    plot(ax, [A(1) E(1)], [A(2) E(2)], 'Color', S.ANG,  'LineWidth', 3);       % barra AE
    plot(ax, E(1), E(2), 's', 'MarkerSize', 9, 'MarkerFaceColor', S.LIN, ...
         'MarkerEdgeColor', 'w');                                              % dolla E
    plot(ax, D(1), D(2), 'o', 'MarkerSize', 7, 'MarkerFaceColor', S.D, ...
         'MarkerEdgeColor', 'w');                                              % punt D
    for Pt = {A, B}
        plot(ax, Pt{1}(1), Pt{1}(2), 'o', 'MarkerSize', 6, 'MarkerFaceColor', 'w', ...
             'MarkerEdgeColor', S.INK2, 'LineWidth', 1.2);
    end

    if k == 1                                   % etiquetes només al primer panell
        noms = {'A', 'B', 'E', 'D'};
        pts  = {A, B, E, D};
        offs = [-0.21 0.07; -0.21 0.07; 0.07 -0.26; 0.09 -0.07];
        for j = 1:numel(noms)
            text(ax, pts{j}(1) + offs(j,1), pts{j}(2) + offs(j,2), noms{j}, ...
                 'FontSize', 16, 'Color', S.INK, 'Interpreter', 'latex');
        end
    end

    title(ax, sprintf('$\\theta=%d^\\circ$, $\\alpha=%.1f^\\circ$', th_i, atan2d(D(2), D(1))), ...
          'Interpreter', 'latex', 'FontSize', 16, 'Color', S.INK);
    daspect(ax, [1 1 1]);
    xlim(ax, [-0.35 2.15]);  ylim(ax, [-0.6 1.45]);
    axis(ax, 'off');
end
desa(fig2, 'TME_ee_barra_corredora_posicions.pdf');


%% ============================================================ funcions locals

function [s, alpha, alphadot, sdot, VD] = cinematica(th_graus, P)
    % Accepta un vector d'angles; alpha es retorna en graus
    th = deg2rad(th_graus);
    s = sqrt(P.l_AE^2 + P.l_AB^2 - 2*P.l_AB*P.l_AE*sin(th));
    alpha = atan2d(P.l_AB - P.l_AE*sin(th), P.l_AE*cos(th));
    alphadot = -P.l_AE*(P.l_AE - P.l_AB*sin(th)) ./ s.^2 * P.thetadot;
    sdot = -P.l_AE*P.l_AB*cos(th) ./ s * P.thetadot;
    VD = 2*P.l_AE*abs(alphadot);
end

function txt = coma(v, n)
    txt = strrep(sprintf('%.*f', n, v), '.', '{,}');
end

function [A, B, E, D] = geometria(th_graus, P)
    % Coordenades dels punts amb l'origen a B
    [~, a] = cinematica(th_graus, P);
    B = [0 0];
    A = [0 P.l_AB];
    E = A + P.l_AE*[cosd(th_graus), -sind(th_graus)];
    D = 2*P.l_AE*[cosd(a), sind(a)];
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
