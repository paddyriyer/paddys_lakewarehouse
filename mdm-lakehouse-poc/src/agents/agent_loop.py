"""
Core Claude Opus 4.6 Agentic Loop
==================================
This is the central pattern that powers all 6 AI agents.

Architecture:
  1. User provides high-level task
  2. Claude reasons about which tools to use
  3. Claude returns tool_use response
  4. Python handler executes the tool (AWS SDK, SQL, file I/O)
  5. Result fed back to Claude as tool_result
  6. Loop repeats until Claude signals end_turn

This pattern replaces traditional ETL development with autonomous
code generation — Claude writes production PySpark, dbt, Airflow,
and Great Expectations code by calling real enterprise data tools.
"""

import anthropic
import json
import logging
from typing import Optional

from tool_definitions import ENTERPRISE_DATA_TOOLS
from tool_handlers import TOOL_HANDLERS

logger = logging.getLogger(__name__)

# Initialize Anthropic client (uses ANTHROPIC_API_KEY env var)
client = anthropic.Anthropic()


def run_agent(
    system_prompt: str,
    task: str,
    tools: Optional[list] = None,
    model: str = "claude-opus-4-6",
    max_tokens: int = 8192,
    max_iterations: int = 25,
) -> str:
    """
    Core agentic loop. Claude decides which tools to call,
    we execute them, feed results back, repeat until done.

    Args:
        system_prompt: Domain-specific instructions for the agent
        task: The user's high-level task description
        tools: List of tool definitions (defaults to ENTERPRISE_DATA_TOOLS)
        model: Claude model to use
        max_tokens: Maximum tokens per API call
        max_iterations: Safety limit on tool-use cycles

    Returns:
        Final text response from Claude after all tool use is complete
    """
    if tools is None:
        tools = ENTERPRISE_DATA_TOOLS

    messages = [{"role": "user", "content": task}]

    for iteration in range(max_iterations):
        logger.info(f"Agent iteration {iteration + 1}/{max_iterations}")

        # ── Call Claude API ──
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            tools=tools,
            messages=messages,
        )

        # ── Check: is Claude done? ──
        if response.stop_reason == "end_turn":
            final_texts = [b.text for b in response.content if b.type == "text"]
            result = "\n".join(final_texts)
            logger.info(f"Agent completed after {iteration + 1} iterations")
            return result

        # ── Claude wants to use tools ──
        if response.stop_reason == "tool_use":
            # Add Claude's response to conversation history
            messages.append({"role": "assistant", "content": response.content})

            # Execute each tool call
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input

                    logger.info(f"  Tool call: {tool_name}({json.dumps(tool_input)[:100]}...)")

                    handler = TOOL_HANDLERS.get(tool_name)
                    if handler:
                        try:
                            result = handler(**tool_input)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps(result),
                            })
                            logger.info(f"  Tool result: success ({len(json.dumps(result))} chars)")
                        except Exception as e:
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": f"ERROR: {str(e)}",
                                "is_error": True,
                            })
                            logger.error(f"  Tool error: {e}")
                    else:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"ERROR: Unknown tool '{tool_name}'",
                            "is_error": True,
                        })

            # Feed results back to Claude
            messages.append({"role": "user", "content": tool_results})

    logger.warning("Max iterations reached")
    return "Max iterations reached — agent did not complete"
