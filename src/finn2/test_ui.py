import os
from pathlib import Path

from dotenv import load_dotenv

from finn2.gradio_ui import launch_finn_ui

load_dotenv()

if __name__ == "__main__":
    # Create a test workspace
    test_workspace = Path(os.getenv("WORKSPACES_DIR", ".")) / "test_workspace"
    test_workspace.mkdir(parents=True, exist_ok=True)

    print("🚀 Launching Finn UI...")
    print("📁 Workspace:", test_workspace.absolute())
    try:
        launch_finn_ui(
            workspace_dir=test_workspace,
            share=False,
            server_name=os.getenv("SERVER_NAME", "0.0.0.0"),
            server_port=os.getenv("SERVER_PORT", 7860),
            show_error=True,
        )
    except KeyboardInterrupt:
        print("\n👋 Finn UI stopped.")
    except Exception as e:
        print(f"\n❌ Error launching UI: {e}")
