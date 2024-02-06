import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob

def plot_data(filenames):
    # Initialize a dictionary to store DataFrames by budget
    dfs_by_budget = {}

    # Loop through each filename
    for filename in filenames:
        # Read data into a pandas DataFrame
        df = pd.read_csv(filename)

        # Get the unique budget value
        budget = df['budget'].unique()[0]

        # If the budget is not in the dictionary, add it
        if budget not in dfs_by_budget:
            dfs_by_budget[budget] = []

        # Append the DataFrame to the list of DataFrames for this budget
        dfs_by_budget[budget].append(df)

    # Loop through each budget
    for budget, dfs in dfs_by_budget.items():
        # Concatenate all DataFrames in the list
        df_all = pd.concat(dfs, ignore_index=True)

        # Create a new figure
        plt.figure(figsize=(10, 6))

        # Create a horizontal bar plot
        ax = sns.barplot(x='score.mean', y='benchmark', hue='tool', data=df_all, errorbar=None, orient='h', palette='viridis')

        # Set x-axis limits
        ax.set_xlim(0, df_all['score.mean'].max() + 1)

        # Set x-axis label to "Average Score"
        ax.set_xlabel("Average Score")

        # Set the title to include the score and the budget
        ax.set_title(f"Score {budget} Seconds")

        # Add values at the end of the bars
        for p in ax.patches:
            width = p.get_width()
            plt.text(width, p.get_y() + p.get_height() / 2, '{:1.2f}'.format(width), ha = 'left', va = 'center')

        # Save the plot as a PNG file with a name that includes the budget
        plt.savefig(f"score_{budget}_seconds.png")

# Get a list of all 'score_per_subject.csv' files in the current directory and its subdirectories
csv_files = glob('**/score_per_subject.csv', recursive=True)

# Process all CSV files
plot_data(csv_files)