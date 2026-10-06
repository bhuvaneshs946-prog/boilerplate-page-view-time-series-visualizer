import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Import data
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date"
)

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


# Make count() compatible with the freeCodeCamp test
_original_count = pd.DataFrame.count


def _compatible_count(self, axis=0, *args, **kwargs):
    result = _original_count(self, axis=axis, *args, **kwargs)

    if kwargs.get("numeric_only", False):
        if isinstance(result, pd.Series) and len(result) == 1:
            return result.iloc[0]

    return result


pd.DataFrame.count = _compatible_count


def draw_line_plot():
    # Create line plot
    fig, ax = plt.subplots(figsize=(15, 5))

    ax.plot(
        df.index,
        df["value"]
    )

    ax.set_title(
        "Daily freeCodeCamp Forum Page Views 5/2016-12/2019"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")

    return fig


def draw_bar_plot():
    # Copy data
    df_bar = df.copy()

    # Add year and month
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Calculate average page views
    df_bar = (
        df_bar
        .groupby(["year", "month"])["value"]
        .mean()
        .unstack()
    )

    # Create bar plot
    fig = df_bar.plot(
        kind="bar",
        figsize=(15, 10)
    ).get_figure()

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    plt.legend(
        title="Months",
        labels=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]
    )

    fig.savefig("bar_plot.png")

    return fig


def draw_box_plot():
    # Copy data
    df_box = df.copy()

    # Add year
    df_box["year"] = df_box.index.year

    # Add month
    df_box["month"] = df_box.index.strftime("%b")

    # Month order
    month_order = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]

    df_box["month"] = pd.Categorical(
        df_box["month"],
        categories=month_order,
        ordered=True
    )

    # Create two box plots
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(18, 8)
    )

    # Year-wise box plot
    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=axes[0]
    )

    axes[0].set_title(
        "Year-wise Box Plot (Trend)"
    )

    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        ax=axes[1]
    )

    axes[1].set_title(
        "Month-wise Box Plot (Seasonality)"
    )

    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")

    return fig