import json
import pandas as pd
from plotly_calplot import calplot

DATE_TIME = "data/date_time.json"


def main():
    '''
    This main function reads time data from json, preprocesses it using pandas, and
    visualizes it using plotly_calplot
    '''
    with open(DATE_TIME, "r") as f:
        raw_data = json.load(f)

    dates, values = [], []
    for entry in raw_data:
        try:
            date = pd.to_datetime(entry["date"]).normalize()
            dates.append(date)
            values.append(int(entry["sec"]))
        except:
            continue
    df = pd.DataFrame({"ds": dates, "value": values})

    if not df.empty:
        years = df["ds"].dt.year.unique()
        full_dates = pd.DatetimeIndex([])
        for year in years:
            year_start = f"{year}-01-01"
            year_end = f"{year}-12-31"
            full_dates = full_dates.union(pd.date_range(year_start, year_end))
    else:
        full_dates = pd.date_range(pd.Timestamp.now().floor("D"), periods=1)

    df_full = pd.DataFrame({"ds": full_dates})

    # Fill missing values with 0
    df_full = df_full.merge(
        df.groupby("ds")["value"].sum().reset_index(),
        on="ds",
        how="left"
    ).fillna(0)

    df_full["value"] = df_full["value"].astype(int)

    # TODO: Replace the colorscale and month_lines_color with your preferred colors
    # Or turn off the dark_theme
    fig = calplot(
        df_full,
        x="ds",
        y="value",
        colorscale="Blues",
        showscale=False,
        gap=3,
        name="",
        years_title=True,
        month_lines_width=2,
        month_lines_color="purple",
        years_as_columns=True,
        dark_theme=True
    )

    fig.for_each_trace(
        lambda trace: trace.update(
            hovertemplate="<b>%{customdata}</b><br>%{z:.0f}s<extra></extra>",
            zmin=0,
            zmax=max(df_full["value"].max(), 1)
        ) if trace.type == "heatmap" else ()
    )

    num_years = len(df_full["ds"].dt.year.unique()) if not df.empty else 1
    fig.update_layout(
        title_text="Time Distribution",
        height=300 * num_years + 100,
        yaxis_autorange="reversed"
    )

    fig.show()


if __name__ == "__main__":
    main()
