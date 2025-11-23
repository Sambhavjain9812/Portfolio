# import os
# import pandas as pd
# from dotenv import load_dotenv
# from crewai import Agent, Task, Crew, Process
# from crewai.tools import tool
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# from crewai import Agent, Task, Crew, LLM

# load_dotenv()
# google_api_key = os.getenv("GOOGLE_API_KEY")
# grok_api_key = os.getenv("GROK")
# if not google_api_key:
#     raise ValueError("GOOGLE_API_KEY not found in environment variables")

# # === LaundromatData Class ===
# class LaundromatData:
#     def __init__(self, pricing_path='data/pricing.xlsx', services_path='data/services.xlsx', orders_path='data/order_status.xlsx'):
#         try:
#             self.pricing_df = pd.read_excel(pricing_path)
#             self.services_df = pd.read_excel(services_path)
#             self.orders_df = pd.read_excel(orders_path) if os.path.exists(orders_path) else pd.DataFrame(columns=["OrderID", "Status"])
#         except Exception as e:
#             raise FileNotFoundError(f"Error loading files: {str(e)}")

# # Create a global instance
# # data_loader = LaundromatData()
# @tool
# def get_price(service_name: str) -> str:
#     """Returns the price and unit of a given laundry service by name."""
#     try:
#         df = pd.read_excel('data/pricing.xlsx')
#         match = df[df['Service'].str.lower() == service_name.lower()]
#         if not match.empty:
#             price = match.iloc[0]['Price (INR)']
#             unit = match.iloc[0]['Unit']
#             return f"{service_name} costs {price} INR per {unit}"
#         return f"Pricing information not found for '{service_name}'"
#     except Exception as e:
#         return f"Error retrieving price: {str(e)}"


# @tool
# def list_services() -> str:
#     """Returns a detailed list of all services offered at the laundromat."""
#     try:
#         df = pd.read_excel('data/services.xlsx')
#         services_list = ["Available services:"]
#         for _, row in df.iterrows():
#             services_list.append(f"- {row['Service']}: {row['Description']}")
#         return "\n".join(services_list)
#     except Exception as e:
#         return f"Error retrieving services: {str(e)}"


# @tool
# def get_order_status(order_id: str) -> str:
#     """Returns the status of an order based on its ID."""
#     try:
#         if os.path.exists('data/order_status.xlsx'):
#             df = pd.read_excel('data/order_status.xlsx')
#         else:
#             return f"No order found with ID: {order_id}"

#         match = df[df['OrderID'].astype(str).str.upper() == order_id.upper()]
#         if not match.empty:
#             return f"Order {order_id.upper()} status: {match.iloc[0]['Status']}"
#         return f"No order found with ID: {order_id}"
#     except Exception as e:
#         return f"Error checking order status: {str(e)}"


# @tool
# def report_issue(description: str) -> str:
#     """Records a customer issue in the issues file and confirms receipt."""
#     try:
#         issue_path = 'data/issues.xlsx'
#         new_issue = pd.DataFrame([{"Issue": description, "Status": "Pending"}])

#         if os.path.exists(issue_path):
#             existing = pd.read_excel(issue_path)
#             updated = pd.concat([existing, new_issue], ignore_index=True)
#         else:
#             updated = new_issue

#         updated.to_excel(issue_path, index=False)
#         return f"Issue recorded successfully: '{description}'. We'll contact you soon."
#     except Exception as e:
#         return f"Error reporting issue: {str(e)}"

# # === Improved Tool Functions with Better Error Handling ===
# # @tool
# # def get_price(service_name: str) -> str:
# #     """Returns the price and unit of a given laundry service by name. Always include the service name in your response."""
# #     try:
# #         match = data_loader.pricing_df[data_loader.pricing_df['Service'].str.lower() == service_name.lower()]
# #         if not match.empty:
# #             price = match.iloc[0]['Price (INR)']
# #             unit = match.iloc[0]['Unit']
# #             return f"{service_name} costs {price} INR per {unit}"
# #         return f"Pricing information not found for '{service_name}'"
# #     except Exception as e:
# #         return f"Error retrieving price: {str(e)}"

# # @tool
# # def list_services() -> str:
# #     """Returns a detailed list of all services offered at the laundromat."""
# #     try:
# #         services_list = ["Available services:"]
# #         for _, row in data_loader.services_df.iterrows():
# #             services_list.append(f"- {row['Service']}: {row['Description']}")
# #         return "\n".join(services_list)
# #     except Exception as e:
# #         return f"Error retrieving services: {str(e)}"

# # @tool
# # def get_order_status(order_id: str) -> str:
# #     """Returns the status of an order based on its ID. Always include the order ID in your response."""
# #     try:
# #         match = data_loader.orders_df[data_loader.orders_df['OrderID'].astype(str).str.upper() == order_id.upper()]
# #         if not match.empty:
# #             return f"Order {order_id.upper()} status: {match.iloc[0]['Status']}"
# #         return f"No order found with ID: {order_id}"
# #     except Exception as e:
# #         return f"Error checking order status: {str(e)}"

# @tool
# def get_pickup_slots() -> str:
#     """Returns available pickup slots for the day in a clear format."""
#     try:
#         return "Available pickup slots today:\n- 9 AM\n- 11 AM\n- 1 PM\n- 3 PM\n- 5 PM\n- 7 PM"
#     except Exception as e:
#         return f"Error retrieving pickup slots: {str(e)}"

# # @tool
# # def report_issue(description: str) -> str:
# #     """Records a customer issue in the issues file and confirms receipt."""
# #     try:
# #         issue_path = 'data/issues.xlsx'
# #         new_issue = pd.DataFrame([{"Issue": description, "Status": "Pending"}])
        
# #         if os.path.exists(issue_path):
# #             existing = pd.read_excel(issue_path)
# #             updated = pd.concat([existing, new_issue], ignore_index=True)
# #         else:
# #             updated = new_issue
            
# #         updated.to_excel(issue_path, index=False)
# #         return f"Issue recorded successfully: '{description}'. We'll contact you soon."
# #     except Exception as e:
# #         return f"Error reporting issue: {str(e)}"

# # === Improved LLM Setup ===
# # llm = ChatGoogleGenerativeAI(
# #     model="gemini-pro",
# #     google_api_key=google_api_key,
# #     temperature=0.3
# # )
# llm2 = LLM(model="gemini/gemini-1.5-flash", api_key=google_api_key)
# llm = LLM(
#     model="groq/gemma2-9b-it",
#     temperature=0.7,
#     api_key=grok_api_key
# )
# # === Enhanced Specialist Agents ===
# def create_specialist_agent(role, goal, backstory, tools):
#     return Agent(
#         role=role,
#         goal=goal,
#         backstory=backstory,
#         tools=tools,
#         verbose=False,
#         llm=llm,
#         max_iter=3,  # Prevent infinite loops
#         max_rpm=10,  # Rate limiting
#         memory=False # Allow agents to remember context
#     )

# pricing_specialist = create_specialist_agent(
#     role="Pricing Specialist",
#     goal="Provide accurate pricing information for all laundry services",
#     backstory="Expert in laundry service pricing with access to complete pricing database.",
#     tools=[get_price]
# )

# services_specialist = create_specialist_agent(
#     role="Services Specialist", 
#     goal="Explain all available laundry services and their details",
#     backstory="Expert in laundry services with complete knowledge of offerings.",
#     tools=[list_services]
# )

# order_specialist = create_specialist_agent(
#     role="Order Tracking Specialist",
#     goal="Track and provide order status information",
#     backstory="Expert in order tracking with access to order database.",
#     tools=[get_order_status]
# )

# pickup_specialist = create_specialist_agent(
#     role="Pickup Scheduling Specialist",
#     goal="Provide pickup slot information and scheduling assistance",
#     backstory="Expert in pickup scheduling with knowledge of all time slots.",
#     tools=[get_pickup_slots]
# )

# issue_specialist = create_specialist_agent(
#     role="Customer Issue Specialist",
#     goal="Handle customer complaints and issues",
#     backstory="Expert in customer service with ability to record issues.",
#     tools=[report_issue]
# )

# # === Enhanced Manager Agent ===
# manager_agent = Agent(
#     role="Customer Service Manager",
#     goal="Coordinate with specialist agents to provide comprehensive customer service",
#     backstory="""Experienced manager who understands customer queries and delegates to specialists:
#     - Pricing: cost queries
#     - Services: service information
#     - Order: status tracking
#     - Pickup: scheduling
#     - Issue: complaints""",
#     verbose=True,
#     llm=llm,
#     allow_delegation=True,
#     memory=True,
#     max_iter=7,
#     step_callback=lambda step: print(f"Manager processing step: {step.description}")  # Debugging
# )

# # === Task Creation with Better Context ===
# def create_tasks_for_query(user_query):
#     """Create tasks with clear instructions and expected outputs"""
#     manager_task = Task(
#         description=f"""Analyze this customer query and coordinate response:
#         Query: "{user_query}"
        
#         Rules:
#         1. Identify which specialist(s) can help
#         2. Delegate appropriately
#         3. Compile a complete response
#         4. Be friendly and professional""",
#         agent=manager_agent,
#         expected_output="A complete, helpful response addressing all aspects of the customer's query.",
#         output_file="output.txt"  # Optional: save responses
#     )
    
#     return [manager_task]

# # === Main Loop with Better Error Handling ===
# def main():
#     print("🧺 Welcome to the Laundromat Chatbot! Type 'quit' to exit.\n")
    
#     while True:
#         try:
#             user_query = input("Customer: ").strip()
#             if user_query.lower() in ['quit', 'exit']:
#                 print("Assistant: Thanks for visiting! 👋")
#                 break
#             if not user_query:
#                 continue

#             tasks = create_tasks_for_query(user_query)
            
#             crew = Crew(
#                 agents=[manager_agent, pricing_specialist, services_specialist, 
#                        order_specialist, pickup_specialist, issue_specialist],
#                 tasks=tasks,
#                 process=Process.hierarchical,
#                 manager_llm=llm,
#                 verbose=True  # More detailed logging
#             )

#             result = crew.kickoff()
#             print(f"\nAssistant: {result}\n{'='*50}\n")

#         except KeyboardInterrupt:
#             print("\nAssistant: Goodbye! 👋")
#             break
#         except Exception as e:
#             print(f"\nError processing request: {str(e)}")
            

# if __name__ == "__main__":
#     # Create data directory if it doesn't exist
#     os.makedirs("data", exist_ok=True)
#     main()


import os
import pandas as pd
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# Load your API keys
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
grok_api_key = os.getenv("GROK")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY missing")
if not grok_api_key:
    raise ValueError("GROK missing")

# Tools that access files at runtime

@tool
def get_price(service_name: str) -> str:
    """
    Input: Name of the laundry service (e.g., 'Dry Cleaning')
    Output: Pricing info or not-found message.
    """
    try:
        df = pd.read_excel('data/pricing.xlsx')
        match = df[df['Service'].str.lower() == service_name.lower()]
        if not match.empty:
            price = match.iloc[0]['Price (INR)']
            unit = match.iloc[0]['Unit']
            return f"{service_name} costs {price} INR per {unit}"
        return f"Pricing information not found for '{service_name}'"
    except Exception as e:
        return f"Error retrieving price: {str(e)}"

@tool
def list_services() -> str:
    """
    Outputs a formatted list of services and their descriptions.
    """
    try:
        df = pd.read_excel('data/services.xlsx')
        lines = ["Available services:"]
        for _, row in df.iterrows():
            lines.append(f"- {row['Service']}: {row['Description']}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error retrieving services: {str(e)}"

@tool
def get_order_status(order_id: str) -> str:
    """
    Input: Order ID string
    Output: Status or not-found message
    """
    try:
        path = 'data/order_status.xlsx'
        if not os.path.exists(path):
            return f"No order found with ID: {order_id}"
        df = pd.read_excel(path)
        match = df[df['OrderID'].astype(str).str.upper() == order_id.upper()]
        if not match.empty:
            return f"Order {order_id.upper()} status: {match.iloc[0]['Status']}"
        return f"No order found with ID: {order_id}"
    except Exception as e:
        return f"Error checking order status: {str(e)}"

@tool
def get_pickup_slots() -> str:
    """Lists the available pickup slots for today."""
    return "Available pickup slots today:\n- 9 AM\n- 11 AM\n- 1 PM\n- 3 PM\n- 5 PM\n- 7 PM"

@tool
def report_issue(description: str) -> str:
    """
    Input: issue description
    Output: confirmation of recording issue
    """
    try:
        path = 'data/issues.xlsx'
        new = pd.DataFrame([{"Issue": description, "Status": "Pending"}])
        if os.path.exists(path):
            existing = pd.read_excel(path)
            updated = pd.concat([existing, new], ignore_index=True)
        else:
            updated = new
        updated.to_excel(path, index=False)
        return f"Issue recorded successfully: '{description}'. We'll contact you soon."
    except Exception as e:
        return f"Error reporting issue: {str(e)}"

# Initialize LLM
llm = LLM(model="groq/gemma2-9b-it", temperature=0.7, api_key=grok_api_key)

# Helper to create agents
def create_specialist_agent(role, goal, backstory, tools):
    return Agent(
        role=role, goal=goal, backstory=backstory, tools=tools,
        verbose=False, llm=llm, max_iter=3, max_rpm=10, memory=False
    )

pricing_specialist = create_specialist_agent(
    "Pricing Specialist",
    "Provide accurate pricing info for laundry services",
    "Expert in laundry service pricing, expects a simple service-name string input.",
    [get_price]
)

services_specialist = create_specialist_agent(
    "Services Specialist",
    "Explain all available laundry services",
    "Expert in services list and descriptions.",
    [list_services]
)

order_specialist = create_specialist_agent(
    "Order Tracking Specialist",
    "Provide order status based on ID",
    "Expert in order tracking; expects an order ID string.",
    [get_order_status]
)

pickup_specialist = create_specialist_agent(
    "Pickup Scheduling Specialist",
    "Give available pickup slots for today",
    "Expert in schedule; outputs time slots.",
    [get_pickup_slots]
)

issue_specialist = create_specialist_agent(
    "Customer Issue Specialist",
    "Log customer issues and confirm recording",
    "Expert in recording issues; input is the issue text string.",
    [report_issue]
)

# Manager Agent orchestrates others
from langchain_core.agents import AgentFinish, AgentAction

def safe_step_callback(step):
    if isinstance(step, AgentFinish):
        print(f"Manager Step (Finished): {step.return_values.get('output', '')}")
    elif hasattr(step, "description"):
        print(f"Manager Step: {step.description}")
    else:
        print("Manager Step: Unknown step format")

# Then pass it here:
manager_agent = Agent(
    role="Customer Service Manager",
    goal="Delegate queries to correct specialist and compile responses",
    backstory=(
        "Manages customer requests and sends exact string arguments to matching tools. "
        "If a query is about cost, call get_price(service_name). "
        "If a query is about services, call list_services() with no args. "
        "And so on."
    ),
    verbose=True,
    llm=llm,
    allow_delegation=True,
    memory=False,
    max_iter=7,
    step_callback=safe_step_callback
)
def create_tasks_for_query(user_query):
    return [
        Task(
            description=(
                f"User query: \"{user_query}\". "
                "Decide which specialist tool to invoke with a basic string argument. "
                "Return the final composed answer."
            ),
            agent=manager_agent,
            expected_output="A full, friendly reply",
            output_file="output.txt"
        )
    ]

def main():
    os.makedirs("data", exist_ok=True)
    print("🧺 Welcome! Type 'quit' to exit.")
    while True:
        try:
            query = input("Customer: ").strip()
            if query.lower() in ['quit', 'exit']:
                print("Assistant: Thanks! 👋")
                break
            if not query:
                continue

            crew = Crew(
                agents=[
                    manager_agent,
                    pricing_specialist,
                    services_specialist,
                    order_specialist,
                    pickup_specialist,
                    issue_specialist
                ],
                tasks=create_tasks_for_query(query),
                process=Process.hierarchical,
                manager_llm=llm,
                verbose=True,
            )
            response = crew.kickoff()
            print(f"\nAssistant: {response}\n{'='*50}\n")
        except KeyboardInterrupt:
            print("\nAssistant: Goodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
