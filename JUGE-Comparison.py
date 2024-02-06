import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import re

def plot_data(filenames):
    # Initialize a dictionary to store DataFrames by timeBudget
    dfs_by_timeBudget = {}

    # Loop through each filename
    for filename in filenames:
        # Read data a pandas DataFrame
        df = pd.read_csv(filename)

        # Convert coverage ratio columns to numeric
        for column in ['linesCoverageRatio', 'conditionsCoverageRatio', 'mutantsCoverageRatio']:
            df[column] = pd.to_numeric(df[column], errors='coerce') / 100.0

        # Get the unique timeBudget value
        timeBudget = df['timeBudget'].unique()[0]

        # If the timeBudget is not in the dictionary, add it
        if timeBudget not in dfs_by_timeBudget:
            dfs_by_timeBudget[timeBudget] = []

        # Append the DataFrame to the list of DataFrames for this timeBudget
        dfs_by_timeBudget[timeBudget].append(df)

    # Loop through each timeBudget
    for timeBudget, dfs in dfs_by_timeBudget.items():
        # Concatenate all DataFrames in the list
        df_all = pd.concat(dfs, ignore_index=True)

        # Group by benchmark, tool, and time budget and calculate the average of each coverage ratio
        df_grouped = df_all.groupby(['benchmark', 'tool', 'timeBudget']).agg({'linesCoverageRatio': 'mean', 'conditionsCoverageRatio': 'mean', 'mutantsCoverageRatio': 'mean'})

        # Reset the index
        df_grouped = df_grouped.reset_index()

        # Melt the DataFrame to make it suitable for seaborn
        df_melted = df_grouped.melt(id_vars=['benchmark', 'tool', 'timeBudget'], var_name='coverageType', value_name='averageCoverageRatio')

        # Create a separate catplot for each coverage ratio
        for coverage_type in ['linesCoverageRatio', 'conditionsCoverageRatio', 'mutantsCoverageRatio']:
            # Filter the DataFrame for the current coverage ratio
            df_filtered = df_melted[df_melted['coverageType'] == coverage_type]

            # Create a catplot with horizontal bars
            g = sns.catplot(y='benchmark', x='averageCoverageRatio', hue='tool', data=df_filtered, kind='bar', errorbar=None, palette='magma', orient='h')

            # Set x-axis label to "Average Coverage Ratio" and y-axis label to "Benchmark"
            g.set_axis_labels("Average Coverage Ratio", "Benchmark")

            # Set the title to "Average Coverage Ratios by Benchmark and Time Budget"
            g.fig.suptitle(f"{coverage_type} {df_filtered['timeBudget'].unique()[0]} Seconds", y=1.02)

            # Loop through each Axes in the FacetGrid and add text at the end of each bar
            for ax in g.axes.flat:
                for bar in ax.patches:
                    ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', ha='left', va='center')

            # Save the plot as a PNG file
            g.savefig(f"{coverage_type}_{df_filtered['timeBudget'].unique()[0]}.png")

# Get a list of all 'results.tmp' files in the current directory and its subdirectories
tmp_files = glob('**/results.tmp', recursive=True)

# Process all .tmp files
plot_data(tmp_files)