"""
Carregador amb cilindre hidràulic: el cilindre AD (longitud s) fa girar la
manovella BD (angle phi) i el cos DE es mou en translació circular.

    s(phi)   = 2 L cos(phi/2)
    phidot   = -sdot / (L sin(phi/2))
    V_G      = V_D = L phidot (-sin(phi) i + cos(phi) j)

El cilindre es retrau a velocitat constant (sdot < 0), de manera que phi
augmenta i el temps és proporcional a la variació de s.

El programa:
  1) escriu la taula de valors en format LaTeX (amb coma decimal),
  2) dibuixa l'evolució de posicions i velocitats en funció de phi, amb
     l'escala de temps a l'eix superior,
  3) dibuixa el mecanisme en diverses posicions.

Genera: TME_ee_carregador.pdf (cilindre i manovella),
        TME_ee_carregador_G.pdf (centre de gravetat) i
        TME_ee_carregador_posicions.pdf (dibuix del mecanisme)
"""
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- paràmetres
L = 2.0          # m
a = 0.4          # m, alçada del CDG sobre DE
b = 0.2          # m, distància horitzontal del CDG a l'esquerra d'E
sdot = -0.25     # m/s, constant (negativa: el cilindre es retrau)
phi_min, phi_max = 60, 120          # graus, recorregut
phi_taula = [60, 90, 120]           # graus, punts de la taula
phi_dibuix = [60, 90, 120]          # graus, posicions del dibuix del mecanisme


# ---------------------------------------------------------------- càlcul
def cinematica(phi_graus):
    phi = np.radians(phi_graus)
    s = 2 * L * np.cos(phi / 2)
    phidot = -sdot / (L * np.sin(phi / 2))
    rG = np.array([L + L * np.cos(phi) - b, L * np.sin(phi) + a])
    VG = L * phidot * np.array([-np.sin(phi), np.cos(phi)])
    return s, phidot, rG, VG


def temps(phi_graus):
    """Temps des de phi_min (s varia linealment amb el temps)."""
    s0 = 2 * L * np.cos(np.radians(phi_min) / 2)
    return (s0 - 2 * L * np.cos(np.radians(phi_graus) / 2)) / abs(sdot)


def angle(t):
    """Inversa de temps(): angle phi [graus] per a un temps t."""
    s0 = 2 * L * np.cos(np.radians(phi_min) / 2)
    x = np.clip((s0 - abs(sdot) * np.asarray(t)) / (2 * L), -1, 1)
    return np.degrees(2 * np.arccos(x))


# ---------------------------------------------------------------- taula LaTeX
def coma(v, n=3):
    return f"{v:.{n}f}".replace(".", "{,}")

def vec(v):
    """Vector en notació i, j, sense termes nuls."""
    termes = []
    for comp, u in zip(v, (r"\vec\imath", r"\vec\jmath")):
        if abs(comp) < 5e-4:
            continue
        signe = "-" if comp < 0 else ("+" if termes else "")
        termes.append(rf"{signe} {coma(abs(comp))}\,{u}")
    return " ".join(termes) if termes else "0"

print(r"\begin{tabular}{c|ccccc}")
print(r"$\varphi$ & $s$ [m] & $\dot\varphi$ [rad/s] & $\vec r_G$ [m] & $\vec V_G$ [m/s] & $|\vec V_G|$ [m/s] \\ \hline")
for i, ph in enumerate(phi_taula):
    s, pd, rG, VG = cinematica(ph)
    fi = r" \\" if i < len(phi_taula) - 1 else ""
    print(rf"${ph}^\circ$ & ${coma(s)}$ & ${coma(pd)}$ & ${vec(rG)}$ & ${vec(VG)}$ "
          rf"& ${coma(np.linalg.norm(VG))}${fi}")
print(r"\end{tabular}")
print(f"Temps de {phi_min}° a {phi_max}°: {temps(phi_max):.2f} s")

# ---------------------------------------------------------------- estil
C_CIL = "#6250d6"    # violeta: cilindre (s)
C_ANG = "#2a78d6"    # blau: manovella (phidot)
C_X = "#eb6834"      # taronja: components x del CDG
C_Y = "#1baf7a"      # aqua: components y del CDG
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e4e3df"
COS = "#f1efe9"      # farciment del cos DE

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

# ---------------------------------------------------------------- evolució
phi = np.linspace(phi_min, phi_max, 400)
s_c, pd, rG, VG = cinematica(phi)
dades_t = [cinematica(p) for p in phi_taula]
s_t = np.array([d[0] for d in dades_t])
pd_t = np.array([d[1] for d in dades_t])
rG_t = np.array([d[2] for d in dades_t])
VG_t = np.array([d[3] for d in dades_t])


def corba(ax, y, y_t, c, et=None):
    ax.plot(phi, y, color=c, lw=2, zorder=3, label=et)
    ax.plot(phi_taula, y_t, "o", ms=6, color=c, mec="white", mew=1.2,
            zorder=4, clip_on=False)
    if et:
        ax.annotate(et, (phi[-1], y[-1]), xytext=(6, 0), textcoords="offset points",
                    color=INK, va="center", fontsize=10)


def eix_temps(ax):
    """Escala de temps a l'eix superior."""
    sec = ax.secondary_xaxis("top", functions=(temps, angle))
    sec.set_xlabel(r"$t$ [s]", color=INK2)
    sec.tick_params(colors=INK2)


def format_eixos(axs_list):
    for ax in axs_list:
        ax.set_xlim(phi_min, phi_max)
        ax.set_xticks(phi_taula)
        ax.grid(True, color=GRID, lw=0.6, zorder=0)


# ---- figura 1: cilindre i manovella
fig, axs = plt.subplots(2, 2, figsize=(7, 5), sharex=True)

ax = axs[0, 0]                                       # longitud del cilindre
corba(ax, s_c, s_t, C_CIL)
ax.set_ylabel(r"$s$ [m]")
ax.set_ylim(0, 1.1 * s_c.max())

ax = axs[1, 0]                                       # velocitat del cilindre (constant)
ax.axhline(0, color=INK2, lw=0.6, zorder=1)
corba(ax, np.full_like(phi, sdot), np.full(len(phi_taula), sdot), C_CIL)
ax.set_ylabel(r"$\dot s$ [m/s]")
ax.set_ylim(1.3 * min(sdot, 0), 1.3 * max(sdot, 0) + 0.05 * abs(sdot))

ax = axs[0, 1]                                       # angle de la manovella
corba(ax, phi, np.array(phi_taula, dtype=float), C_ANG)
ax.set_ylabel(r"$\varphi$ [$^\circ$]")
ax.set_ylim(0, 1.1 * phi_max)

ax = axs[1, 1]                                       # velocitat angular
corba(ax, pd, pd_t, C_ANG)
ax.set_ylabel(r"$\dot\varphi$ [rad/s]")
ax.set_ylim(0, 1.1 * pd.max())

format_eixos(axs.flat)
for ax in axs[1]:
    ax.set_xlabel(r"$\varphi$ [$^\circ$]")
for ax in axs[0]:
    eix_temps(ax)

fig.tight_layout()
fig.savefig("TME_ee_carregador.pdf")

# ---- figura 2: centre de gravetat del cos
fig3, axs3 = plt.subplots(1, 2, figsize=(7, 2.8))

ax = axs3[0]                                         # posició del CDG
corba(ax, rG[0], rG_t[:, 0], C_X, r"$x_G$")
corba(ax, rG[1], rG_t[:, 1], C_Y, r"$y_G$")
ax.set_ylabel(r"$\vec r_G$ [m]")
ax.set_ylim(0, 1.1 * max(rG[0].max(), rG[1].max()))
ax.legend(frameon=False, loc="lower left", fontsize=9)

ax = axs3[1]                                         # velocitat del CDG
ax.axhline(0, color=INK2, lw=0.6, zorder=1)
corba(ax, VG[0], VG_t[:, 0], C_X, r"$V_{G,x}$")
corba(ax, VG[1], VG_t[:, 1], C_Y, r"$V_{G,y}$")
ax.set_ylabel(r"$\vec V_G$ [m/s]")
ax.legend(frameon=False, loc="upper right", fontsize=9)

format_eixos(axs3)
for ax in axs3:
    ax.set_xlabel(r"$\varphi$ [$^\circ$]")
    eix_temps(ax)

fig3.tight_layout()
fig3.savefig("TME_ee_carregador_G.pdf")

text_caption = (rf"Carregador, $L={L}$ m, $\dot s={sdot}$ m/s constant "
                rf"(el cilindre es retrau).")
print(text_caption)


# ---------------------------------------------------------------- posicions del mecanisme
# Forma del cos en coordenades relatives a D (en unitats de L); DE és el costat inferior
FORMA = np.array([(-0.12, 0.00), (1.12, 0.00), (1.12, 0.78), (0.80, 0.78),
                  (0.55, 0.40), (0.30, 0.27), (-0.12, 0.20)])
L_CAMISA = 1.2   # m, longitud de la camisa del cilindre (ha de ser < s mínima)


def geometria(phi_graus):
    """Coordenades dels punts amb l'origen a B."""
    p = np.radians(phi_graus)
    A, B, C = np.array([-L, 0.0]), np.array([0.0, 0.0]), np.array([L, 0.0])
    D = L * np.array([np.cos(p), np.sin(p)])
    E = C + D
    G = E + np.array([-b, a])
    return A, B, C, D, E, G


def suport(ax, P, mida=0.13):
    """Articulació fixa: triangle i ratllat a sota."""
    x, y = P
    ax.fill([x, x - mida, x + mida], [y, y - 1.6 * mida, y - 1.6 * mida],
            color="white", ec=INK2, lw=1, zorder=2)
    ax.plot([x - 1.6 * mida, x + 1.6 * mida], [y - 1.6 * mida] * 2, color=INK2, lw=1)
    for k in np.linspace(-1.4, 1.2, 6):
        ax.plot([x + k * mida, x + (k + 0.4) * mida],
                [y - 2.2 * mida, y - 1.6 * mida], color=INK2, lw=0.6)


G_arc = np.array([geometria(p)[5] for p in np.linspace(phi_min, phi_max, 100)])

fig2, axs2 = plt.subplots(1, len(phi_dibuix), figsize=(11, 3.4))
for ax, ph in zip(np.atleast_1d(axs2), phi_dibuix):
    A, B, C, D, E, G = geometria(ph)

    ax.plot(*G_arc.T, ls="--", lw=0.8, color=C_X, alpha=0.8, zorder=2.5)  # trajectòria de G

    # cos DE (translació: la forma només es desplaça)
    ax.fill(*(D + L * FORMA).T, color=COS, ec=INK2, lw=1, zorder=2)

    # cilindre: tija prima de A a D i camisa gruixuda des de A
    u = (D - A) / np.linalg.norm(D - A)
    ax.plot(*np.c_[A, D], color=INK2, lw=2, zorder=3)
    ax.plot(*np.c_[A, A + L_CAMISA * u], color=C_CIL, lw=7,
            solid_capstyle="butt", zorder=4)

    # manovelles
    for P0, P1 in ((B, D), (C, E)):
        ax.plot(*np.c_[P0, P1], color=INK, lw=3.5, solid_capstyle="round", zorder=5)

    for P in (A, B, C):
        suport(ax, P)
    for P in (A, B, C, D, E):
        ax.plot(*P, "o", ms=6, color="white", mec=INK2, mew=1.2, zorder=6)
    ax.plot(*G, "o", ms=7, color=C_X, mec="white", mew=1, zorder=7)       # CDG

    if ph == phi_dibuix[0]:                      # etiquetes només al primer panell
        for nom, P, off in (("A", A, (-16, 3)), ("B", B, (-16, 3)), ("C", C, (-16, 3)),
                            ("D", D, (-14, 2)), ("E", E, (6, -10)), ("G", G, (6, 2))):
            ax.annotate(nom, P, xytext=off, textcoords="offset points", fontsize=16, color=INK)

    s_i, pd_i, _, _ = cinematica(ph)
    ax.set_title(rf"$\varphi={ph}^\circ$, $s={s_i:.2f}$ m, $t={temps(ph):.2f}$ s",
                 fontsize=16, color=INK)
    ax.set_aspect("equal")
    ax.set_xlim(-2.6, 3.6)
    ax.set_ylim(-0.5, 3.8)
    ax.axis("off")

fig2.tight_layout()
fig2.savefig("TME_ee_carregador_posicions.pdf")
plt.show()