% TME_ee_taula_elevadora.m
%
% Taula elevadora: variació de theta, y i les seves derivades en funció de la
% posició x del punt A.
%
%     x = 2L cos(theta),   y = 2L sin(theta),   0 < x < 2L
%
% Amb una velocitat de l'actuador xdot constant (xddot = 0), es veu com la
% mateixa entrada produeix velocitats i acceleracions molt diferents segons la
% posició, i com tot divergeix quan x -> 2L (theta -> 0, configuració singular).

clear; close all;

%% ------------------------------------------------------------ paràmetres
L       = 0.5;    % m, longitud de mitja barra
xdot    = 0.10;   % m/s, velocitat del punt A (positiva: x augmenta, la taula baixa)
xddot   = 0.0;    % m/s^2, acceleració del punt A
th_lim  = 25;     % graus, angle a partir del qual s'ombreja la zona propera a la singularitat
x_lim   = 2*L*cosd(th_lim);
lim_vel = 4.0;    % factor per retallar l'eix vertical prop de la singularitat
fitxer  = 'TME_ee_taula_elevadora.pdf';

%% ------------------------------------------------------------ càlcul
x = linspace(0.01*2*L, 0.995*2*L, 800);
w = sqrt(4*L^2 - x.^2);              % = 2L sin(theta) = y

theta     = acos(x/(2*L));
y         = w;
thetadot  = -xdot./w;
ydot      = -x.*xdot./w;
thetaddot = -xddot./w - x.*xdot^2./w.^3;
yddot     = -x.*xddot./w - 4*L^2*xdot^2./w.^3;

%% ------------------------------------------------------------ estil
hex = @(h) sscanf(h(2:end), '%2x%2x%2x', [1 3])/255;
C_THETA = hex('#2a78d6');   % blau    (columna theta)
C_Y     = hex('#eb6834');   % taronja (columna y)
INK     = hex('#0b0b0b');
INK2    = hex('#52514e');
GRID    = hex('#e4e3df');

dades = { rad2deg(theta), '$\theta$ [$^\circ$]',          y,     '$y$ [m]';
          thetadot,       '$\dot\theta$ [rad/s]',         ydot,  '$\dot y$ [m/s]';
          thetaddot,      '$\ddot\theta$ [rad/s$^2$]',    yddot, '$\ddot y$ [m/s$^2$]' };
colors = {C_THETA, C_Y};

fig = figure('Color', 'w', 'Units', 'centimeters', 'Position', [2 2 20.3 16.5]);
axs = cell(3, 2);

for fila = 1:3
    for col = 1:2
        v  = dades{fila, 2*col-1};
        et = dades{fila, 2*col};
        ax = subplot(3, 2, 2*(fila-1) + col);
        axs{fila, col} = ax;
        hold(ax, 'on');

        % Límits verticals (es calculen abans per poder dibuixar el fons)
        lo = min(min(v), 0);  hi = max(max(v), 0);       % el zero sempre visible
        if fila > 1
            % Retalla l'eix vertical prop de la singularitat perquè es vegi la resta
            ref = max(abs(v(x < x_lim)));
            yl  = [max(lo, -lim_vel*ref)*1.05 - 0.02*ref, ...
                   min(hi,  lim_vel*ref)*1.05 + 0.02*ref];
        else
            yl  = [lo - 0.05*(hi - lo), hi + 0.05*(hi - lo)];
        end

        % Zona ombrejada i línia del zero (al fons), i després la corba
        patch(ax, [x_lim 2*L 2*L x_lim], [yl(1) yl(1) yl(2) yl(2)], GRID, ...
              'EdgeColor', 'none');
        plot(ax, [0 2*L], [0 0], 'Color', INK2, 'LineWidth', 0.6);
        plot(ax, x, v, 'Color', colors{col}, 'LineWidth', 2);
        xlim(ax, [0 2*L]);
        ylim(ax, yl);

        set(ax, 'Box', 'off', 'TickDir', 'out', 'Layer', 'top', ...
                'XGrid', 'on', 'YGrid', 'on', 'GridColor', GRID, 'GridAlpha', 1, ...
                'XColor', INK2, 'YColor', INK2, 'FontSize', 10, ...
                'TickLabelInterpreter', 'latex');
        ylabel(ax, et, 'Interpreter', 'latex', 'Color', INK);
        if fila < 3
            set(ax, 'XTickLabel', []);
        else
            xlabel(ax, '$x$ [m]', 'Interpreter', 'latex', 'Color', INK);
        end
    end
end

%% ------------------------------------------------------------ anotació
ax = axs{1, 2};
yl = ylim(ax);
punt = [x_lim + 0.25*(2*L - x_lim), 0.2*yl(2)];      % dins la zona, sota la corba
xt   = x_lim - 0.06;                                  % on acaba el text
plot(ax, [xt + 0.01, punt(1)], [punt(2) punt(2)], 'Color', INK2, 'LineWidth', 0.8);
plot(ax, punt(1), punt(2), 'o', 'MarkerSize', 4, ...
     'MarkerFaceColor', INK2, 'MarkerEdgeColor', INK2);
text(ax, xt, punt(2), ...
     {'zona propera', 'a la singularitat', ...
      sprintf('($x > %.1f$ m, $\\theta < %.0f^\\circ$)', x_lim, th_lim)}, ...
     'Interpreter', 'latex', 'FontSize', 9, 'Color', INK2, ...
     'HorizontalAlignment', 'right', 'VerticalAlignment', 'middle');

%% ------------------------------------------------------------ desar
text_caption = sprintf('Taula elevadora, L = %g m, xdot = %g m/s constant.', L, xdot);
disp(text_caption);

if exist('exportgraphics', 'file')                    % MATLAB R2020a o posterior
    exportgraphics(fig, fitxer, 'ContentType', 'vector');
else
    set(fig, 'PaperUnits', 'centimeters', 'PaperSize', [20.3 16.5], ...
             'PaperPosition', [0 0 20.3 16.5]);
    print(fig, fitxer, '-dpdf');
end
