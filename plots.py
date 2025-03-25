import plotly.express as px

def plot_prices(df):
    return px.line(
        df,
        x="Date",
        y="Close",     
        color="Ticker",
        title="Comparative Closing Prices"
)


def plot_market_cap(df):
    return px.line(
        df,
        x="Date",
        y="Estimated Market Cap",
        color="Ticker",
        title="Estimated Market Cap Growth Over Time",
        labels={"Estimated Market Cap": "Estimated Market Cap (USD)"}
    )
