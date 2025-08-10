import asyncio
from checklist import checklist_data
from core.speech_engine import SpeechEngine
from fpdf import FPDF
import os
import datetime

class ChecklistAssistant:
    def __init__(self):
        self.engine = SpeechEngine()
        self.completed = {
            "sign_in": False,
            "time_out": False,
            "sign_out": False
        }
        self.log = []

    def log_item(self, section, item):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log.append(f"[{timestamp}] {section.upper()} - {item}")

    async def process_section(self, name, items):
        print(f"\n--- Starting {name.upper()} checklist ---\n")
        for item in items:
            await self.engine.speak(item)
            while True:
                user_input = self.engine.listen()
                if "confirm" in user_input:
                    self.log_item(name, item)
                    break
                await self.engine.speak("Please say confirm to continue")
        self.completed[name] = True
        await self.engine.speak(f"{name.replace('_', ' ').title()} checklist completed.")

    def save_log_to_pdf(self, filename="surgical_checklist_log.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Surgical Checklist Report", ln=True, align='C')
        pdf.ln(10)
        for entry in self.log:
            pdf.multi_cell(0, 10, txt=entry)
        pdf.output(filename)
        print(f"Checklist saved to {filename}")

    async def start(self):
        if not self.completed["sign_in"]:
            await self.process_section("sign_in", checklist_data.sign_in)
        if self.completed["sign_in"] and not self.completed["time_out"]:
            await self.process_section("time_out", checklist_data.time_out)
        if self.completed["time_out"] and not self.completed["sign_out"]:
            await self.process_section("sign_out", checklist_data.sign_out)

        await self.engine.speak("All surgical safety checklists are completed.")
        self.save_log_to_pdf() 
