from pathlib import Path

from dotenv import load_dotenv
from dreamai.plan_act import run_plan_and_act_agent
from loguru import logger
from pydantic_ai.toolsets import FunctionToolset

from finn2.finn_deps import DataDirs, FinnDeps
from finn2.toolsets.file_toolset import describe_df
from finn2.toolsets.math_tools import calculate_sum

load_dotenv()

if __name__ == "__main__":
    import asyncio

    workspace_dir = Path("./workspaces/session/")
    agent_deps = FinnDeps(
        dirs=DataDirs(
            workspace_dir=workspace_dir,
            thread_dir=workspace_dir / "threads/1",
        ),
        toolsets=[FunctionToolset([calculate_sum, describe_df])],
    )
    asyncio.run(run_plan_and_act_agent("what is the total profit in orders.csv?", agent_deps=agent_deps))
    logger.success("Agent run completed successfully.")
