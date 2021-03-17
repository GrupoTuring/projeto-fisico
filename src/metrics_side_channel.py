from mlagents_envs.side_channel.side_channel import SideChannel, OutgoingMessage
import uuid
from collections import defaultdict
import ray


class MetricsSideChannel(SideChannel):

    def __init__(self) -> None:
        super().__init__(uuid.UUID("7a9acce6-3f8f-47cd-adf5-a45956fdbd71"))

    def on_message_received(self, msg) -> None:
        name = msg.read_string()
        value = msg.read_float32()
        tracker = ray.get_actor('agent_metric_tracker')
        tracker.add_metric.remote(name, value)
