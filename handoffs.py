import asyncio
import logging
from agents import Agent, handoff, Runner
from dotenv import load_dotenv
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("handoff_logger")

load_dotenv()

# Create specialist agents
billing_agent = Agent(
   name="Billing Agent",
   instructions="""You are a billing specialist who helps customers with payment issues.
   Focus on resolving billing inquiries, subscription changes, and refund requests.""",
)

technical_agent = Agent(
   name="Technical Agent",
   instructions="""You are a technical support specialist who helps with product issues.
   Assist users with troubleshooting, error messages, and how-to questions.""",
)

# Create a triage agent that can hand off to specialists
triage_agent = Agent(
   name="Customer Service",
   instructions="""You are the initial customer service contact who helps direct
   customers to the right specialist.
  
   If the customer has billing or payment questions, hand off to the Billing Agent.
   If the customer has technical problems or how-to questions, hand off to the Technical Agent.
   For general inquiries or questions about products, you can answer directly.
   
   IMPORTANT: When you decide to hand off to another agent, explicitly state your reasoning
   in your response like this: "HANDOFF REASON: [explain why you're handing off]"
   """,
   handoffs=[billing_agent, technical_agent],  # Direct handoff to specialist agents
)

class HandoffTracker:
    def __init__(self):
        self.handoffs = []
    
    def track_run(self, agent_name, request):
        logger.info(f"Starting request with agent: {agent_name}")
        logger.info(f"Request: {request}")
    
    def track_response(self, response, agent_name):
        logger.info(f"Response from {agent_name}:")
        
        # Check if there was a handoff by examining the trace
        if hasattr(response, 'trace') and response.trace:
            self.analyze_trace(response.trace)
        
        # Also check if the final agent is different from the initial agent
        if hasattr(response, 'agent_name') and response.agent_name != "Customer Service":
            logger.info(f"HANDOFF DETECTED: Final response from {response.agent_name}")
        
        logger.info("=" * 50)
    
    def analyze_trace(self, trace):
        """Analyze the trace to find handoff information"""
        if not trace:
            return
        print("trace",trace)
        # Look for handoff patterns in the trace
        for step in trace:
            if isinstance(step, dict) and 'handoff' in str(step).lower():
                logger.info(f"HANDOFF TRACE: {json.dumps(step, indent=2)}")
            
            # Look for handoff reason in messages
            if isinstance(step, dict) and 'messages' in step:
                for message in step.get('messages', []):
                    content = message.get('content', '')
                    if 'HANDOFF REASON' in content:
                        reason = content.split('HANDOFF REASON:')[1].strip()
                        logger.info(f"HANDOFF REASON: {reason}")

async def handle_customer_request(request, tracker):
    # Track the start of the request
    tracker.track_run(triage_agent.name, request)
    
    # Create a runner
    runner = Runner()
    
    # Run the agent with the request
    result = await runner.run(triage_agent, request)
    
    # Track the response
    tracker.track_response(result, triage_agent.name)
    
    return result.final_output


# Example customer inquiries
billing_inquiry = (
   "I was charged twice for my subscription last month. Can I get a refund?"
)
technical_inquiry = (
   "The app keeps crashing when I try to upload photos. How can I fix this?"
)
general_inquiry = "What are your business hours?"


async def main():
    # Create a handoff tracker
    tracker = HandoffTracker()
    
    print("\n--- BILLING INQUIRY ---")
    billing_response = await handle_customer_request(billing_inquiry, tracker)
    print(f"Billing inquiry response:\n{billing_response}\n")

    print("\n--- TECHNICAL INQUIRY ---")
    technical_response = await handle_customer_request(technical_inquiry, tracker)
    print(f"Technical inquiry response:\n{technical_response}\n")

    print("\n--- GENERAL INQUIRY ---")
    general_response = await handle_customer_request(general_inquiry, tracker)
    print(f"General inquiry response:\n{general_response}")

asyncio.run(main())
