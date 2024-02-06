import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob

def plot_data(filename):
    # Read data into a pandas DataFrame
    df = pd.read_csv(filename)

    # Melt the DataFrame to have coverage types as a single column
    df_melt = pd.melt(df, id_vars=['benchmark', 'run'], value_vars=['linesCoverageRatio', 'conditionsCoverageRatio', 'mutantsCoverageRatio'])

    # Group the DataFrame by benchmark
    grouped = df_melt.groupby('benchmark')

    # Loop through each group
    for name, group in grouped:
        # Create a new figure for each group
        plt.figure(figsize=(10, 6))
        
        # Create a horizontal bar plot
        ax = sns.barplot(x='value', y='variable', hue='run', data=group, errorbar=None, orient='h')
        
        # Set x-axis limits
        ax.set_xlim(0, 100)
        
        # Get the tool name and time budget from the original DataFrame
        tool_name = df.loc[df['benchmark'] == name, 'tool'].iloc[0].upper()
        time_budget = df.loc[df['benchmark'] == name, 'timeBudget'].iloc[0]
        
        # Add percentage values at the end of the bars
        for p in ax.patches:
            width = p.get_width()
            plt.text(p.get_x() + width, p.get_y() + 0.55 * p.get_height(),
                     '{:1.2f}'.format(width),
                     ha='left', va='center')
        
        # Add a title
        plt.title(f'{tool_name} {name} {time_budget} Seconds')
        
        # Adjust the margins to make sure the labels fit within the figure
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(f'{tool_name}-{name}-{time_budget}Seconds.png')

    return df['timeBudget'].unique()[0]

# Find all .tmp files in the current directory
filenames = glob('**/results.tmp', recursive=True) 

# Initialize a dictionary to store files by timeBudget
files_by_timeBudget = {}

# Loop through each file
for filename in filenames:
    # Call the plot_data function with the current filename
    timeBudget = plot_data(filename)

    # If the timeBudget is not in the dictionary, add it
    if timeBudget not in files_by_timeBudget:
        files_by_timeBudget[timeBudget] = []

    # Add the filename to the list of files for this timeBudget
    files_by_timeBudget[timeBudget].append(filename)

# Loop through each timeBudget
for timeBudget, filenames in files_by_timeBudget.items():
    # Loop through each file for this timeBudget
    for filename in filenames:
        # Call the plot_data function with the current filename
        plot_data(filename)