from __future__ import annotations

from langchain_core.messages import SystemMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from prompt_library.prompt import SYSTEM_PROMPT
from tools.calculator_tool import (
    calculate,
    calculate_percentage,
    calculate_total_with_tax,
)
from tools.currency_conversion import convert_currency
from tools.place_search import search_places, get_place_details
from tools.weather_information import get_current_weather, get_weather_forecast
from utils.model_loader import ModelLoader
from models import UserPreferenceManager


class GraphBuilder:
    """
    Builds and compiles the LangGraph ReAct agent for the travel planner.

    Responsibilities (Single Responsibility Principle):
        - Register all available tools.
        - Bind tools to the LLM.
        - Construct and compile the StateGraph.

    Open/Closed: New tools can be added to `self.tools` without touching
    the graph wiring logic.  User preferences are injected dynamically
    via the UserPreferenceManager without modifying the base prompt.
    """

    def __init__(self, model_provider: str = "groq", user_id: int | None = None) -> None:
        self.tools: list = [
            get_current_weather,
            get_weather_forecast,
            convert_currency,
            calculate,
            calculate_percentage,
            calculate_total_with_tax,
            search_places,
            get_place_details,
        ]

        # ── Dynamic system prompt with user preferences ───────────────────
        base_content = SYSTEM_PROMPT.content
        if user_id is not None:
            pref_mgr = UserPreferenceManager()
            pref_block = pref_mgr.format_for_prompt(user_id)
            base_content = base_content + pref_block

        self.system_prompt = SystemMessage(content=base_content)

        loader = ModelLoader(model_provider=model_provider)
        llm = loader.load_llm()
        self.llm_with_tools = llm.bind_tools(self.tools)

    def _agent_node(self, state: MessagesState) -> dict:
        """
        Core ReAct agent node.

        Guards:
          1. Ensures the SYSTEM_PROMPT is always the first message — even if
             the state already carries a system message from a previous cycle.
          2. If any message content is an empty dict or falsy non-string value
             (e.g. a failed tool call returning {}), it is replaced with a
             descriptive error string so the LLM always receives useful context.
        """
        user_messages = state["messages"]

        # ── Guard 1: ensure SYSTEM_PROMPT leads the message list ──────────
        sanitized: list = []
        for msg in user_messages:
            if isinstance(msg, SystemMessage):
                continue  # drop any stale system messages from state
            sanitized.append(msg)

        input_messages = [self.system_prompt] + sanitized

        # ── Guard 2: replace empty / failed tool responses ────────────────
        cleaned_messages = []
        for msg in input_messages:
            content = getattr(msg, "content", None)
            if isinstance(content, dict) and not content:
                msg = msg.copy(update={
                    "content": "[Tool returned no data — information could not be retrieved. "
                               "Please proceed with available information.]"
                })
            elif content is None:
                msg = msg.copy(update={
                    "content": "[Tool returned no data — information could not be retrieved.]"
                })
            cleaned_messages.append(msg)

        response = self.llm_with_tools.invoke(cleaned_messages)
        return {"messages": [response]}

    def build_graph(self):
        """Assemble and compile the StateGraph."""
        graph_builder = StateGraph(MessagesState)

        graph_builder.add_node("agent", self._agent_node)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")

        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        """Allow the instance to be called as a factory: react_app = GraphBuilder()()"""
        return self.build_graph()