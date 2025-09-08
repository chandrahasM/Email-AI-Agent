# Email Extraction Agent

A Python application that demonstrates how to use OpenAI's Agents framework to extract structured information from emails.

## Overview

This project showcases how to use OpenAI's Agents SDK to create an intelligent email processing system that can extract key information from email content and structure it into well-defined data models using Pydantic.

## OpenAI SDK Concepts Covered

### 1. Agent Creation and Configuration
- **Agent Initialization**: Creating an agent with a specific name and instructions
- **Agent Instructions**: Providing detailed instructions to guide the agent's behavior
- **Output Type Specification**: Using Pydantic models to define structured output formats

```python
email_extractor = Agent(
   name="Email Extractor",
   instructions="""You are an assistant that extracts structured information from emails...""",
   output_type=EmailData,  # This tells the agent to return data in EmailData format
)
```

### 2. Runner Execution
- **Asynchronous Execution**: Using async/await pattern for non-blocking agent execution
- **Runner Instance**: Creating and using a Runner to execute the agent
- **Input Formatting**: Properly formatting prompts for the agent

```python
async def process_email(email_text):
   runner = Runner()
   result = await runner.run(
       email_extractor,
       f"Please extract information from this email:\n\n{email_text}"
   )
   return result
```

### 3. Structured Data with Pydantic Integration
- **Data Modeling**: Using Pydantic BaseModel for structured data
- **Nested Models**: Creating complex data structures with nested models
- **Type Annotations**: Using Python type hints for better code clarity and validation
- **Optional Fields**: Handling optional data with Optional type

```python
class EmailData(BaseModel):
   subject: str
   sender: Person
   recipients: List[Person]
   main_points: List[str]
   meetings: List[Meeting]
   tasks: List[Task]
   next_steps: Optional[str]
```

### 4. Result Processing
- **Accessing Agent Results**: Extracting the final output from agent responses
- **JSON Serialization**: Converting Pydantic models to JSON for display or storage
- **Field Access**: Accessing nested fields in the structured output

```python
# Print the raw structured data
print(extracted_data.model_dump_json(indent=2))

# Accessing nested objects
print(f"Sender Name: {extracted_data.sender.name}")
```

## Key Benefits

1. **Structured Information Extraction**: Automatically converts unstructured email text into structured, typed data
2. **Type Safety**: Pydantic models ensure type validation and provide clear data structure
3. **Customizable Extraction**: The agent can be instructed to focus on specific types of information
4. **Nested Data Handling**: Complex relationships between data elements are preserved in the nested model structure

## Requirements

- Python 3.8+
- OpenAI Agents SDK
- Pydantic
- python-dotenv

## Setup

1. Clone this repository
2. Create a virtual environment: `python -m venv agents-venv`
3. Activate the virtual environment:
   - Windows: `agents-venv\Scripts\activate`
   - Unix/MacOS: `source agents-venv/bin/activate`
4. Install dependencies: `pip install openai-agents pydantic python-dotenv`
5. Create a `.env` file with your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`
6. Run the example: `python main.py`

## Example Output

The script will output:
1. Raw JSON representation of the extracted data
2. Examples of accessing specific fields in the data structure
3. Formatted output showing the extracted information in a readable format
