#!/usr/bin/env python3
"""Cinemàtica (theta de 0 a 60°) del mecanisme A-E (dolla) - guia BD.  h = L, AE = L, BD = 2L.
Origen a B, A = (0, L). theta: AE per sota de l'horitzontal; alpha: BD per sobre.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

L = 1.0            # m
thd = 3.0          # rad/s (constant, sentit horari)

# ---------- solució analítica ----------
def sol(th):
    al   = np.pi/4 - th/2                    # alpha
    s    = 2*L*np.sin(al)                    # BE
    ald  = -thd/2*np.ones_like(th)           # alpha punt
    sd   = -L*thd*np.cos(al)                 # s punt
    vD   = 2*L*np.abs(ald)                   # |v_D|
    vDv  = 2*L*ald*np.stack([-np.sin(al), np.cos(al)])   # components (x,y)
    return al, s, ald, sd, vD, vDv

# ---------- comprovació independent: equacions d'enllaç generals ----------
def sol_num(th):
    # resol L cos th = s cos a ; L - L sin th = s sin a
    s  = np.hypot(L*np.cos(th), L - L*np.sin(th))
    al = np.arctan2(L - L*np.sin(th), L*np.cos(th))
    return al, s

th = np.radians(np.linspace(0, 60, 601))
al, s, ald, sd, vD, vDv = sol(th)
al_n, s_n = sol_num(th)
assert np.allclose(al, al_n) and np.allclose(s, s_n), "posicions no coincideixen"

# derivades numèriques respecte al temps (theta = thd*t)
t = th/thd
assert np.allclose(np.gradient(al_n, t)[2:-2], ald[2:-2], atol=1e-3)
assert np.allclose(np.gradient(s_n,  t)[2:-2], sd[2:-2],  atol=1e-3)

# comprovació: v_E absolut = L*thd (perp. a AE) = sd*u_BD + s*ald*n_BD
vE_abs = np.hypot(sd, s*ald)
assert np.allclose(vE_abs, L*thd), "|v_E| ha de ser L*thetadot"
print("Verificacions OK (posició, derivades numèriques, |v_E| = L*thetadot)\n")

# ---------- apartat c) ----------
print(f"L = {L} m, thetadot = {thd} rad/s")
print(f"{'theta':>6} {'alpha':>7} {'BE (m)':>8} {'alpha_d':>9} {'s_d (m/s)':>10} "
      f"{'|vD|':>6} {'vD_x':>7} {'vD_y':>7} {'|vG|':>6}")
for deg in (0, 30, 60):
    x = np.radians(np.array([deg], float))
    a, ss, ad, sdd, v, vv = sol(x)
    print(f"{deg:>5}° {np.degrees(a[0]):>6.2f}° {ss[0]:>8.4f} {ad[0]:>9.3f} {sdd[0]:>10.4f} "
          f"{v[0]:>6.3f} {vv[0,0]:>7.3f} {vv[1,0]:>7.3f} {v[0]/2:>6.3f}")

# ---------- gràfiques ----------
deg = np.degrees(th)
fig, ax = plt.subplots(2, 2, figsize=(10, 7), sharex=True)
ax[0,0].plot(deg, np.degrees(al)); ax[0,0].set_ylabel(r"$\alpha$ [°]")
ax[0,1].plot(deg, s);              ax[0,1].set_ylabel("BE  [m]")
ax[1,0].plot(deg, ald, label=r"$\dot\alpha$ [rad/s]")
ax[1,0].plot(deg, sd,  label=r"$\dot s$ [m/s]")
ax[1,0].plot(deg, vD,  label=r"$|v_D|$ [m/s]"); ax[1,0].legend()
ax[1,1].plot(deg, vDv[0], label=r"$v_{D,x}$"); ax[1,1].plot(deg, vDv[1], label=r"$v_{D,y}$")
ax[1,1].set_ylabel("v_D [m/s]"); ax[1,1].legend()
for a_ in ax.flat:
    a_.grid(alpha=.3)
    for d_ in (0, 30, 60): a_.axvline(d_, color='gray', ls=':', lw=.8)
for a_ in ax[1]: a_.set_xlabel(r"$\theta$ [°]")
fig.suptitle(rf"$L={L}$ m, $\dot\theta={thd}$ rad/s")
fig.tight_layout(); fig.savefig("cinematica_guia.png", dpi=130)

# ---------- configuracions (dibuix) ----------
fig2, a2 = plt.subplots(figsize=(5.5, 4))
for d, c in ((0, "tab:blue"), (30, "tab:red"), (60, "tab:green")):
    x = np.radians(d); al_ = np.pi/4 - x/2
    A = np.array([0, L]); B = np.array([0, 0])
    E = np.array([L*np.cos(x), L - L*np.sin(x)])
    D = 2*L*np.array([np.cos(al_), np.sin(al_)])
    a2.plot(*zip(A, E), c=c, lw=3); a2.plot(*zip(B, D), c=c, lw=1.5, label=f"θ = {d}°")
    a2.plot(*E, "s", c=c)
a2.plot(0, L, "k^"); a2.plot(0, 0, "k^")
a2.text(-.12, L, "A"); a2.text(-.12, 0, "B")
a2.set_aspect("equal"); a2.legend(); a2.grid(alpha=.3)
fig2.savefig("cinematica_guia_config.png", dpi=130)