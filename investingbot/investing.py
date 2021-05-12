"""
Main Logic of module.

Save photo with investing curve
"""

from datetime import datetime
from typing import List, Tuple

from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter


def millions(number: int, pos: float) -> str:
    """
    Convert numbers to millions for matplotlib figure.

    Args:
        number (int): number for converting
        pos (float): position for matplotlib figure

    Returns:
        str: millions
    """
    millionth_share = 1e-6
    return '${0:1.1f}M'.format(number * millionth_share)


def thousands(number: int, pos: float) -> str:
    """
    Convert numbers to thousands for matplotlib figure.

    Args:
        number (int): number for converting
        pos (float): position for matplotlib figure

    Returns:
        str: thousands
    """
    thousandth_share = 1e-3
    return '${0:1.1f}K'.format(number * thousandth_share)


def count_investing(
    month_investing: int = 100000,
    count_years: int = 10,
    perc_return: float = 10.0,
    seed_money: int = 50000,
) -> Tuple[int, List[int], List[datetime]]:
    """
    Count investing by date.

    Args:
        month_investing (int): monthly investing. Defaults to 100000.
        count_years (int): count of years. Defaults to 10.
        perc_return (float): percentage return. Defaults to 10.0.
        seed_money (int): seed money for initial savings. Defaults to 50000.

    Returns:
        Tuple[int, List[datetime], List[int]]: investing and two lists
    """
    count_month_in_years = 12
    count_month = count_month_in_years * count_years
    current_month = datetime.today()
    investing = seed_money
    months = 0
    dates = []
    total_investing = []
    monthly_percentage_share = 0.01 / 12
    perc_return *= monthly_percentage_share
    print(perc_return)
    for _ in range(0, count_month):
        if _ != 0:
            investing = int(investing + (investing * perc_return))
            investing += month_investing
        dates.append(current_month + relativedelta(months=months))
        total_investing.append(investing)
        months += 1
    return investing, total_investing, dates


def draw_investing(
    chat_id: str, investing: int, count_years: int, perc_return: float, seed_money: int
) -> str:
    """
    Draw investing curve.

    Args:
        chat_id (str): user's chad_id
        investing (int): total sum of investing
        count_years (int): count of years
        perc_return (float): percentage return
        seed_money (int): initial investing

    Returns:
        str: main message for user with total investing
    """
    (investing, total_investing, dates) = count_investing(
        investing, count_years, perc_return, seed_money
    )
    million = 1000000
    thousand = 1000
    dpi = 150
    if investing < million:
        total = 'TOTAL INVESTING: {0}K'.format(round(investing / thousand, 2))
        formatter = FuncFormatter(thousands)
    else:
        total = 'TOTAL INVESTING: {0}M'.format(round(investing / million, 2))
        formatter = FuncFormatter(millions)

    fontsize = 20
    grid = True
    fig, ax = plt.subplots(figsize=(15, 15))
    plt.grid(grid, color='grey', linestyle='-', linewidth=0.5)
    plt.style.use('dark_background')
    plt.rcParams.update({'font.size': 12})
    plt.title(
        str(count_years) + ' YEARS, ' + str(perc_return) + ' ANNUAL PERCENT, ' + total,
        fontsize=fontsize,
    )
    plt.xlabel('DATE', fontsize=fontsize)
    plt.ylabel('INVESTING', fontsize=fontsize)
    plt.xlim(min(dates), max(dates))
    print(total_investing)
    plt.ylim(min(total_investing), max(total_investing))
    plt.plot(dates, total_investing)
    plt.fill_between(dates, total_investing)
    ax.yaxis.set_major_formatter(formatter)
    plt.savefig('{0}.png'.format(chat_id), dpi=dpi)
    return total
