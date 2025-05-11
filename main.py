"""Main"""

from tools import EventTools as event_t, DatabaseTools as db_t

# Task Pipeline
from task.pipeline.trx.main import main as task_pipeline_trx
from task.pipeline.npp.main import main as task_pipeline_npp

# Task Views
from task.views.ticket_size.main import main as task_views_ticket_size

# Task Visualizations
from task.visualizations.ticket_size.main import main as task_viz_ticket_size

# Set, True= Enable viz; False: Disable viz
enable_visualization = True


def main():
    """Pipeline first then Views."""

    # Drop all Views
    db_t.drop_all_views()

    # Pipeline
    task_pipeline_trx()
    task_pipeline_npp()

    # Views Model
    task_views_ticket_size()

    # Visualization
    if enable_visualization:
        task_viz_ticket_size()


if __name__ == "__main__":
    event_t.show_msg("START")
    main()
    event_t.show_msg("DONE")
