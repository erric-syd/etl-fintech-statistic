from tools import EventTools as event_t, DatabaseTools as db_t

# Packages
import plotly.graph_objects as go
import pandas as pd
from nicegui import ui


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
        fig.update_layout(
            title="Average Disbursement Amount per Account",
            xaxis_title="Period",
            yaxis_title="Average Ticket Size",
            template="plotly_dark",
            margin=dict(l=50, r=50, t=50, b=50),
        )

        # fig.show()

        # Create NiceGUI dashboard
        ui.plotly(fig).classes("w-full h-[750px]")  # Custom 75% height using square brackets
        # ui.plotly(fig).classes("w-full h-screen")  # Full viewport height

        # Add a card with summary stats
        with ui.card().classes("w-full"):
            first_ticket_size = df["ticket_size"].iloc[0]
            last_ticket_size = df["ticket_size"].iloc[-1]
            total_growth = last_ticket_size - first_ticket_size
            percent_growth = (total_growth / df["ticket_size"].iloc[0]) * 100

            ui.label(f"Total Growth Since Beginning: Rp {total_growth:,.0f}").classes("text-lg")
            ui.label(f"Percent Growth Since Beginning: {percent_growth:.2f}%").classes("text-lg")
            ui.label(
                f"There was an {percent_growth:.2f}% increase in ticket size "
                f"from {df['period'].min()} to {df['period'].max()}, reflecting a growth in "
                f"the average loan amount disbursed per account, "
                f"from Rp {first_ticket_size:,.0f} to Rp {last_ticket_size:,.0f}."
            ).classes("text-lg")

        ui.run(port=8080, reload=False)

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
