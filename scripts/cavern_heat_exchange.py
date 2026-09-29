"""Does the cavern rock heat or cool the stored air in cyclic operation?

Evidence for docs/02, "The cavern". A spherical salt cavern of volume V holds
well-mixed ideal-gas air; the air exchanges heat with the wall through h*A,
and the salt conducts radially (1-D, implicit in time) out to 300 m, where it
stays at the virgin rock temperature, 35.6 °C. Each day: charge 8 h at
``mdot`` with air at ``T_in``, dwell 4 h, discharge 8 h, dwell 4 h. The script
prints, after 1 day ... 20 years, the mass-averaged temperature of the
withdrawn air and the net heat the rock gave the air per kg cycled.

usage:  python scripts/cavern_heat_exchange.py T_in_C mdot_kg_s h_W_m2K V_m3
e.g.    python scripts/cavern_heat_exchange.py 20 185 15 5e5     (about 1.5 min)

Salt: k = 5.2 W/(m K), rho = 2160 kg/m3, c = 880 J/(kg K).
"""
import numpy as np, sys
from scipy.linalg import solve_banded
T_in = float(sys.argv[1]) + 273.15
mdot = float(sys.argv[2]); h = float(sys.argv[3]); V = float(sys.argv[4])
R = (3*V/(4*np.pi))**(1/3); A = 4*np.pi*R**2
k, rho, c = 5.2, 2160.0, 880.0
cp, cv, Rg = 1005.0, 718.0, 287.0
T_rock = 35.6 + 273.15
r = R + np.concatenate([[0.0], np.geomspace(0.01, 300.0, 120)])
n = r.size
rf = 0.5*(r[1:]+r[:-1]); G = k*4*np.pi*rf**2/np.diff(r)      # conductances between nodes
vol = np.empty(n)
vol[0] = 4/3*np.pi*(rf[0]**3 - r[0]**3)
vol[1:-1] = 4/3*np.pi*(rf[1:]**3 - rf[:-1]**3)
C = rho*c*vol
T = np.full(n, T_rock); Ta = T_rock
swing = mdot*8*3600
M = 100e5*V/(Rg*T_rock) - swing
dt = 600.0; spd = int(86400/dt)
def phase(s):
    t = (s*dt) % 86400
    return 1 if t < 8*3600 else (0 if t < 12*3600 else (-1 if t < 20*3600 else 0))
# rock part of the banded matrix, built once
m = n
base = np.zeros((3, m))
for i in range(n-1):
    j = i+1
    base[1, j] = C[i] + G[i]*dt + (h*A*dt if i == 0 else 0.0) + (G[i-1]*dt if i > 0 else 0.0)
    if i == 0:
        base[2, 0] = -h*A*dt
    else:
        base[2, j-1] = -G[i-1]*dt
    if i < n-2:
        base[0, j+1] = -G[i]*dt
base[0, 1] = -h*A*dt
Cfree = C[:n-1]
edge = G[n-2]*dt*T_rock
for day in range(1, 20*365+1):
    e = q = 0.0
    for s in range(spd):
        ph = phase(s)
        Mn = M + ph*mdot*dt
        base[1, 0] = Mn*cv + h*A*dt + (mdot*cp*dt if ph == -1 else 0.0)
        b = np.empty(m)
        b[0] = M*cv*Ta + (mdot*cp*T_in*dt if ph == 1 else 0.0)
        b[1:] = Cfree*T[:n-1]
        b[-1] += edge
        x = solve_banded((1, 1), base, b, check_finite=False)
        Ta_new = x[0]; T[:n-1] = x[1:]
        q += h*A*(T[0]-Ta_new)*dt
        if ph == -1:
            e += mdot*dt*Ta_new
        Ta = Ta_new; M = Mn
    if day in (1, 10, 100, 365, 3*365, 10*365, 20*365):
        print(f"day {day:5d}: withdrawn mean {e/swing-273.15:6.2f} C (injected {T_in-273.15:.1f}, rock {T_rock-273.15:.1f}); "
              f"net rock heat to air {q/swing/1e3:6.2f} kJ/kg; wall {T[0]-273.15:6.2f} C", flush=True)
