"""Example invalid workflow."""
from dkist_processing_core import Workflow
from dkist_processing_core.tests.task_example import Task
from dkist_processing_core.tests.task_example import Task2


# |<--------------------|
# |-->Task -> Task2 --> |


example = Workflow(
    input_data="test-data",
    output_data="invalid",
    category="core",
    workflow_package=__package__,
)
example.add_node(task=Task, upstreams=Task2)
example.add_node(task=Task2, upstreams=Task)
