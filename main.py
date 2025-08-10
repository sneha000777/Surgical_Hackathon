# main.py
import asyncio
from core.assistant import ChecklistAssistant

if __name__ == "__main__":
    assistant = ChecklistAssistant()
    asyncio.run(assistant.start())
