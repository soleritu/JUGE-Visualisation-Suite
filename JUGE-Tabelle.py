import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

def create_table(filename):
    df = pd.read_csv(filename)
    if 'score' in df.columns:  # This is a CSV file
        df = df[['benchmark', 'run', 'tool', 'timeBudget', 'score']]
    else:  # This is a tmp file
        df = df[['benchmark', 'run', 'tool', 'timeBudget', 'linesCoverageRatio', 'conditionsCoverageRatio', 'mutantsCoverageRatio']]
        for column in ['linesCoverageRatio', 'conditionsCoverageRatio', 'mutantsCoverageRatio']:
            df[column] = pd.to_numeric(df[column], errors='coerce')
    return df, df['timeBudget'].unique()[0]

csv_filenames = glob('**/detailed_score.csv', recursive=True)
tmp_filenames = glob('**/results.tmp', recursive=True)

csv_tables = {}
tmp_tables = {}

for filename in csv_filenames:
    df, timeBudget = create_table(filename)
    if timeBudget not in csv_tables:
        csv_tables[timeBudget] = []
    csv_tables[timeBudget].append(df)

for filename in tmp_filenames:
    df, timeBudget = create_table(filename)
    if timeBudget not in tmp_tables:
        tmp_tables[timeBudget] = []
    tmp_tables[timeBudget].append(df)

for timeBudget in set(list(csv_tables.keys()) + list(tmp_tables.keys())):
    df_csv = pd.concat(csv_tables.get(timeBudget, []), ignore_index=True)
    df_tmp = pd.concat(tmp_tables.get(timeBudget, []), ignore_index=True)

    # Merge the two DataFrames on 'benchmark', 'run', 'tool', and 'timeBudget'
    df_all = pd.merge(df_tmp, df_csv, on=['benchmark', 'run', 'tool', 'timeBudget'], how='outer')

    # Sort the DataFrame by 'run' and 'benchmark'
    df_all = df_all.sort_values(by=['run', 'benchmark'])

    # Create a new figure with larger size
    fig, ax = plt.subplots(figsize=(20, 10)) # adjust the size as needed

    # Remove the plot frame
    ax.axis('off')

    # Create the table and adjust the font size
    table = plt.table(cellText=df_all.values, colLabels=df_all.columns, cellLoc = 'center', loc='center')

    # Auto-adjust the columns widths
    table.auto_set_column_width(col=list(range(len(df_all.columns))))

    # Save the figure with a filename that includes the timeBudget
    plt.savefig(f'comparison-tabelle_{timeBudget}.png', bbox_inches='tight')