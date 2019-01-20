import matplotlib.pyplot as plt


class Plot:
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values

    def set_x_values(self, x_values):
        self.x_values = x_values

    def set_y_values(self, y_values):
        self.y_values = y_values

    def create_line_plot(self, x_label, y_label, legend, save_path="", title=""):
        for i in range(0, len(self.x_values)):
            plt.plot(self.x_values[i], self.y_values[i], label=legend[i])
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.legend()
        plt.savefig(save_path + title.replace(" ", "_"))
        plt.close()


def try_out():
    x_values = [[1, 5, 10], [1, 5, 10]]
    y_values = [[20, 25, 50], [10, 40, 70]]
    legend = ["proov1", "proov2"]
    x_label = "Passengers"
    y_label = "avg_time"
    plot = Plot(x_values, y_values)
    plot.create_line_plot(x_label, y_label, legend, title="Try")


if __name__ == "__main__":
    try_out()
