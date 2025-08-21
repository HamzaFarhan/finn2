from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dreamai.agent import AgentDeps
from pydantic_ai import ModelRetry, RunContext
from pydantic_ai.tools import Tool, ToolFuncEither
from pydantic_ai.toolsets import FunctionToolset, ToolsetTool
from pydantic_ai.toolsets.function import FunctionToolsetTool


@dataclass(init=False)
class DataDirs:
    thread_dir: Path
    workspace_dir: Path
    analysis_dir: Path
    results_dir: Path
    data_dir: Path
    message_history_path: Path

    def __init__(self, thread_dir: Path, workspace_dir: Path):
        self.thread_dir = thread_dir.expanduser().resolve()
        self.workspace_dir = workspace_dir
        self.results_dir = self.thread_dir / "results"
        self.data_dir = self.workspace_dir / "data"
        self.message_history_path = self.thread_dir / "message_history.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)


class FinnDeps(AgentDeps):
    dirs: DataDirs


class FinnToolset(FunctionToolset[AgentDeps]):
    def __init__(
        self,
        tools: Sequence[Tool[AgentDeps] | ToolFuncEither[AgentDeps, ...]] = [],
        max_retries: int = 1,
        *,
        id: str | None = None,
        file_path_resolver: Callable[[RunContext[AgentDeps], str | Path], str | Path],
    ):
        super().__init__(tools=tools, max_retries=max_retries, id=id)
        self.file_path_resolver = file_path_resolver

    async def call_tool(
        self, name: str, tool_args: dict[str, Any], ctx: RunContext[AgentDeps], tool: ToolsetTool[AgentDeps]
    ) -> Any:
        assert isinstance(tool, FunctionToolsetTool)
        try:
            for arg in tool_args:
                if "path" in arg:
                    tool_args[arg] = str(self.file_path_resolver(ctx, tool_args[arg]))
            return await tool.call_func(tool_args, ctx)
        except Exception as e:
            raise ModelRetry(f"Error calling tool {name}: {e}")
