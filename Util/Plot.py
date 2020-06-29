import matplotlib.pyplot as plt

@staticmethod
def generate_plot(path):
    plt.plot(path[2], path[1])
    plt.show()