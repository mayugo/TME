#!/usr/bin/env python3
"""Carregador (quadrilàter articulat governat per un cilindre) - apartat d).

Origen a A; B=(L,0), C=(2L,0).  D = B + L(cos phi, sin phi),  E = C + L(cos phi, sin phi),
G = (E_x - b, D_y + a) = (2L - b + L cos phi,  a + L sin phi).
Enllaç del cilindre:  l = |AD| = 2 L cos(phi/2).
El cilindre es retrau: dl/dt = -|ldot| (constant).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ------------------------------- dades -------------------------------------
L, a, b = 2.0, 0.4, 0.2          # m
ldot = -0.2                      # m/s  (retracció: dl/dt < 0; |ldot| = 0,2 m/s)
PHI_DEG = (60.0, 90.0, 120.0)

# ------------------------- model analític (solució) -------------------------
def ell(phi):        return 2*L*np.cos(phi/2)
def phi_of_ell(l):   return 2*np.arccos(l/(2*L))
def phidot(phi):     return -ldot/(L*np.sin(phi/2))
def pos_G(phi):      return np.array([2*L - b + L*np.cos(phi), a + L*np.sin(phi)])
def vel_G(phi):      return L*phidot(phi)*np.array([-np.sin(phi), np.cos(phi)])   # = v_D = v_E

# ------------------- model geomètric independent (verificació) -------------
A, B, C = np.array([0., 0.]), np.array([L, 0.]), np.array([2*L, 0.])
def punts(phi):
    u = np.array([np.cos(phi), np.sin(phi)])
    D, E = B + L*u, C + L*u
    G = np.array([E[0] - b, D[1] + a])
    return D, E, G

def verifica(phi):
    D, E, G = punts(phi)
    assert np.isclose(np.linalg.norm(D - A), ell(phi))         # enllaç del cilindre
    assert np.allclose(E - D, [L, 0.0])                        # DE horitzontal i |DE| = L
    assert np.allclose(G, pos_G(phi))                          # posició de G

# ------------------------------- apartat d) --------------------------------
print(f"L = {L} m, a = {a} m, b = {b} m, dl/dt = {ldot} m/s\n")

print(f"{'phi':>5} {'l [m]':>8} {'phidot [rad/s]':>15} {'G = (x ; y) [m]':>18} "
      f"{'v_G = (vx ; vy) [m/s]':>24} {'|v| [m/s]':>10}")
for d in PHI_DEG:
    phi = np.radians(d); verifica(phi)
    G, v = pos_G(phi), vel_G(phi)
    print(f"{d:>4.0f}° {ell(phi):>8.4f} {phidot(phi):>15.5f} "
          f"({G[0]:6.3f} ; {G[1]:5.3f}) ({v[0]:8.4f} ; {v[1]:7.4f}) {np.linalg.norm(v):>10.4f}")

l60, l120 = ell(np.radians(60)), ell(np.radians(120))
t_total = (l60 - l120)/abs(ldot)
print(f"\nCursa del cilindre: {l60:.4f} -> {l120:.4f} m  (Δl = {l60-l120:.4f} m)")
print(f"Temps de φ = 60° a φ = 120°: t = {t_total:.3f} s")

# ---------- verificació temporal: derivada numèrica de G(t) vs solució -----
t = np.linspace(0.0, t_total, 2001)
l_t = l60 + ldot*t                          # dl/dt constant
phi_t = phi_of_ell(l_t)
assert np.isclose(np.degrees(phi_t[0]), 60) and np.isclose(np.degrees(phi_t[-1]), 120)
G_t = np.array([pos_G(p) for p in phi_t])
v_num = np.gradient(G_t, t, axis=0)
v_ana = np.array([vel_G(p) for p in phi_t])
assert np.allclose(v_num[2:-2], v_ana[2:-2], atol=2e-4), "v_G numèrica ≠ analítica"
assert np.allclose(np.gradient(phi_t, t)[2:-2], phidot(phi_t)[2:-2], atol=2e-4)
print("Verificacions OK (geometria, enllaç, DE horitzontal, derivada numèrica de G(t)).")

# ------------------------------- gràfics ------------------------------------
fig, ax = plt.subplots(1, 3, figsize=(16, 4.8), gridspec_kw={"width_ratios": [1.5, 1, 1]})

# (1) configuracions i trajectòria de G
th = np.linspace(np.radians(60), np.radians(120), 200)
Gc = np.array([pos_G(p) for p in th])
ax[0].plot(Gc[:, 0], Gc[:, 1], "k--", lw=1, label="trajectòria de G")
for d, c in zip(PHI_DEG, ("tab:blue", "tab:green", "tab:red")):
    phi = np.radians(d); D, E, G = punts(phi)
    ax[0].plot(*zip(B, D), c=c, lw=2.5); ax[0].plot(*zip(C, E), c=c, lw=2.5)
    ax[0].plot(*zip(A, D), c=c, lw=1.2, ls=":")
    ax[0].plot(*zip(D, E), c=c, lw=2.5); ax[0].plot(*G, "o", c=c, label=f"φ = {d:.0f}°")
    v = vel_G(phi); ax[0].annotate("", xy=G + 2.0*v, xytext=G, arrowprops=dict(arrowstyle="->", color=c))
for P, n in ((A, "A"), (B, "B"), (C, "C")):
    ax[0].plot(*P, "k^"); ax[0].text(P[0] - .12, P[1] - .25, n)
ax[0].set_aspect("equal"); ax[0].grid(alpha=.3); ax[0].legend(fontsize=7, loc="lower center", ncol=4)
ax[0].set_title("Configuracions, trajectòria i velocitat de G"); ax[0].set_xlabel("x [m]"); ax[0].set_ylabel("y [m]")

# (2) φ, φ̇ en funció del temps
ax[1].plot(t, np.degrees(phi_t), label=r"$\varphi$ [°]")
ax[1].set_xlabel("t [s]"); ax[1].set_ylabel(r"$\varphi$ [°]"); ax[1].grid(alpha=.3)
ax1b = ax[1].twinx(); ax1b.plot(t, phidot(phi_t), "tab:orange"); ax1b.set_ylabel(r"$\dot\varphi$ [rad/s]", color="tab:orange")
ax[1].set_title(r"$\varphi(t)$ i $\dot\varphi(t)$")

# (3) components i mòdul de la velocitat de G
ax[2].plot(t, v_ana[:, 0], label=r"$v_x$"); ax[2].plot(t, v_ana[:, 1], label=r"$v_y$")
ax[2].plot(t, np.linalg.norm(v_ana, axis=1), "k", label=r"$|v_G|$")
ax[2].set_xlabel("t [s]"); ax[2].set_ylabel("v [m/s]"); ax[2].grid(alpha=.3); ax[2].legend()
ax[2].set_title("Velocitat de G (= v_D = v_E)")

fig.tight_layout(); fig.savefig("carregador_apartat_d.png", dpi=130)
