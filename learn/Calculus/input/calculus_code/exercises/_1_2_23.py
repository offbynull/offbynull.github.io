from matplotlib import pyplot as plt
import numpy as np

# x = [4, 6, 8, 12, 16, 20, 30, 45, 60]
# y = [14.1, 13.0, 13.4, 12.5, 12.0, 12.4, 10.5, 9.4, 8.2]
# plt.scatter(x, y)
# x = np.linspace(0,60, 100)
# y = -0.105357143*x+14.52142858
# plt.plot(x, y)
# plt.show()

x = np.array([4, 6, 8, 12, 16, 20, 30, 45, 60])
y = np.array([14.1, 13.0, 13.4, 12.5, 12.0, 12.4, 10.5, 9.4, 8.2])
plt.scatter(x, y)
A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y, rcond=None)[0]
print(f'{m, c}')
x = np.linspace(0,60, 100)
y = m*x+c
plt.plot(x, y)
plt.show()

print(f'{m*25+c}')
print(f'{m*80+c}')