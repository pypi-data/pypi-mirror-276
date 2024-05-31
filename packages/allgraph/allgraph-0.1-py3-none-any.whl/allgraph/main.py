# allgraph/main.py

import matplotlib.pyplot as plt

def make_bar_graph(**kwargs):
    data_x = kwargs.get('data_x', [1, 2, 3])
    data_y = kwargs.get('data_y', [5, 6, 7])
    title = kwargs.get('title', 'Bar Graph')
    xlabel = kwargs.get('xlabel', 'X-axis')
    ylabel = kwargs.get('ylabel', 'Y-axis')
    color = kwargs.get('color', 'blue')

    # Validation
    if len(data_x) != len(data_y):
        raise ValueError("data_x and data_y must be of the same length")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(data_x, data_y, color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def make_line_graph(**kwargs):
    data_x = kwargs.get('data_x', [1, 2, 3])
    data_y = kwargs.get('data_y', [1, 4, 9])
    title = kwargs.get('title', 'Line Graph')
    xlabel = kwargs.get('xlabel', 'X-axis')
    ylabel = kwargs.get('ylabel', 'Y-axis')
    color = kwargs.get('color', 'blue')
    linestyle = kwargs.get('linestyle', '-')
    marker = kwargs.get('marker', 'o')

    # Validation
    if len(data_x) != len(data_y):
        raise ValueError("data_x and data_y must be of the same length")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(data_x, data_y, color=color, linestyle=linestyle, marker=marker)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def make_histogram(**kwargs):
    data = kwargs.get('data', [1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
    bins = kwargs.get('bins', 10)
    title = kwargs.get('title', 'Histogram')
    xlabel = kwargs.get('xlabel', 'X-axis')
    ylabel = kwargs.get('ylabel', 'Frequency')
    color = kwargs.get('color', 'blue')

    # Plot
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=bins, color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def make_pie_chart(**kwargs):
    labels = kwargs.get('labels', ['A', 'B', 'C'])
    sizes = kwargs.get('sizes', [10, 20, 30])
    title = kwargs.get('title', 'Pie Chart')
    colors = kwargs.get('colors', None)
    autopct = kwargs.get('autopct', '%1.1f%%')

    # Plot
    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct=autopct, colors=colors, startangle=140)
    plt.title(title)
    plt.show()

def make_scatter_plot(**kwargs):
    data_x = kwargs.get('data_x', [1, 2, 3, 4, 5])
    data_y = kwargs.get('data_y', [5, 4, 3, 2, 1])
    title = kwargs.get('title', 'Scatter Plot')
    xlabel = kwargs.get('xlabel', 'X-axis')
    ylabel = kwargs.get('ylabel', 'Y-axis')
    color = kwargs.get('color', 'blue')
    marker = kwargs.get('marker', 'o')

    # Validation
    if len(data_x) != len(data_y):
        raise ValueError("data_x and data_y must be of the same length")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(data_x, data_y, color=color, marker=marker)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()
