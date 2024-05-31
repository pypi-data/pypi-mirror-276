import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mpl_dates

def plot_scatter_with_one_to_one_line(dataframe, column1, column2):
    plt.figure(figsize=(10, 7))
    plt.scatter(dataframe[column1], dataframe[column2], alpha=0.5, label='Data Points')
    min_val = min(dataframe[column1].min(), dataframe[column2].min())
    max_val = max(dataframe[column1].max(), dataframe[column2].max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='1:1 Line')
    plt.xlabel(column1)
    plt.ylabel(column2)
    plt.title(f'Scatter Plot with 1:1 Line: {column1} vs. {column2}')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_line_graph(dataframe, x_column, y_columns, labels):
    sns.set_theme()
    plt.figure(figsize=(10, 7))
    for y_col, label in zip(y_columns, labels):
        sns.lineplot(x=x_column, y=y_col, data=dataframe, label=label)
    plt.gcf().autofmt_xdate()
    date_format = mpl_dates.DateFormatter('%b %d, %y')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.title(f'{", ".join(labels)} vs Date')
    plt.xlabel('Date')
    plt.ylabel(f'{", ".join(labels)} Values')
    plt.legend()
    plt.show()
