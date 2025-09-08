from pydantic import BaseModel
from typing import List, Optional
from agents import Agent, Runner
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()

class Person(BaseModel):
   name: str
   role: Optional[str]
   contact: Optional[str]

class Meeting(BaseModel):
   date: str
   time: str
   location: Optional[str]
   duration: Optional[str]

class Task(BaseModel):
   description: str
   assignee: Optional[str]
   deadline: Optional[str]
   priority: Optional[str]

class EmailData(BaseModel):
   subject: str
   sender: Person
   recipients: List[Person]
   main_points: List[str]
   meetings: List[Meeting]
   tasks: List[Task]
   next_steps: Optional[str]

email_extractor = Agent(
   name="Email Extractor",
   instructions="""You are an assistant that extracts structured information from emails.
  
   When given an email, carefully identify:
   - Subject and main points
   - People mentioned (names, roles, contact info)
   - Meetings (dates, times, locations)
   - Tasks or action items (with assignees and deadlines)
   - Next steps or follow-ups
  
   Extract this information as structured data. If something is unclear or not mentioned,
   leave those fields empty rather than making assumptions.
   """,
   output_type=EmailData,  # This tells the agent to return data in EmailData format
)

sample_email = """From: Alex Johnson <alex.j@techcorp.com>
To: Team Development <team-dev@techcorp.com>
CC: Sarah Wong <sarah.w@techcorp.com>, Miguel Fernandez <miguel.f@techcorp.com>
Subject: Project Phoenix Update and Next Steps

Hi team,

I wanted to follow up on yesterday's discussion about Project Phoenix and outline our next steps.

Key points from our discussion:
- The beta testing phase has shown promising results with 85% positive feedback
- We're still facing some performance issues on mobile devices
- The client has requested additional features for the dashboard

Let's schedule a follow-up meeting this Friday, June 15th at 2:00 PM in Conference Room B. The meeting should last about 1.5 hours, and we'll need to prepare the updated project timeline.

Action items:
1. Sarah to address the mobile performance issues by June 20th (High priority)
2. Miguel to create mock-ups for the new dashboard features by next Monday
3. Everyone to review the beta testing feedback document and add comments by EOD tomorrow

If you have any questions before Friday's meeting, feel free to reach out.

Best regards,
Alex Johnson
Senior Project Manager
(555) 123-4567"""

async def process_email(email_text):
   runner = Runner()
   result = await runner.run(
       email_extractor,
       f"Please extract information from this email:\n\n{email_text}"
   )

   return result

async def main():
   result = await process_email(sample_email)
   extracted_data = result.final_output
   
   # Print the raw structured data
   print("=== RAW STRUCTURED DATA ===")
   print(extracted_data.model_dump_json(indent=2))
   print("\n=== ACCESSING SPECIFIC FIELDS ===")
   
   # Accessing top-level fields
   print(f"Email Subject: {extracted_data.subject}")
   
   # Accessing nested objects
   print(f"\nSender Information:")
   print(f"  Name: {extracted_data.sender.name}")
   print(f"  Role: {extracted_data.sender.role}")
   print(f"  Contact: {extracted_data.sender.contact}")
   
   # Accessing lists of objects
   print(f"\nRecipients:")
   for i, recipient in enumerate(extracted_data.recipients, 1):
       print(f"  Recipient {i}: {recipient.name} ({recipient.role or 'No role specified'})")
   
   # Accessing nested lists
   print(f"\nTasks with details:")
   for i, task in enumerate(extracted_data.tasks, 1):
       print(f"  Task {i}: {task.description}")
       print(f"    Assignee: {task.assignee}")
       print(f"    Deadline: {task.deadline}")
       print(f"    Priority: {task.priority}")
   
   # Standard formatted output
   print("\n=== FORMATTED OUTPUT ===")
   print(f"Subject: {extracted_data.subject}")
   print(f"From: {extracted_data.sender.name} ({extracted_data.sender.role})")
   print("\nMain points:")
   for point in extracted_data.main_points:
       print(f"- {point}")

   print("\nMeetings:")
   for meeting in extracted_data.meetings:
       print(f"- {meeting.date} at {meeting.time}, Location: {meeting.location}")

   print("\nTasks:")
   for task in extracted_data.tasks:
       print(f"- {task.description}")
       print(
           f"  Assignee: {task.assignee}, Deadline: {task.deadline}, Priority: {task.priority}"
       )

asyncio.run(main())
