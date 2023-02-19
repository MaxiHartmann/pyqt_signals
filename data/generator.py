import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### INPUTS
# time in seconds
time_start = 0
time_end = 1
dt=0.001
# frequency in hertz
f = 1
f2 = 0.5

filename=f"sine_f{f}.csv"
filename=f"sine_f{f}_f{f2}.csv"

t = np.arange(time_start, time_end, dt)
omega = 2 * np.pi * f
y = np.sin(omega * t)
y += np.sin(2 * np.pi * f2 * t)
plt.plot(t, y)
plt.show()
df = pd.DataFrame({"t": t, "y": y})
print(df.head())

print(f"Save: {filename}")
df.to_csv(filename)
