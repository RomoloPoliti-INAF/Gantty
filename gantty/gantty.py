# Copyright (C) 2025  Romolo Politi
from datetime import datetime
import rich_click as click
from pathlib import Path
import pandas as pd
from rich import print
from rich_click import RichContext
from gantty.time_tools import string_to_timedelta, stopCal, day_length
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

__version__ = '1.0.0'

def buildCD(sessions):
    colors = ['#E64646', '#E69646', '#34D05C', '#34D0C3', '#3475D0']
    i = 0
    c_dict = {}
    for elem in sessions:
        c_dict[elem] = colors[i]
        i += 1
        if i == len(colors):
            i = 0
    return c_dict




def color(row, c_dict):
    return c_dict[row['Session']]

def build(ctx:RichContext,inputFile:Path, show:bool)->pd.DataFrame:
    df = pd.read_csv(inputFile)
    df.columns = [col.strip().title() for col in df.columns]
    df['Label'] = df['Label'].str.strip()
    df['Start_Values'] = pd.to_datetime(df['Start'].str.strip(), errors='coerce')
    df['End'] = None
    df['Start_Num']=0
    df['End_Num']=0
    for index, row in df.iterrows():
        if pd.notnull(row['Start_Values']):
            df.at[index, 'End'] = stopCal(row['Start_Values'], row['Durate'])
            # if index == 0:
            #     df.at[index, 'Start_Num'] = 0
            #     df.at[index, 'End_Num'] = day_length(row['Start_Values'], df.at[index, 'End'])
            # else:
            #     df.at[index, 'Start_Num'] = df.at[index-1, 'End_Num']
            #     df.at[index, 'End_Num'] = day_length(row['Start_Values'], df.at[index, 'End'])+df.at[index, 'Start_Num']
        else:
            parts = row['Start'].strip().split(' ')
            if parts[0] == 'after':
                matching_row = df[df['Label'] == parts[1]].iloc[0]
                if pd.notnull(matching_row['End']):
                    df.at[index, 'Start_Values'] = matching_row['End']
                    df.at[index, 'End'] = stopCal(df.at[index,'Start_Values'], row['Durate'])
                    # df.at[index, 'Start_Num'] = df.at[index-1, 'End_Num']
                    # df.at[index, 'End_Num'] = day_length(df.at[index, 'Start_Values'], df.at[index, 'End'])+df.at[index, 'Start_Num']
                pass
    df['End'] = pd.to_datetime(df['End'])
    proj_start = df.Start_Values.min()
    df['Start_Num'] = (df['Start_Values'] - proj_start).dt.days
    df['End_Num'] = (df['End'] - proj_start).dt.days
    df['Day_Start_2_End'] = df.End_Num - df.Start_Num
    sessions = df['Session'].unique()
    cdict = buildCD(sessions)
    df['color'] = df.apply(color, axis=1, c_dict=cdict)
    if show:
        orDF = pd.read_csv(inputFile)
        from rich.console import Console
        console=Console()
        console.print('Input Data:')
        console.print(orDF)
        console.print("Output Data:")
        console.print(df)
        ctx.exit()
    return df


def visualize(df:pd.DataFrame, title: str = 'Gantt PLOT', step: int = 1, outputFile: str = None, display: bool = False, no_sessions:bool=False):
    if display:
        dpi = 100
    else:
        dpi = 300
    if step < 1:
        step = 1
    fd = df[::-1]
    proj_start = df.Start_Values.min()
    fig, (ax, ax1) = plt.subplots(2, figsize=(20, 6), gridspec_kw={
        'height_ratios': [6, 1]}, facecolor='#36454F', dpi=dpi)

    ax.set_facecolor('#36454F')
    ax1.set_facecolor('#36454F')
    # bars
    ax.barh(df.Task, df.Day_Start_2_End,
            left=df.Start_Num, color=df.color, alpha=0.5, height=0.6)
    for idx, row in df.iterrows():
        ax.text(row.Start_Num + (row.Day_Start_2_End // 2), idx, row.Task,
                va='center', ha='center', alpha=0.8, color='w')
    sessions = df['Session'].unique()
    c_dict = buildCD(sessions)
    id = -0.6
    if not no_sessions:
        flag = False
        for session in sessions:
            filter = df[df['Session'] == session]
            if flag:
                ax.axhspan(id, id + len(filter), facecolor='#FFFFFF', alpha=0.2)
                flag = False
            else:
                flag = True
            id += len(filter)

    # grid lines
    ax.set_axisbelow(True)
    ax.xaxis.grid(color='k', linestyle='dashed', alpha=0.4, which='both')

    # ticks
    xticks_labels = pd.date_range(
        proj_start, end=df.End.max()).strftime("%d/%m/%y")
    xticks2 = [index for index, element in enumerate(
        xticks_labels) if element[0:2] == '01']
    ax.set_xticks(xticks2[::step])

    ax.set_xticklabels([element[3:] for index, element in enumerate(
        xticks_labels) if element[0:2] == '01'][::step], color='w')
    ax.set_yticks([])

    plt.setp([ax.get_xticklines()], color='w')

    # align x axis
    ax.set_xlim(0, df.End_Num.max())

    # remove spines
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('w')
    plt.suptitle(title, color='w')

    ##### LEGENDS #####
    legend_elements = []
    for session in sessions:
        legend_elements.append(Patch(facecolor=c_dict[session], label=session))

    legend = ax1.legend(handles=legend_elements,
                        loc='upper center', ncol=5, frameon=False)
    plt.setp(legend.get_texts(), color='w')

    # clean second axis
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.set_xticks([])
    ax1.set_yticks([])
    if display:
        plt.show()
    else:
        plt.savefig(outputFile, facecolor='#36454F')
        

def show_version(ctx, param, value):
    from rich.console import Console
    console = Console()
    if not value or ctx.resilient_parsing:
        return
    console.print(
        f"[bold]gantty[/] Version [cyan bold]{__version__}[/] \nCopyright (C) 2025  Romolo Politi")
    ctx.exit()


@click.command()
@click.option('-i', '--input', metavar='FILE', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
              help='The CSV input file. The default is gantt.csv', default=Path('./gantt.csv').expanduser())
@click.option('-o', '--output', metavar='FILE', type=click.Path(file_okay=True, dir_okay=False, writable=True),
              help='The PNG output file. The default is gantt.png', default=Path('./gantt.png').expanduser())
@click.option('-t', '--title', metavar='TITLE', help=' Title of the plot', default='Gantt Plot')
@click.option('-x', '--xticks', metavar='NUM', type=int, help='Set the x Thicks frequency to NUM. The default is every month (1)', default=1)
@click.option('-s', '--show', is_flag=True, help='Print the input data and the computed one and exit', default=False)
@click.option('-d', '--display', is_flag=True, help='Display the plot. No output will be saved', default=False)
@click.option('-n', '--no-sessions', is_flag=True, help='Do not use session colors', default=False)
@click.option('--version', is_flag=True, help='Print the version and exit', callback=show_version, is_eager=True)
@click.pass_context
def main(ctx,input: Path, output: Path, title: str, xticks: int, show: bool, display: bool,no_sessions:bool):
    df = build(ctx,input, show)
    visualize(df, title, outputFile=output,
              display=display, step=xticks,no_sessions=no_sessions)

if __name__ == "__main__":
    main()