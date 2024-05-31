

import matplotlib.pyplot as plt
from typing import List, Tuple, Union, Optional
from matplotlib.colors import Normalize
import numpy as np
import squarify


def make_bar_graph(data_x: List[float], data_y: List[float], title: str = 'Bar Graph', xlabel: str = 'X-axis', ylabel: str = 'Y-axis', color: str = 'blue', alpha: float = 1.0, edgecolor: str = 'black', fontsize: int = 12, legend: bool = False, **kwargs):
    """
    Create a bar graph.

    Parameters:
        data_x (List[float]): Values for the x-axis. Example: [1, 2, 3, 4]
        data_y (List[float]): Values for the y-axis. Example: [10, 20, 30, 40]
        title (str, optional): Title of the graph. Defaults to 'Bar Graph'. Example: 'Sales Data'
        xlabel (str, optional): Label for the x-axis. Defaults to 'X-axis'. Example: 'Months'
        ylabel (str, optional): Label for the y-axis. Defaults to 'Y-axis'. Example: 'Revenue'
        color (str, optional): Color of the bars. Defaults to 'blue'. Example: 'red'
        alpha (float, optional): Transparency of the bars. Defaults to 1.0. Example: 0.5
        edgecolor (str, optional): Color of the edges of the bars. Defaults to 'black'. Example: 'gray'
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
        legend (bool, optional): Whether to display the legend. Defaults to False. Example: True
        **kwargs: Additional keyword arguments for matplotlib bar function.
    """
    # Validation
    if len(data_x) != len(data_y):
        raise ValueError("data_x and data_y must be of the same length")

    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(data_x, data_y, color=color, alpha=alpha, edgecolor=edgecolor, **kwargs)
    plt.title(title, fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    if legend:
        plt.legend(bars, [f'Bar {i+1}' for i in range(len(data_x))], fontsize=fontsize)
    plt.grid(True)
    plt.show()


def make_line_graph(data_x: List[float], data_y: List[float], title: str = 'Line Graph', xlabel: str = 'X-axis', ylabel: str = 'Y-axis', color: str = 'blue', linestyle: str = '-', marker: str = 'o', linewidth: float = 1.0, alpha: float = 1.0, markersize: float = 6.0, markeredgecolor: str = 'black', markeredgewidth: float = 1.0, markerfacecolor: str = 'blue', fontsize: int = 12):
    """
    Create a line graph.

    Parameters:
        data_x (List[float]): Values for the x-axis. Example: [1, 2, 3, 4]
        data_y (List[float]): Values for the y-axis. Example: [10, 20, 30, 40]
        title (str, optional): Title of the graph. Defaults to 'Line Graph'. Example: 'Sales Trend'
        xlabel (str, optional): Label for the x-axis. Defaults to 'X-axis'. Example: 'Months'
        ylabel (str, optional): Label for the y-axis. Defaults to 'Y-axis'. Example: 'Revenue'
        color (str, optional): Color of the line. Defaults to 'blue'. Example: 'red'
        linestyle (str, optional): Style of the line. Defaults to '-'. Example: '--'
        marker (str, optional): Marker style. Defaults to 'o'. Example: 's'
        linewidth (float, optional): Width of the line. Defaults to 1.0. Example: 2.0
        alpha (float, optional): Transparency of the line. Defaults to 1.0. Example: 0.5
        markersize (float, optional): Size of markers. Defaults to 6.0. Example: 8.0
        markeredgecolor (str, optional): Color of marker edges. Defaults to 'black'. Example: 'red'
        markeredgewidth (float, optional): Width of marker edges. Defaults to 1.0. Example: 2.0
        markerfacecolor (str, optional): Color of marker faces. Defaults to 'blue'. Example: 'green'
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
    """
    # Validation
    if len(data_x) != len(data_y):
        raise ValueError("data_x and data_y must be of the same length")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(data_x, data_y, color=color, linestyle=linestyle, marker=marker, linewidth=linewidth, alpha=alpha, markersize=markersize, markeredgecolor=markeredgecolor, markeredgewidth=markeredgewidth, markerfacecolor=markerfacecolor)
    plt.title(title, fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.grid(True)
    plt.show()


def make_histogram(data: List[float], title: str = 'Histogram', xlabel: str = 'X-axis', ylabel: str = 'Frequency', color: str = 'blue', bins: Union[int, List[float], str] = 10, range: Optional[Tuple[float, float]] = None, density: bool = False, cumulative: bool = False, histtype: str = 'bar', align: str = 'mid', orientation: str = 'vertical', rwidth: Optional[float] = None, fontsize: int = 12):
    """
    Create a histogram.

    Parameters:
        data (List[float]): Input data for the histogram. Example: [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
        title (str, optional): Title of the graph. Defaults to 'Histogram'. Example: 'Distribution of Scores'
        xlabel (str, optional): Label for the x-axis. Defaults to 'X-axis'. Example: 'Values'
        ylabel (str, optional): Label for the y-axis. Defaults to 'Frequency'. Example: 'Counts'
        color (str, optional): Color of the bars. Defaults to 'blue'. Example: 'green'
        bins (Union[int, List[float], str], optional): Number of bins or bin edges. Defaults to 10. Example: 20
        range (Optional[Tuple[float, float]], optional): Range of the histogram bins. Example: (0, 100)
        density (bool, optional): If True, the first element of the return tuple will be the counts normalized to form a probability density. Defaults to False. Example: True
        cumulative (bool, optional): If True, then a histogram is computed where each bin gives the counts in that bin plus all bins for smaller values. Defaults to False. Example: True
        histtype (str, optional): Type of histogram. Defaults to 'bar'. Example: 'step'
        align (str, optional): Controls how bars are aligned relative to their bin centers. Defaults to 'mid'. Example: 'left'
        orientation (str, optional): Orientation of the histogram. Defaults to 'vertical'. Example: 'horizontal'
        rwidth (Optional[float], optional): Relative width of bars as a fraction of bin width. Defaults to None. Example: 0.8
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
    """
    # Plot
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=bins, range=range, density=density, cumulative=cumulative, histtype=histtype, align=align, orientation=orientation, color=color, rwidth=rwidth)
    plt.title(title, fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.grid(True)
    plt.show()




def make_pie_chart(labels: List[str], sizes: List[float], title: str = 'Pie Chart', colors: Optional[List[str]] = None, startangle: float = 0, explode: Optional[Union[List[float], Tuple[float, ...]]] = None, shadow: bool = False, autopct: Optional[str] = '%1.1f%%', pctdistance: float = 0.6, labeldistance: float = 1.1, radius: float = 1, counterclock: bool = True, wedgeprops: Optional[dict] = None, textprops: Optional[dict] = None, fontsize: int = 12):
    """
    Create a pie chart.

    Parameters:
        labels (List[str]): Labels for each wedge of the pie. Example: ['A', 'B', 'C']
        sizes (List[float]): Sizes of each wedge. Example: [10, 20, 30]
        title (str, optional): Title of the graph. Defaults to 'Pie Chart'. Example: 'Distribution of Scores'
        colors (Optional[List[str]], optional): Colors for the wedges. Defaults to None. Example: ['red', 'green', 'blue']
        startangle (float, optional): Start angle for the pie chart. Defaults to 0. Example: 90
        explode (Optional[Union[List[float], Tuple[float, ...]]], optional): Fraction of the radius with which to offset each wedge. Defaults to None. Example: (0, 0.1, 0)
        shadow (bool, optional): If True, draws a shadow beneath the pie. Defaults to False. Example: True
        autopct (Optional[str], optional): Format string for the labels inside the wedges. Defaults to '%1.1f%%'. Example: '%.1f%%'
        pctdistance (float, optional): Distance from the center of each pie wedge at which the text should be drawn. Defaults to 0.6. Example: 0.8
        labeldistance (float, optional): Radial distance at which the pie labels are drawn. Defaults to 1.1. Example: 1.2
        radius (float, optional): Radius of the pie. Defaults to 1. Example: 1.5
        counterclock (bool, optional): If True, the wedges are drawn counterclockwise. Defaults to True. Example: False
        wedgeprops (Optional[dict], optional): Properties (like linewidth, edgecolor) of the wedge objects making up the pie. Defaults to None. Example: {'linewidth': 2, 'edgecolor': 'black'}
        textprops (Optional[dict], optional): Properties (like fontsize, fontweight) of the text objects for the labels. Defaults to None. Example: {'fontsize': 12, 'fontweight': 'bold'}
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
    """
    # Plot
    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, colors=colors, startangle=startangle, explode=explode, shadow=shadow, autopct=autopct, pctdistance=pctdistance, labeldistance=labeldistance, radius=radius, counterclock=counterclock, wedgeprops=wedgeprops, textprops=textprops)
    plt.title(title, fontsize=fontsize)
    plt.show()



def make_scatter_plot(data_x: List[float], data_y: List[float], title: str = 'Scatter Plot', xlabel: str = 'X-axis', ylabel: str = 'Y-axis', color: str = 'blue', marker: str = 'o', s: Optional[Union[int, List[int]]] = None, alpha: float = 1.0, edgecolors: str = 'none', linewidths: float = 1.0, cmap: Optional[str] = None, norm: Optional[Normalize] = None, vmin: Optional[float] = None, vmax: Optional[float] = None, fontsize: int = 12):
    """
    Create a scatter plot.

    Parameters:
        data_x (List[float]): Values for the x-axis. Example: [1, 2, 3, 4]
        data_y (List[float]): Values for the y-axis. Example: [10, 20, 30, 40]
        title (str, optional): Title of the graph. Defaults to 'Scatter Plot'. Example: 'Relationship between X and Y'
        xlabel (str, optional): Label for the x-axis. Defaults to 'X-axis'. Example: 'X Values'
        ylabel (str, optional): Label for the y-axis. Defaults to 'Y-axis'. Example: 'Y Values'
        color (str, optional): Color of the markers. Defaults to 'blue'. Example: 'red'
        marker (str, optional): Marker style for data points. Defaults to 'o'. Example: 's'
        s (Optional[Union[int, List[int]]], optional): Size of markers. Defaults to None. Example: 50
        alpha (float, optional): Transparency of markers. Defaults to 1.0. Example: 0.8
        edgecolors (str, optional): Color of marker edges. Defaults to 'none'. Example: 'black'
        linewidths (float, optional): Width of marker edges. Defaults to 1.0. Example: 2.0
        cmap (Optional[str], optional): Colormap for mapping scalar data to colors. Defaults to None. Example: 'viridis'
        norm (Optional[Normalize], optional): Normalization instance for scaling scalar data to the colormap. Defaults to None.
        vmin (Optional[float], optional): Minimum scalar value for colormap normalization. Defaults to None.
        vmax (Optional[float], optional): Maximum scalar value for colormap normalization. Defaults to None.
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
    """
    # Plot
    plt.figure(figsize=(10, 6))
    sc = plt.scatter(data_x, data_y, c=color, marker=marker, s=s, alpha=alpha, edgecolors=edgecolors, linewidths=linewidths, cmap=cmap, norm=norm, vmin=vmin, vmax=vmax)
    plt.colorbar(sc)  # Add colorbar if colormap is specified
    plt.title(title, fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.grid(True)
    plt.show()

#----------------------------------Phase 2-------------------------------------------# 



def make_area_chart(data_x: List[float], data_y: List[float], title: str = 'Area Chart', xlabel: str = 'X-axis', ylabel: str = 'Y-axis', color: str = 'blue', alpha: float = 1.0, linestyle: str = '-', linewidth: float = 1.0, fontsize: int = 12, legend: bool = False, **kwargs):
    """
    Create an area chart.

    Parameters:
        data_x (List[float]): Values for the x-axis. Example: [1, 2, 3, 4]
        data_y (List[float]): Values for the y-axis. Example: [10, 20, 30, 40]
        title (str, optional): Title of the graph. Defaults to 'Area Chart'. Example: 'Sales Data'
        xlabel (str, optional): Label for the x-axis. Defaults to 'X-axis'. Example: 'Months'
        ylabel (str, optional): Label for the y-axis. Defaults to 'Y-axis'. Example: 'Revenue'
        color (str, optional): Color of the area. Defaults to 'blue'. Example: 'red'
        alpha (float, optional): Transparency of the area. Defaults to 1.0. Example: 0.5
        linestyle (str, optional): Style of the line. Defaults to '-'. Example: '--'
        linewidth (float, optional): Width of the line. Defaults to 1.0. Example: 2.0
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
        legend (bool, optional): Whether to display the legend. Defaults to False. Example: True
        **kwargs: Additional keyword arguments for matplotlib plot function.
    """
    # Validation
    if len(data_x) != len(data_y):
        raise ValueError("data_x and data_y must be of the same length")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.fill_between(data_x, data_y, color=color, alpha=alpha, **kwargs)
    plt.plot(data_x, data_y, color=color, linestyle=linestyle, linewidth=linewidth, **kwargs)
    
    plt.title(title, fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    
    if legend:
        plt.legend([f'Area {i+1}' for i in range(len(data_x))], fontsize=fontsize)
    
    plt.grid(True)
    plt.show()





import matplotlib.pyplot as plt
from typing import List

def make_stacked_bar_chart(categories: List[str], data: List[List[float]], labels: List[str], title: str = 'Stacked Bar Chart', xlabel: str = 'X-axis', ylabel: str = 'Y-axis', colors: List[str] = None, fontsize: int = 12, legend: bool = True, **kwargs):
    """
    Create a stacked bar chart.

    Parameters:
        categories (List[str]): Categories for the x-axis. Example: ['A', 'B', 'C']
        data (List[List[float]]): Values for each stack segment. Example: [[10, 20, 30], [15, 25, 35]]
        labels (List[str]): Labels for each stack segment. Example: ['Segment 1', 'Segment 2']
        title (str, optional): Title of the graph. Defaults to 'Stacked Bar Chart'. Example: 'Sales Data'
        xlabel (str, optional): Label for the x-axis. Defaults to 'X-axis'. Example: 'Months'
        ylabel (str, optional): Label for the y-axis. Defaults to 'Y-axis'. Example: 'Revenue'
        colors (List[str], optional): Colors for each stack segment. Defaults to None. Example: ['red', 'blue']
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
        legend (bool, optional): Whether to display the legend. Defaults to True. Example: True
        **kwargs: Additional keyword arguments for matplotlib bar function.
    """
    # Validation
    if not all(isinstance(i, list) for i in data):
        raise ValueError("data should be a list of lists")
    if len(categories) != len(data[0]):
        raise ValueError("Length of categories and length of data columns must match")
    if colors and len(colors) != len(data):
        raise ValueError("Length of colors and length of data rows must match")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.35
    bar_positions = range(len(categories))
    
    # Initial bottom position is zero for all bars
    bottom = [0] * len(categories)
    
    for i, segment in enumerate(data):
        ax.bar(bar_positions, segment, bar_width, label=labels[i], bottom=bottom, color=colors[i] if colors else None, **kwargs)
        # Update bottom position for next segment
        bottom = [bottom[j] + segment[j] for j in range(len(segment))]

    ax.set_title(title, fontsize=fontsize)
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(categories, fontsize=fontsize)
    
    if legend:
        ax.legend(fontsize=fontsize)

    plt.show()




def make_box_plot(data: List[List[float]], labels: Optional[List[str]] = None, title: str = 'Box Plot', xlabel: str = 'Categories', ylabel: str = 'Values', color: str = 'blue', notch: bool = False, vert: bool = True, patch_artist: bool = False, showmeans: bool = False, showfliers: bool = True, showcaps: bool = True, showbox: bool = True, fontsize: int = 12):
    """
    Create a box plot.

    Parameters:
        data (List[List[float]]): List of data lists for each category. Example: [[10, 20, 30], [15, 25, 35], [20, 30, 40]]
        labels (List[str], optional): Labels for each category. Defaults to None. Example: ['Category 1', 'Category 2', 'Category 3']
        title (str, optional): Title of the graph. Defaults to 'Box Plot'. Example: 'Distribution of Scores'
        xlabel (str, optional): Label for the x-axis. Defaults to 'Categories'. Example: 'Groups'
        ylabel (str, optional): Label for the y-axis. Defaults to 'Values'. Example: 'Scores'
        color (str, optional): Color of the boxes. Defaults to 'blue'. Example: 'green'
        notch (bool, optional): Whether to draw a notch around the median. Defaults to False. Example: True
        vert (bool, optional): Whether to plot the boxes vertically. Defaults to True. Example: False
        patch_artist (bool, optional): Whether to fill the boxes with color. Defaults to False. Example: True
        showmeans (bool, optional): Whether to show the mean value. Defaults to False. Example: True
        showfliers (bool, optional): Whether to show the outliers. Defaults to True. Example: False
        showcaps (bool, optional): Whether to show the caps. Defaults to True. Example: False
        showbox (bool, optional): Whether to show the boxes. Defaults to True. Example: False
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
    """
    plt.figure(figsize=(10, 6))
    plt.boxplot(data, labels=labels, notch=notch, vert=vert, patch_artist=patch_artist,
                showmeans=showmeans, showfliers=showfliers, showcaps=showcaps, showbox=showbox)
    plt.title(title, fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.grid(True)
    plt.show()


def make_bubble_chart(data_x: List[float], data_y: List[float], sizes: List[float], title: str = 'Bubble Chart', xlabel: str = 'X-axis', ylabel: str = 'Y-axis', color: str = 'blue', alpha: float = 0.6, edgecolors: str = 'black', linewidths: float = 1.0, fontsize: int = 12):
    """
    Create a bubble chart.

    Parameters:
        data_x (List[float]): Values for the x-axis. Example: [1, 2, 3, 4]
        data_y (List[float]): Values for the y-axis. Example: [10, 20, 30, 40]
        sizes (List[float]): Sizes of the bubbles. Example: [50, 100, 150, 200]
        title (str, optional): Title of the graph. Defaults to 'Bubble Chart'. Example: 'Sales Data'
        xlabel (str, optional): Label for the x-axis. Defaults to 'X-axis'. Example: 'Months'
        ylabel (str, optional): Label for the y-axis. Defaults to 'Y-axis'. Example: 'Revenue'
        color (str, optional): Color of the bubbles. Defaults to 'blue'. Example: 'red'
        alpha (float, optional): Transparency of the bubbles. Defaults to 0.6. Example: 0.8
        edgecolors (str, optional): Color of bubble edges. Defaults to 'black'. Example: 'red'
        linewidths (float, optional): Width of bubble edges. Defaults to 1.0. Example: 2.0
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(data_x, data_y, s=sizes, c=color, alpha=alpha, edgecolors=edgecolors, linewidths=linewidths)
    plt.title(title, fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.grid(True)
    plt.show()



import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional


def make_heat_map(data: List[List[float]], x_labels: Optional[List[str]] = None, y_labels: Optional[List[str]] = None, title: str = 'Heat Map', xlabel: str = 'X-axis', ylabel: str = 'Y-axis', cmap: str = 'viridis', cbar_label: str = 'Values', fontsize: int = 12):
    """
    Create a heat map.

    Parameters:
        data (List[List[float]]): 2D array of values. Example: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        x_labels (List[str], optional): Labels for the x-axis. Defaults to None. Example: ['A', 'B', 'C']
        y_labels (List[str], optional): Labels for the y-axis. Defaults to None. Example: ['X', 'Y', 'Z']
        title (str, optional): Title of the graph. Defaults to 'Heat Map'. Example: 'Temperature Distribution'
        xlabel (str, optional): Label for the x-axis. Defaults to 'X-axis'. Example: 'Time'
        ylabel (str, optional): Label for the y-axis. Defaults to 'Y-axis'. Example: 'Frequency'
        cmap (str, optional): Colormap for mapping values to colors. Defaults to 'viridis'. Example: 'coolwarm'
        cbar_label (str, optional): Label for the color bar. Defaults to 'Values'. Example: 'Temperature (°C)'
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
    """
    plt.figure(figsize=(10, 6))
    plt.imshow(data, cmap=cmap, aspect='auto')
    plt.colorbar(label=cbar_label)
    plt.title(title, fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    if x_labels:
        plt.xticks(ticks=np.arange(len(x_labels)), labels=x_labels)
    if y_labels:
        plt.yticks(ticks=np.arange(len(y_labels)), labels=y_labels)
    plt.show()


def make_radar_chart(categories: List[str], values: List[float], title: str = 'Radar Chart', color: str = 'blue', alpha: float = 0.6, fontsize: int = 12):
    """
    Create a radar chart.

    Parameters:
        categories (List[str]): Labels for each category. Example: ['A', 'B', 'C', 'D']
        values (List[float]): Values for each category. Example: [0.6, 0.7, 0.8, 0.9]
        title (str, optional): Title of the graph. Defaults to 'Radar Chart'. Example: 'Performance Metrics'
        color (str, optional): Color of the radar area. Defaults to 'blue'. Example: 'green'
        alpha (float, optional): Transparency of the radar area. Defaults to 0.6. Example: 0.8
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
    """
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()

    values += values[:1]  # Close the plot
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color=color, alpha=alpha)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=fontsize)
    ax.set_title(title, fontsize=fontsize)
    ax.grid(True)
    plt.show()


#----------------------------Phase 3--------------------------------------------#
    

def make_treemap(data: List[float], labels: List[str], title: str = 'Treemap', colors: List[str] = None, alpha: float = 0.8, fontsize: int = 12, **kwargs):
    """
    Create a treemap using squarify and matplotlib.

    Parameters:
        data (List[float]): Sizes of the rectangles. Example: [50, 25, 25]
        labels (List[str]): Labels for each rectangle. Example: ['A', 'B', 'C']
        title (str, optional): Title of the graph. Defaults to 'Treemap'. Example: 'Category Distribution'
        colors (List[str], optional): Colors for each rectangle. Defaults to None. Example: ['red', 'blue', 'green']
        alpha (float, optional): Transparency of rectangles. Defaults to 0.8. Example: 0.7
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
        **kwargs: Additional keyword arguments for matplotlib text function.
    """
    if len(data) != len(labels):
        raise ValueError("data and labels must be of the same length")
    
    if colors is None:
        colors = plt.cm.tab20.colors  # Default color cycle
    elif len(colors) < len(data):
        raise ValueError("Not enough colors for the data provided")

    fig, ax = plt.subplots()
    ax.set_title(title, fontsize=fontsize)
    ax.axis('off')

    # Normalize data
    norm_data = [i / sum(data) for i in data]

    # Plot
    squarify.plot(sizes=norm_data, label=labels, color=colors, alpha=alpha, ax=ax, **kwargs)
    plt.show()




def make_waterfall_chart(categories: List[str], values: List[float], title: str = 'Waterfall Chart', xlabel: str = 'Categories', ylabel: str = 'Values', colors: List[str] = None, fontsize: int = 12, **kwargs):
    """
    Create a waterfall chart.

    Parameters:
        categories (List[str]): Labels for each bar. Example: ['A', 'B', 'C']
        values (List[float]): Values for each bar. Example: [10, -5, 15]
        title (str, optional): Title of the graph. Defaults to 'Waterfall Chart'. Example: 'Financial Changes'
        xlabel (str, optional): Label for the x-axis. Defaults to 'Categories'. Example: 'Stages'
        ylabel (str, optional): Label for the y-axis. Defaults to 'Values'. Example: 'Amount'
        colors (List[str], optional): Colors for each bar. Defaults to None. Example: ['green', 'red', 'blue']
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
        **kwargs: Additional keyword arguments for matplotlib bar function.
    """
    # Validation
    if len(categories) != len(values):
        raise ValueError("categories and values must be of the same length")

    # Compute cumulative values
    cumulative = np.cumsum(values)
    total = cumulative[-1]

    # Bar colors
    if colors is None:
        colors = ['green' if v >= 0 else 'red' for v in values]

    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(categories, values, color=colors, edgecolor='black', **kwargs)
    plt.plot(categories, cumulative, color='blue', marker='o', linestyle='-', linewidth=2, markersize=8)
    
    # Annotate values
    for i, (category, value) in enumerate(zip(categories, values)):
        plt.text(i, value/2, f'{value}', ha='center', va='center', color='black', fontsize=fontsize)
        plt.text(i, cumulative[i], f'{cumulative[i]}', ha='center', va='bottom', color='blue', fontsize=fontsize)

    plt.title(title, fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.grid(True)
    plt.show()



import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from typing import List

def make_gantt_chart(tasks: List[str], start_dates: List[str], end_dates: List[str], title: str = 'Gantt Chart', xlabel: str = 'Date', ylabel: str = 'Tasks', colors: List[str] = None, fontsize: int = 12, **kwargs):
    """
    Create a Gantt chart.

    Parameters:
        tasks (List[str]): Labels for each task. Example: ['Task 1', 'Task 2']
        start_dates (List[str]): Start dates for each task. Example: ['2021-01-01', '2021-01-05']
        end_dates (List[str]): End dates for each task. Example: ['2021-01-10', '2021-01-15']
        title (str, optional): Title of the graph. Defaults to 'Gantt Chart'. Example: 'Project Timeline'
        xlabel (str, optional): Label for the x-axis. Defaults to 'Date'. Example: 'Timeline'
        ylabel (str, optional): Label for the y-axis. Defaults to 'Tasks'. Example: 'Project Tasks'
        colors (List[str], optional): Colors for each task. Defaults to None. Example: ['red', 'blue']
        fontsize (int, optional): Font size for text elements. Defaults to 12. Example: 14
        **kwargs: Additional keyword arguments for matplotlib barh function.
    """
    if len(tasks) != len(start_dates) or len(tasks) != len(end_dates):
        raise ValueError("tasks, start_dates, and end_dates must be of the same length")
    
    # Convert dates to datetime objects
    start_dates = [datetime.strptime(date, '%Y-%m-%d') for date in start_dates]
    end_dates = [datetime.strptime(date, '%Y-%m-%d') for date in end_dates]
    
    # Calculate durations
    durations = [(end - start).days for start, end in zip(start_dates, end_dates)]

    # Colors
    if colors is None:
        colors = plt.cm.tab20.colors

    fig, ax = plt.subplots()
    for i, task in enumerate(tasks):
        ax.barh(task, durations[i], left=start_dates[i], color=colors[i % len(colors)], edgecolor='black', **kwargs)
    
    # Format the x-axis to show dates
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.title(title, fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.grid(True)
    plt.show()


