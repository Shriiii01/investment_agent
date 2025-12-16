#!/usr/bin/env python3
"""
Main entry point for running the Investment Agent application.
This script provides an alternative way to run the Streamlit app.
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    agent_script = os.path.join(script_dir, "agent.py")
    
    if not os.path.exists(agent_script):
        print(f"Error: {agent_script} not found!")
        sys.exit(1)
    
    print("🚀 Starting Investment Agent...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", agent_script])

if __name__ == "__main__":
    main()

