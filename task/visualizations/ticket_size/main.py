from tools import EventTools as event_t, DatabaseTools as db_t

# Packages
import plotly.graph_objects as go
import pandas as pd


def main():
    Visualization().do()


class Visualization:

    def do(self):

        df = self.get_data()

        # Create a plotly figure
        fig = go.Figure()

        # Add line chart
        fig.add_trace(
            go.Scatter(
                x=df["period"],
                y=df["ticket_size"],
                mode="lines+markers",
                name="Avg Ticket Size",
                line={
                    "width": 3,
                    "color": "chartreuse",
                },
                marker=dict(
                    color="coral",
                    size=10,
                    line=dict(
                        width=2,
                    ),
                ),
            )
        )
        # Update background
        fig.update_layout(
            title="Average Disbursement Amount per Account",
            xaxis_title="Period",
            yaxis_title="Average Ticket Size",
            template="plotly_dark",
            margin=dict(l=50, r=50, t=50, b=250),
        )

        # Add statistic description.
        first_ticket_size = df["ticket_size"].iloc[0]
        last_ticket_size = df["ticket_size"].iloc[-1]
        total_growth = last_ticket_size - first_ticket_size
        percent_growth = (total_growth / df["ticket_size"].iloc[0]) * 100
        # fmt: off
        fig.add_annotation(
            text=f"Total Growth Since Beginning: Rp {total_growth:,.0f}<br>"
                 f"Percent Growth Since Beginning: {percent_growth:.2f}%<br><br>"
                 f"There was an {percent_growth:.2f}% increase in ticket size from {df['period'].min()} to {df['period'].max()}, "
                 f"from Rp {first_ticket_size:,.0f} to Rp {last_ticket_size:,.0f}.",
            align="left",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(color="white", size=15),
            bgcolor="rgba(0,0,0,0)",
            y=-0.25,
            x=0,
            xanchor="left",
        )
        # fmt: on

        # Show viz
        fig.show()

    @classmethod
    def get_data(cls):
        q = """
            SELECT
              *
            FROM
              ticket_size a
            ORDER BY
              a."period"
        """
        return db_t.extract_from_database(q)


if __name__ == "__main__":
    main()
