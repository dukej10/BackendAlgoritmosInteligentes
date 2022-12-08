import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# samplong


def sampling(x, mu, std):
    return (1/(np.sqrt(2*np.pi*std**2)))*np.exp(-(x-mu)**2/(2*std**2))


# Tptal process
mu = 0.2  # media partition
sigma = 0.1
delta = 0.5
n = 50000
x = np.zeros(n)
accept = 0

for i in range(0, n-1):
    y = x[i]+np.random.uniform(-delta, delta)
    if np.random.rand() < min(1, sampling(y, mu, sigma)/sampling(x[i], mu, sigma)):
        x[i+1] = y
        accept += 1
    else:
        x[i+1] = x[i]

print("The acceptance was: ", accept/n*100, "%")

plt.hist(x, density=True, bins=30)
xs = np.linspace(-1, 1, 100)
plt.plot(xs, sampling(xs, mu, sigma))
print("REMCMC: ", x[:100])