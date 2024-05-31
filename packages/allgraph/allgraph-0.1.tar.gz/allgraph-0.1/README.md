# AllGraph

AllGraph is a Python library for creating various types of charts and graphs with ease.


## List of all the graphs that can be made using allgraph.py

- Bar Chart
- Line Graph
- Histogram
- Pie Chart
- Scatter Plot
- Area Chart
- Stacked Bar Chart
- Box Plot
- Bubble Chart
- Heat Map
- Radar Chart
- Tree Diagram
- Waterfall Chart
- Gantt Chart




## Installation

You can install AllGraph using pip. Simply run the following command:

```bash
pip install allgraph

```

# make_bar_graph

The `make_bar_graph` function is used to create a bar graph using the provided data.

## Usage

```python
from allgraph import make_bar_graph

# Example data
data_x = [1, 2, 3, 4]
data_y = [10, 20, 30, 40]

# Basic usage
make_bar_graph(data_x, data_y)

```

## Parameters

* `data_x (List[float])`: Values for the x-axis.
* `data_y (List[float])`: Values for the y-axis.
* `title (str, optional)`: Title of the graph. Defaults to 'Bar Graph'.
* `xlabel (str, optional)`: Label for the x-axis. Defaults to 'X-axis'.
* `ylabel (str, optional)`: Label for the y-axis. Defaults to 'Y-axis'.
* `color (str, optional)`: Color of the bars. Defaults to 'blue'.
* `alpha (float, optional)`: Transparency of the bars. Defaults to 1.0.
* `edgecolor (str, optional)`: Color of the edges of the bars. Defaults to 'black'.
* `fontsize (int, optional)`: Font size for text elements. Defaults to 12.
* `legend (bool, optional)`: Whether to display the legend. Defaults to False.
* `**kwargs`: Additional keyword arguments for matplotlib bar function.




# make_line_graph

The `make_line_graph` function is used to create a line graph using the provided data.

## Usage

```python
from allgraph import make_line_graph

# Example data
data_x = [1, 2, 3, 4]
data_y = [10, 20, 30, 40]

# Basic usage
make_line_graph(data_x, data_y)
```

## Parameters

* `data_x (List[float])`: Values for the x-axis.
* `data_y (List[float])`: Values for the y-axis.
* `title (str, optional)`: Title of the graph. Defaults to 'Line Graph'.
* `xlabel (str, optional)`: Label for the x-axis. Defaults to 'X-axis'.
* `ylabel (str, optional)`: Label for the y-axis. Defaults to 'Y-axis'.
* `color (str, optional)`: Color of the line. Defaults to 'blue'.
* `linestyle (str, optional)`: Line style. Defaults to '-'.
* `linewidth (float, optional)`: Line width. Defaults to 1.0.
* `marker (str, optional)`: Marker style. Defaults to 'o'.
* `markersize (float, optional)`: Marker size. Defaults to 5.0.
* `legend (bool, optional)`: Whether to display the legend. Defaults to False.
* `**kwargs`: Additional keyword arguments for matplotlib plot function.


# make_histogram

The `make_histogram` function is used to create a histogram using the provided data.

## Usage

```python
from allgraph import make_histogram

# Example data
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

# Basic usage
make_histogram(data)

```

## Parameters

* `data (List[float])`: Input data for the histogram.
* `title (str, optional)`: Title of the graph. Defaults to 'Histogram'.
* `xlabel (str, optional)`: Label for the x-axis. Defaults to 'X-axis'.
* `ylabel (str, optional)`: Label for the y-axis. Defaults to 'Frequency'.
* `color (str, optional)`: Color of the bars. Defaults to 'blue'.
* `bins (Union[int, List[float], str], optional)`: Number of bins or bin edges. Defaults to 10.
* `range (Optional[Tuple[float, float]], optional)`: Range of the histogram bins.
* `density (bool, optional)`: If True, the first element of the return tuple will be the counts normalized to form a probability density. Defaults to False.
* `cumulative (bool, optional)`: If True, then a histogram is computed where each bin gives the counts in that bin plus all bins for smaller values. Defaults to False.
* `histtype (str, optional)`: Type of histogram. Defaults to 'bar'.
* `align (str, optional)`: Controls how bars are aligned relative to their bin centers. Defaults to 'mid'.
* `orientation (str, optional)`: Orientation of the histogram. Defaults to 'vertical'.
* `rwidth (Optional[float], optional)`: Relative width of bars as a fraction of bin width. Defaults to None.
* `fontsize (int, optional)`: Font size for text elements. Defaults to 12.


# make_pie_chart

The `make_pie_chart` function is used to create a pie chart using the provided data.

## Usage

```python
from allgraph import make_pie_chart

# Example data
labels = ['A', 'B', 'C']
sizes = [10, 20, 30]

# Basic usage
make_pie_chart(labels, sizes)
```

## Parameters

* `labels (List[str])`: Labels for each wedge of the pie.
* `sizes (List[float])`: Sizes of each wedge.
* `title (str, optional)`: Title of the graph. Defaults to 'Pie Chart'.
* `colors (Optional[List[str]], optional)`: Colors for the wedges. Defaults to None.
* `startangle (float, optional)`: Start angle for the pie chart. Defaults to 0.
* `explode (Optional[Union[List[float], Tuple[float, ...]]], optional)`: Fraction of the radius with which to offset each wedge. Defaults to None.
* `shadow (bool, optional)`: If True, draws a shadow beneath the pie. Defaults to False.
* `autopct (Optional[str], optional)`: Format string for the labels inside the wedges. Defaults to '%1.1f%%'.
* `pctdistance (float, optional)`: Distance from the center of each pie wedge at which the text should be drawn. Defaults to 0.6.
* `labeldistance (float, optional)`: Radial distance at which the pie labels are drawn. Defaults to 1.1.
* `radius (float, optional)`: Radius of the pie. Defaults to 1.
* `counterclock (bool, optional)`: If True, the wedges are drawn counterclockwise. Defaults to True.
* `wedgeprops (Optional[dict], optional)`: Properties (like linewidth, edgecolor) of the wedge objects making up the pie. Defaults to None.
* `textprops (Optional[dict], optional)`: Properties (like fontsize, fontweight) of the text objects for the labels. Defaults to None.
* `fontsize (int, optional)`: Font size for text elements. Defaults to 12.



# make_scatter_plot

The `make_scatter_plot` function is used to create a scatter plot using the provided data.

## Usage

```python
from allgraph import make_scatter_plot

# Example data
data_x = [1, 2, 3, 4]
data_y = [10, 20, 30, 40]

# Basic usage
make_scatter_plot(data_x, data_y)
```

## Parameters

* `data_x (List[float])`: Values for the x-axis.
* `data_y (List[float])`: Values for the y-axis.
* `title (str, optional)`: Title of the graph. Defaults to 'Scatter Plot'.
* `xlabel (str, optional)`: Label for the x-axis. Defaults to 'X-axis'.
* `ylabel (str, optional)`: Label for the y-axis. Defaults to 'Y-axis'.
* `color (str, optional)`: Color of the markers. Defaults to 'blue'.
* `marker (str, optional)`: Marker style for data points. Defaults to 'o'.
* `s (Optional[Union[int, List[int]]], optional)`: Size of markers. Defaults to None.
* `alpha (float, optional)`: Transparency of markers. Defaults to 1.0.
* `edgecolors (str, optional)`: Color of marker edges. Defaults to 'none'.
* `linewidths (float, optional)`: Width of marker edges. Defaults to 1.0.
* `cmap (Optional[str], optional)`: Colormap for mapping scalar data to colors. Defaults to None.
* `norm (Optional[Normalize], optional)`: Normalization instance for scaling scalar data to the colormap. Defaults to None.
* `vmin (Optional[float], optional)`: Minimum scalar value for colormap normalization. Defaults to None.
* `vmax (Optional[float], optional)`: Maximum scalar value for colormap normalization. Defaults to None.
* `fontsize (int, optional)`: Font size for text elements. Defaults to 12.


# make_area_chart

The `make_area_chart` function is used to create an area chart using the provided data.

## Usage

```python
from allgraph import make_area_chart

# Example data
data_x = [1, 2, 3, 4]
data_y = [10, 20, 30, 40]

# Basic usage
make_area_chart(data_x, data_y)
```

## Parameters

* `data_x (List[float])`: Values for the x-axis.
* `data_y (List[float])`: Values for the y-axis.
* `title (str, optional)`: Title of the graph. Defaults to 'Area Chart'.
* `xlabel (str, optional)`: Label for the x-axis. Defaults to 'X-axis'.
* `ylabel (str, optional)`: Label for the y-axis. Defaults to 'Y-axis'.
* `color (str, optional)`: Color of the area. Defaults to 'blue'.
* `alpha (float, optional)`: Transparency of the area. Defaults to 1.0.
* `linestyle (str, optional)`: Style of the line. Defaults to '-'.
* `linewidth (float, optional)`: Width of the line. Defaults to 1.0.
* `fontsize (int, optional)`: Font size for text elements. Defaults to 12.
* `legend (bool, optional)`: Whether to display the legend. Defaults to False.
* `**kwargs`: Additional keyword arguments for matplotlib plot function.


# make_stacked_bar_chart

The `make_stacked_bar_chart` function is used to create a stacked bar chart using the provided data.

## Usage

```python
from allgraph import make_stacked_bar_chart

# Example data
categories = ['A', 'B', 'C']
data = [[10, 20, 30], [15, 25, 35]]
labels = ['Segment 1', 'Segment 2']

# Basic usage
make_stacked_bar_chart(categories, data, labels)
```

## Parameters

* `categories (List[str])`: Categories for the x-axis. Example: ['A', 'B', 'C']
* `data (List[List[float]])`: Values for each stack segment. Example: [[10, 20, 30], [15, 25, 35]]
* `labels (List[str])`: Labels for each stack segment. Example: ['Segment 1', 'Segment 2']
* `title (str, optional)`: Title of the graph. Defaults to 'Stacked Bar Chart'. Example: 'Sales Data'
* `xlabel (str, optional)`: Label for the x-axis. Defaults to 'X-axis'. Example: 'Months'
* `ylabel (str, optional)`: Label for the y-axis. Defaults to 'Y-axis'. Example: 'Revenue'
* `colors (List[str], optional)`: Colors for each stack segment. Defaults to None. Example: ['red', 'blue']
* `fontsize (int, optional)`: Font size for text elements. Defaults to 12. Example: 14
* `legend (bool, optional)`: Whether to display the legend. Defaults to True. Example: True
* `**kwargs`: Additional keyword arguments for matplotlib bar function.


# make_box_plot

The `make_box_plot` function is used to create a box plot using the provided data.

## Usage

```python
from allgraph import make_box_plot

# Example data
data = [[10, 20, 30], [15, 25, 35], [20, 30, 40]]

# Basic usage
make_box_plot(data)
```

## Parameters

* `data (List[List[float]])`: List of data lists for each category. Example: [[10, 20, 30], [15, 25, 35], [20, 30, 40]]
* `labels (List[str], optional)`: Labels for each category. Defaults to None. Example: ['Category 1', 'Category 2', 'Category 3']
* `title (str, optional)`: Title of the graph. Defaults to 'Box Plot'. Example: 'Distribution of Scores'
* `xlabel (str, optional)`: Label for the x-axis. Defaults to 'Categories'. Example: 'Groups'
* `ylabel (str, optional)`: Label for the y-axis. Defaults to 'Values'. Example: 'Scores'
* `color (str, optional)`: Color of the boxes. Defaults to 'blue'. Example: 'green'
* `notch (bool, optional)`: Whether to draw a notch around the median. Defaults to False. Example: True
* `vert (bool, optional)`: Whether to plot the boxes vertically. Defaults to True. Example: False
* `patch_artist (bool, optional)`: Whether to fill the boxes with color. Defaults to False. Example: True
* `showmeans (bool, optional)`: Whether to show the mean value. Defaults to False. Example: True
* `showfliers (bool, optional)`: Whether to show the outliers. Defaults to True. Example: False
* `showcaps (bool, optional)`: Whether to show the caps. Defaults to True. Example: False
* `showbox (bool, optional)`: Whether to show the boxes. Defaults to True. Example: False
* `fontsize (int, optional)`: Font size for text elements. Defaults to 12. Example: 14



# make_bubble_chart

The `make_bubble_chart` function is used to create a bubble chart using the provided data.

## Usage

```python
from allgraph import make_bubble_chart

# Example data
data_x = [1, 2, 3, 4]
data_y = [10, 20, 30, 40]
sizes = [50, 100, 150, 200]

# Basic usage
make_bubble_chart(data_x, data_y, sizes)
```

## Parameters

* `data_x (List[float])`: Values for the x-axis.
* `data_y (List[float])`: Values for the y-axis.
* `sizes (List[float])`: Sizes of the bubbles.
* `title (str, optional)`: Title of the graph. Defaults to 'Bubble Chart'.
* `xlabel (str, optional)`: Label for the x-axis. Defaults to 'X-axis'.
* `ylabel (str, optional)`: Label for the y-axis. Defaults to 'Y-axis'.
* `color (str, optional)`: Color of the bubbles. Defaults to 'blue'.
* `alpha (float, optional)`: Transparency of the bubbles. Defaults to 0.6.
* `edgecolors (str, optional)`: Color of bubble edges. Defaults to 'black'.
* `linewidths (float, optional)`: Width of bubble edges. Defaults to 1.0.
* `fontsize (int, optional)`: Font size for text elements. Defaults to 12.


# make_heat_map

The `make_heat_map` function is used to create a heat map using the provided data.

## Usage

```python
from allgraph import make_heat_map

# Example data
data = [
    [0.1, 0.2, 0.3, 0.4, 0.5],
    [0.6, 0.7, 0.8, 0.9, 0.1],
    [0.2, 0.3, 0.4, 0.5, 0.6],
    [0.7, 0.8, 0.9, 0.1, 0.2],
    [0.3, 0.4, 0.5, 0.6, 0.7]
]

# Basic usage
make_heat_map(data)

```

* `data (List[List[float]])`: 2D array of values. Example: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
* `x_labels (List[str], optional)`: Labels for the x-axis. Defaults to None. Example: ['A', 'B', 'C']
* `y_labels (List[str], optional)`: Labels for the y-axis. Defaults to None. Example: ['X', 'Y', 'Z']
* `title (str, optional)`: Title of the graph. Defaults to 'Heat Map'. Example: 'Temperature Distribution'
* `xlabel (str, optional)`: Label for the x-axis. Defaults to 'X-axis'. Example: 'Time'
* `ylabel (str, optional)`: Label for the y-axis. Defaults to 'Y-axis'. Example: 'Frequency'
* `cmap (str, optional)`: Colormap for mapping values to colors. Defaults to 'viridis'. Example: 'coolwarm'
* `cbar_label (str, optional)`: Label for the color bar. Defaults to 'Values'. Example: 'Temperature (°C)'
* `fontsize (int, optional)`: Font size for text elements. Defaults to 12. Example: 14


# make_radar_chart

The `make_radar_chart` function is used to create a radar chart using the provided data.

## Usage

```python
from allgraph import make_radar_chart

# Example data
categories = ['A', 'B', 'C', 'D']
values = [0.6, 0.7, 0.8, 0.9]

# Basic usage
make_radar_chart(categories, values)
```

* `categories (List[str])`: Labels for each category. Example: `['A', 'B', 'C', 'D']`
* `values (List[float])`: Values for each category. Example: `[0.6, 0.7, 0.8, 0.9]`
* `title (str, optional)`: Title of the graph. Defaults to `'Radar Chart'`. Example: `'Performance Metrics'`
* `color (str, optional)`: Color of the radar area. Defaults to `'blue'`. Example: `'green'`
* `alpha (float, optional)`: Transparency of the radar area. Defaults to `0.6`. Example: `0.8`
* `fontsize (int, optional)`: Font size for text elements. Defaults to `12`. Example: `14`


# make_treemap

The `make_treemap` function is used to create a treemap using squarify and matplotlib.

## Usage

```python
from allgraph import make_treemap

# Example data
data = [50, 25, 25]
labels = ['A', 'B', 'C']
colors = ['red', 'blue', 'green']

# Basic usage
make_treemap(data, labels, colors=colors)
```

## Parameters

- `data (List[float])`: Sizes of the rectangles. Example: [50, 25, 25]
- `labels (List[str])`: Labels for each rectangle. Example: ['A', 'B', 'C']
- `title (str, optional)`: Title of the graph. Defaults to 'Treemap'. Example: 'Category Distribution'
- `colors (List[str], optional)`: Colors for each rectangle. Defaults to None. Example: ['red', 'blue', 'green']
- `alpha (float, optional)`: Transparency of rectangles. Defaults to 0.8. Example: 0.7
- `fontsize (int, optional)`: Font size for text elements. Defaults to 12. Example: 14
- `**kwargs`: Additional keyword arguments for matplotlib text function.



# make_waterfall_chart

The `make_waterfall_chart` function is used to create a waterfall chart.

## Usage

```python
from allgraph import make_waterfall_chart

# Example data
categories = ['Initial', 'Income', 'Expense', 'Profit']
values = [100, 200, -150, 50]

# Basic usage
make_waterfall_chart(categories, values)
```

## Parameters

* `categories (List[str])`: Labels for each bar. Example: ['Initial', 'Income', 'Expense', 'Profit']
* `values (List[float])`: Values for each bar. Example: [100, 200, -150, 50]
* `title (str, optional)`: Title of the graph. Defaults to 'Waterfall Chart'. Example: 'Financial Changes'
* `xlabel (str, optional)`: Label for the x-axis. Defaults to 'Categories'. Example: 'Stages'
* `ylabel (str, optional)`: Label for the y-axis. Defaults to 'Values'. Example: 'Amount'
* `colors (List[str], optional)`: Colors for each bar. Defaults to None. Example: ['green', 'red', 'blue']
* `fontsize (int, optional)`: Font size for text elements. Defaults to 12. Example: 14
* `**kwargs`: Additional keyword arguments for matplotlib bar function.



# make_gantt_chart

The `make_gantt_chart` function is used to create a gantt chart.

## Usage

```python
from allgraph import make_gantt_chart

# Example data
tasks = ['Task 1', 'Task 2', 'Task 3']
start_dates = ['2021-01-01', '2021-01-05', '2021-01-10']
end_dates = ['2021-01-10', '2021-01-15', '2021-01-20']
colors = ['red', 'blue', 'green']

# Basic usage
make_gantt_chart(tasks, start_dates, end_dates, colors=colors)

```




## Parameters

* `tasks (List[str])`: Labels for each task. Example: ['Task 1', 'Task 2']
* `start_dates (List[str])`: Start dates for each task. Example: ['2021-01-01', '2021-01-05']
* `end_dates (List[str])`: End dates for each task. Example: ['2021-01-10', '2021-01-15']
* `title (str, optional)`: Title of the graph. Defaults to 'Gantt Chart'. Example: 'Project Timeline'
* `xlabel (str, optional)`: Label for the x-axis. Defaults to 'Date'. Example: 'Timeline'
* `ylabel (str, optional)`: Label for the y-axis. Defaults to 'Tasks'. Example: 'Project Tasks'
* `colors (List[str], optional)`: Colors for each task. Defaults to None. Example: ['red', 'blue']
* `fontsize (int, optional)`: Font size for text elements. Defaults to 12. Example: 14
* `**kwargs`: Additional keyword arguments for matplotlib barh function.



#### We hope you found this documentation helpful! Your contributions, error identifications, and suggestions are highly valued as they help improve the quality of our documentation and the library itself. Please feel free to contribute by submitting pull requests, reporting issues, or providing feedback. Together, we can make this documentation more comprehensive and accurate for all users. Thank you for your support and happy coding!


