"""
Mecanisme de barra amb corredora: la barra AE (angle theta, coordenada
independent) mou la dolla E, que llisca per la barra BD (angle alpha).

    s(theta)     = sqrt(lAE^2 + lAB^2 - 2 lAB lAE sin(theta))
    alpha(theta) = atan2(lAB - lAE sin(theta), lAE cos(theta))
    alphadot     = -lAE (lAE - lAB sin(theta)) / s^2 * thetadot
    sdot         = -lAE lAB cos(theta) / s * thetadot
    |V_D|        = 2 lAE |alphadot|

El programa:
  1) escriu la taula de valors en format LaTeX (amb coma decimal),
  2) dibuixa les corbes en tot el recorregut, marcant els punts de la taula.

Genera: TME_ee_barra_corredora.pdf
"""
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- paràmetres
l_AE = 1.0           # m
l_AB = 0.8           # m
thetadot = 3.0       # rad/s, constant
th_min, th_max = 0, 60                     # graus, recorregut
th_taula = [0, 15, 30, 45, 60]             # graus, punts de la taula


# ---------------------------------------------------------------- càlcul
def cinematica(th_graus):
    th = np.radians(th_graus)
    s = np.sqrt(l_AE**2 + l_AB**2 - 2 * l_AB * l_AE * np.sin(th))
    alpha = np.arctan2(l_AB - l_AE * np.sin(th), l_AE * np.cos(th))
    alphadot = -l_AE * (l_AE - l_AB * np.sin(th)) / s**2 * thetadot
    sdot = -l_AE * l_AB * np.cos(th) / s * thetadot
    VD = 2 * l_AE * np.abs(alphadot)
    return s, np.degrees(alpha), alphadot, sdot, VD


# ---------------------------------------------------------------- taula LaTeX
def coma(v, n):
    return f"{v:.{n}f}".replace(".", "{,}")

print(r"\begin{tabular}{c|ccccc}")
print(r"$\theta$ & $\alpha$ & $s=BE$ [m] & $\dot\alpha$ [rad/s] & $\dot s$ [m/s] & $|\vec V_D|$ [m/s] \\ \hline")
for i, th in enumerate(th_taula):
    s, a, ad, sd, vd = cinematica(th)
    fi = r" \\" if i < len(th_taula) - 1 else ""
    print(rf"${th}^\circ$ & ${coma(a, 2)}^\circ$ & ${coma(s, 4)}$ & ${coma(ad, 3)}$ "
          rf"& ${coma(sd, 3)}$ & ${coma(vd, 3)}${fi}")
print(r"\end{tabular}")

# ---------------------------------------------------------------- estil
C_ANG = "#2a78d6"    # blau: magnituds angulars (alpha, alphadot)
C_LIN = "#eb6834"    # taronja: magnituds lineals de la dolla (s, sdot)
C_D = "#1baf7a"      # aqua: punt D
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e4e3df"

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 10,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# ---------------------------------------------------------------- gràfic
th = np.linspace(th_min, th_max, 400)
s, a, ad, sd, vd = cinematica(th)
s_t, a_t, ad_t, sd_t, vd_t = cinematica(np.array(th_taula))

fig = plt.figure(figsize=(7, 6))
gs = fig.add_gridspec(3, 2)
panells = [
    (gs[0, 0], a, a_t, r"$\alpha$ [$^\circ$]", C_ANG),
    (gs[0, 1], s, s_t, r"$s=BE$ [m]", C_LIN),
    (gs[1, 0], ad, ad_t, r"$\dot\alpha$ [rad/s]", C_ANG),
    (gs[1, 1], sd, sd_t, r"$\dot s$ [m/s]", C_LIN),
    (gs[2, :], vd, vd_t, r"$|\vec V_D|$ [m/s]", C_D),
]

for pos, v, v_t, et, c in panells:
    ax = fig.add_subplot(pos)
    ax.axhline(0, color=INK2, lw=0.6, zorder=1)
    ax.plot(th, v, color=c, lw=2, zorder=3)
    ax.plot(th_taula, v_t, "o", ms=6, color=c, mec="white", mew=1.2, zorder=4,
            clip_on=False)   # que els punts de 0° i 60° no quedin tallats
    ax.set_ylabel(et)
    ax.set_xlim(th_min, th_max)
    ax.set_xticks(th_taula)
    ax.grid(True, color=GRID, lw=0.6, zorder=0)
    ax.set_xlabel(r"$\theta$ [$^\circ$]")
    # el zero sempre visible
    lo, hi = min(v.min(), 0), max(v.max(), 0)
    marge = 0.08 * (hi - lo)
    ax.set_ylim(lo - marge, hi + marge)

text_caption = (rf"Barra amb corredora, $\ell_{{AE}}={l_AE}$ m, $\ell_{{AB}}={l_AB}$ m, "
                rf"$\dot\theta={thetadot}$ rad/s constant.")
fig.tight_layout()
fig.savefig("TME_ee_barra_corredora.pdf")
print(text_caption)


# ---------------------------------------------------------------- posicions del mecanisme
def geometria(th_graus):
    """Coordenades dels punts amb l'origen a B."""
    th = np.radians(th_graus)
    s, a, *_ = cinematica(th_graus)
    a = np.radians(a)
    B = np.array([0.0, 0.0])
    A = np.array([0.0, l_AB])
    E = A + l_AE * np.array([np.cos(th), -np.sin(th)])
    D = 2 * l_AE * np.array([np.cos(a), np.sin(a)])
    return A, B, E, D


def suport(ax, P, mida=0.09):
    """Articulació fixa: cercle buit amb triangle i ratllat a sota."""
    x, y = P
    ax.fill([x, x - mida, x + mida], [y, y - 1.6 * mida, y - 1.6 * mida],
            color="white", ec=INK2, lw=1, zorder=2)
    ax.plot([x - 1.6 * mida, x + 1.6 * mida], [y - 1.6 * mida] * 2, color=INK2, lw=1)
    for k in np.linspace(-1.4, 1.2, 6):
        ax.plot([x + k * mida, x + (k + 0.4) * mida],
                [y - 2.2 * mida, y - 1.6 * mida], color=INK2, lw=0.6)


th_arc = np.linspace(th_min, th_max, 100)
geo_arc = [geometria(t) for t in th_arc]
E_arc = np.array([g[2] for g in geo_arc])
D_arc = np.array([g[3] for g in geo_arc])

fig2, axs2 = plt.subplots(1, len(th_taula), figsize=(10, 2.4), sharey=True)
for ax, th_i in zip(axs2, th_taula):
    A, B, E, D = geometria(th_i)

    # trajectòries de E i D en tot el recorregut
    ax.plot(*E_arc.T, ls="--", lw=0.8, color=C_LIN, alpha=0.6, zorder=1)
    ax.plot(*D_arc.T, ls="--", lw=0.8, color=C_D, alpha=0.6, zorder=1)

    suport(ax, A)
    suport(ax, B)
    ax.plot(*np.c_[B, D], color=INK2, lw=4, solid_capstyle="round", zorder=3)     # barra BD
    ax.plot(*np.c_[A, E], color=C_ANG, lw=3, solid_capstyle="round", zorder=4)    # barra AE
    ax.plot(*E, "s", ms=9, color=C_LIN, mec="white", mew=1, zorder=5)            # dolla E
    ax.plot(*D, "o", ms=7, color=C_D, mec="white", mew=1, zorder=5)              # punt D
    for P in (A, B):
        ax.plot(*P, "o", ms=6, color="white", mec=INK2, mew=1.2, zorder=6)

    if th_i == th_taula[0]:          # etiquetes només al primer panell
        ax.annotate("A", A, xytext=(-12, 4), textcoords="offset points", fontsize=16, color=INK)
        ax.annotate("B", B, xytext=(-12, 4), textcoords="offset points", fontsize=16, color=INK)
        ax.annotate("E", E, xytext=(4, -15), textcoords="offset points", fontsize=16, color=INK)
        ax.annotate("D", D, xytext=(5, -4), textcoords="offset points", fontsize=16, color=INK)

    ax.set_title(rf"$\theta={th_i}^\circ$, $\alpha={np.degrees(np.arctan2(*(D[::-1]))):.1f}^\circ$",
                 fontsize=16, color=INK)
    ax.set_aspect("equal")
    ax.set_xlim(-0.35, 2.15)
    ax.set_ylim(-0.6, 1.45)
    ax.axis("off")

fig2.tight_layout()
fig2.savefig("TME_ee_barra_corredora_posicions.pdf")
plt.show()