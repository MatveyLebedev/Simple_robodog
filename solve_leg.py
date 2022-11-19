import numpy as np
import pickle
import matplotlib.pyplot as plt

l1 = 98
l2 = 126
y0 = l1 + l2

leg_solves_x = np.zeros([181, 181])  # [a, b]
leg_solves_y = np.zeros([181, 181])  # [a, b]

for i, a in enumerate(np.linspace(-np.pi / 2, np.pi / 2, 181)):
    print(i)
    for j, b in enumerate(np.linspace(-np.pi / 2, np.pi / 2, 181)):
        x = l1 * np.sin(a) - l2 * np.sin(a - b)
        y = y0 - l1 * np.cos(a) - l2 * np.sin(np.pi / 2 - b + a)

        leg_solves_x[i, j] = x
        leg_solves_y[i, j] = y

with open('leg_solve_x.pickle', 'wb') as f:
    pickle.dump(leg_solves_x, f)

with open('leg_solve_y.pickle', 'wb') as f:
    pickle.dump(leg_solves_y, f)

print(leg_solves_x, leg_solves_y)
plt.plot(leg_solves_x[:, 80], leg_solves_y[:, 80])
plt.plot(leg_solves_x[80], leg_solves_y[80])
plt.xlim([-100, 100])
plt.ylim([-100, 100])
plt.show()
