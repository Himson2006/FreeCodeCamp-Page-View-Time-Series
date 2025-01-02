import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('/workspace/boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv',
    parse_dates = ['date'],
    index_col = ['date']
)

# Clean data
df = df[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize = (20,6))
    
    plt.plot(df.index, df['value'],color = 'red')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df['Months'] = df.index.month
    df['Years'] = df.index.year
    df_bar = df.groupby(['Years', 'Months'], as_index = False )['value'].mean()
    df_bar.replace([1,2,3,4,5,6,7,8,9,10,11,12], ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], inplace = True)
    df_bar.rename(columns={"value": "Average Page Views"}, inplace = True)

    # Draw bar plot
    fig, ax = plt.subplots(figsize = (16, 6))

    fig = sns.catplot(data = df_bar, x = 'Years', y ='Average Page Views', hue = 'Months', kind = 'bar', edgecolor = 'black',
    linewidth = 0.5, palette= ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b",
    "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#f45b69", "#4caf50"], legend_out = False,
    hue_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box.rename(columns = {'year' : 'Year', 'month' : 'Month', 'value' : 'Page Views'}, inplace = True)

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2 , figsize = (16, 6))

    # The first boxplot in terms of years
    sns.boxplot(data = df_box, x = 'Year', y = 'Page Views', ax = ax[0],
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
    flierprops = {
        'marker' : 'd',
        'markerfacecolor' : 'black', 
        'markersize' : 3,
    })
    ax[0].set_title('Year-wise Box Plot (Trend)')

    #The second box plot in terms of month
    sns.boxplot(data = df_box, x = 'Month', y = "Page Views", ax = ax[1],
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b",
    "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#f45b69", "#4caf50"],
    order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    flierprops = {
        'marker' : 'd',
        'markerfacecolor' : 'black', 
        'markersize' : 3,
    })
    ax[1].set_title('Month-wise Box Plot (Seasonality)')



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
