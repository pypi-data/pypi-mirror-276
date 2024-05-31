#import nest_asyncio
from .Request import Request
from .Agent import AgentFactory
from .Facility import FacilityManager
from .WebSocket import WebSocketServer, WebSocketClient
from .Workflow import Workflow, Schema as WorkflowSchema
from ._global import global_plugin_manager, global_settings, global_storage, global_tool_manager, global_websocket_server
from .utils import *

#nest_asyncio.apply()

def create_agent(*args, **kwargs):
    return AgentFactory().create_agent(*args, **kwargs)

facility = FacilityManager()
lib = facility

set_settings = global_settings.set