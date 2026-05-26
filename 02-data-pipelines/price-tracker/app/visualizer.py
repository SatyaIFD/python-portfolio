import plotly.express as px

def generate_report(df):
    """
    Generate an interactive HTML dashboard to visualize
    time-series product price trends.

    Args:
        df (DataFrame): A pandas DataFrame containing:
                        - 'timestamp' column for time records
                        - 'price' column for product prices
                        - 'title' column for product names

    Returns:
        None
    """

    # Check whether the dataset is empty
    if df.empty:

        # Display warning if no data is available
        print("[WARNING] Analytics matrix empty. Visual generation skipped.")
        return

    # Display processing message
    print("[INFO] Formatting time-series metrics into structural plot lines...")

    # Sort records by timestamp to ensure proper line progression
    df = df.sort_values(by="timestamp")

    # -----------------------------------------
    # Create interactive line chart
    # -----------------------------------------
    fig = px.line(
        df,

        # X-axis: timestamp of recorded prices
        x="timestamp",

        # Y-axis: product price values
        y="price",

        # Separate colored line for each product
        color="title",

        # Use straight line connections
        line_shape="linear",

        # Dashboard title
        title="Automated Tracker Dashboard: Live E-Commerce Asset Variance",

        # Rename axis labels for readability
        labels={
            "timestamp": "Recording Timestamp",
            "price": "Normalized Price ($ USD)"
        },

        # Apply dark theme styling
        template="plotly_dark"
    )

    # -----------------------------------------
    # Enhance chart appearance
    # -----------------------------------------

    # Add markers to line points for better visibility
    fig.update_traces(
        mode="lines+markers",
        marker=dict(size=6)
    )

    # Enable unified hover tooltip mode
    fig.update_layout(hovermode="x unified")

    # Define output HTML report file
    output_file = "price_report.html"

    # Save chart as standalone interactive HTML file
    fig.write_html(output_file)

    # Display success confirmation message
    print(
        f"[SUCCESS] Interactive market trend asset rendered to: "
        f"'{output_file}'"
    )