from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from superblocks_agent._constant import DEFAULT_AGENT_ENDPOINT
from superblocks_agent._util.doc import modify_pdoc
from superblocks_agent.api.ViewMode import ViewMode


@dataclass(kw_only=True)
class Config:
    """
    Configuration for the client.

    Args:
        endpoint: (str): The endpoint of the execution engine. Defaults to `'agent.superblocks.com:8443'`
        token: (str): The agent auth token.
        branch_name (Optional[str]): The default branch to use. Defaults to `None`.
        commit_id (Optional[str]): The ID of the commit to use. Defaults to `None`.
        profile (Optional[str]): The default profile to use. If not set, the default for view_mode will be used. Defaults to `None`.
        view_mode (Optional[superblocks_agent.api.ViewMode]): The default view mode. Defaults to `None`.
    """

    endpoint: str = DEFAULT_AGENT_ENDPOINT
    token: str
    branch_name: Optional[str] = None
    commit_id: Optional[str] = None
    profile: Optional[str] = None
    view_mode: Optional[ViewMode] = None


__pdoc__ = modify_pdoc(dataclass=Config)
