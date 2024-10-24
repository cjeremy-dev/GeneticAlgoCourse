# Generate a code which draws the graph of the function f(x) = e ** x +2x  + 3 using matplotlib
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-10, 10, 100)
y = np.exp(x) + 2*x + 3
plt.plot(x, y)
