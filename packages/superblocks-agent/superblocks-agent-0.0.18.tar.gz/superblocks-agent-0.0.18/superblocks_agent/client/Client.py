from __future__ import annotations

import queue
from typing import Callable

import grpc
from grpc import ChannelConnectivity
from superblocks_types.api.v1.service_pb2 import StreamResponse

from superblocks_agent.client.Config import Config
from superblocks_agent.types._client import TwoWayStreamResponseHandler


def get_connection_monitor(client: Client) -> Callable[[grpc.ChannelConnectivity], None]:
    def connection_monitor(channel_connectivity: ChannelConnectivity):
        """
        Monitors the GRPC connection and reconnects when it shuts down.
        """
        match channel_connectivity:
            case ChannelConnectivity.SHUTDOWN:
                if client._expect_alive:
                    # the connection was shut down and we expect to be connected, attempt to reconnect
                    client._get_connection()

    return connection_monitor


class Client:
    """
    Used for connecting to the Superblocks Agent.
    """

    def __init__(self, config: Config):
        """
        Args:
            config (Optional[superblocks_agent.client.Config]): The Client configuration.
        """
        self.config = config
        self._channel = None
        self._connection_monitor_callable = get_connection_monitor(self)
        # expect_alive is used to monitor whether this client is expected to be connected or not
        # this is important to know whether we should try to reconnect or not
        self._expect_alive = False

    def close(self) -> None:
        """
        Closes the client.
        """
        self._expect_alive = False
        if self._channel is not None:
            self._channel.unsubscribe(self._connection_monitor_callable)
            self._channel.close()
            # set to None so next time this client is used, it is reset
            self._channel = None

    def __enter__(self):
        self._get_connection()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.close()
        # this check is needed in order to propagate errors
        return exception_type is None

    def _get_connection(self) -> grpc.Channel:
        """
        If a channel already exists, returns it.
        If a channel does not already exist, instanciates and returns the new channel.
        """
        self._expect_alive = True
        if self._channel is None:
            self._channel = grpc.insecure_channel(target=self.config.endpoint)
            self._channel.subscribe(self._connection_monitor_callable, try_to_connect=True)
        return self._channel

    async def _run(
        self,
        *,
        with_stub: object,
        stub_func_name: str,
        initial_request: object,
        response_handler: TwoWayStreamResponseHandler,
    ) -> list[StreamResponse]:
        # TODO: (joey) throw clear errors here for auth/connection issues
        # TODO: (joey) implement some reconnect logic
        stub = with_stub(channel=self._get_connection())
        stub_function = getattr(stub, stub_func_name)

        stream_responses = []
        q = queue.Queue()

        q.put(initial_request)

        def get_requests():
            while True:
                yield q.get()

        try:
            responses = stub_function(get_requests())

            for response in responses:
                next_request, two_way_response = response_handler(response)
                if two_way_response is not None:
                    stream_responses.append(two_way_response.stream)
                if next_request is not None:
                    q.put(next_request)
        except Exception as e:
            print("ERROR WHILE GETTING RESPONSES", e)
            raise e

        return stream_responses


__pdoc__ = {"StreamResponse": False}
