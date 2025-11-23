# import os
# import pandas as pd
# from dotenv import load_dotenv
# from crewai import Agent, Task, Crew, LLM
# from crewai.tools import tool

# # Load environment variables
# load_dotenv()
# google_api_key = os.getenv("GOOGLE_API_KEY")
# if not google_api_key:
#     raise ValueError("GOOGLE_API_KEY not found")

# # === LaundromatData Class with real Excel file reading ===
# class LaundromatData:
#     def __init__(self, pricing_path='data/pricing.xlsx', services_path='data/services.xlsx', orders_path='data/order_status.xlsx'):
#         try:
#             self.pricing_df = pd.read_excel(pricing_path)
#             self.services_df = pd.read_excel(services_path)
#             self.orders_df = pd.read_excel(orders_path) if os.path.exists(orders_path) else pd.DataFrame(columns=["OrderID", "Status"])
#         except Exception as e:
#             raise FileNotFoundError(f"Error loading files: {str(e)}")
#     @tool
#     def get_price(self, service_name):
#         """Returns the price and unit of a given laundry service by name."""
#         match = self.pricing_df[self.pricing_df['Service'].str.lower() == service_name.lower()]
#         if not match.empty:
#             price = match.iloc[0]['Price (INR)']
#             unit = match.iloc[0]['Unit']
#             return f"{price} INR {unit}"
#         return "Pricing information not found for that service."
#     @tool
#     def list_services(self):
#         """Returns a list of all services offered at the laundromat."""
#         return self.services_df.to_dict(orient='records')
#     @tool
#     def get_order_status(self, order_id):
#         """Returns the status of an order based on its ID."""
#         match = self.orders_df[self.orders_df['OrderID'].astype(str).str.upper() == order_id.upper()]
#         if not match.empty:
#             return f"Order {order_id.upper()} status: {match.iloc[0]['Status']}"
#         return "Sorry, no such order ID found."
#     @tool
    
#     def get_pickup_slots(self):
#         """Returns available pickup slots for the day."""
#         return "Available pickup slots: 9 AM, 11 AM, 1 PM, 3 PM, 5 PM, and 7 PM."
#     @tool
#     def report_issue(self, description):
#         """Records a customer issue in the issues file."""
#         issue_path = 'data/issues.xlsx'
#         new_issue = pd.DataFrame([{"Issue": description}])
#         if os.path.exists(issue_path):
#             existing = pd.read_excel(issue_path)
#             updated = pd.concat([existing, new_issue], ignore_index=True)
#         else:
#             updated = new_issue
#         updated.to_excel(issue_path, index=False)
#         return "Your issue has been recorded. We'll get back to you soon."

# # === LLM Setup ===
# llm = LLM(model="gemini/gemini-1.5-flash", api_key=google_api_key)
# data_loader = LaundromatData()

# # === Agents ===
# pricing_agent = Agent(
#     role="Pricing Agent",
#     goal="Answer any customer questions about pricing",
#     backstory="You know all prices in the pricing sheet",
#     tools=[data_loader.get_price],
#     verbose=True,
#     llm=llm,
# )

# services_agent = Agent(
#     role="Services Agent",
#     goal="Tell users what services are offered",
#     backstory="You read directly from the services Excel file",
#     tools=[data_loader.list_services],
#     verbose=True,
#     llm=llm,
# )

# order_status_agent = Agent(
#     role="Order Status Agent",
#     goal="Give order status based on order ID",
#     backstory="You read statuses from a real-time file",
#     tools=[data_loader.get_order_status],
#     verbose=True,
#     llm=llm,
# )

# pickup_agent = Agent(
#     role="Pickup Scheduler",
#     goal="Provide available pickup slots",
#     backstory="You manage and suggest time slots for customer orders",
#     tools=[data_loader.get_pickup_slots],
#     verbose=True,
#     llm=llm,
# )

# issue_agent = Agent(
#     role="Complaint Handler",
#     goal="Register any issues the customer reports",
#     backstory="You record complaints to the issues file and acknowledge it",
#     tools=[data_loader.report_issue],
#     verbose=True,
#     llm=llm,
# )

# chat_agent = Agent(
#     role="Welcome Helper",
#     goal="You are a welcoming agent who will greet users and coordinate with other agents to answer questions about laundry pricing, services, or order status.",
#     backstory="You've helped thousands of customers get quick and accurate info from the team. You delegate tasks to the best expert agent.",
#     verbose=True,
#     llm=llm,
#     allow_delegation=True  
# )


# # === Main Loop ===
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

#             chat_task = Task(
#                 description=f"Respond or delegate: '{user_query}'",
#                 agent=chat_agent,
#                 expected_output="A complete and friendly response based on customer's query."
#             )

#             crew = Crew(
#                 agents=[chat_agent, pricing_agent, services_agent, order_status_agent, pickup_agent, issue_agent],
#                 tasks=[chat_task],
#                 verbose=True
#             )

#             result = crew.kickoff()
#             print(f"\nAssistant: {result}")
#             print("-" * 50)

#         except KeyboardInterrupt:
#             print("\nAssistant: Goodbye! 👋")
#             break
#         except Exception as e:
#             print(f"\nError: {str(e)}")

# if __name__ == "__main__":
#     main()

    
    
    
import os
import pandas as pd
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM, Process
from crewai.tools import tool

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found")

# === LaundromatData Class ===
class LaundromatData:
    def __init__(self, pricing_path='data/pricing.xlsx', services_path='data/services.xlsx', orders_path='data/order_status.xlsx'):
        try:
            self.pricing_df = pd.read_excel(pricing_path)
            self.services_df = pd.read_excel(services_path)
            self.orders_df = pd.read_excel(orders_path) if os.path.exists(orders_path) else pd.DataFrame(columns=["OrderID", "Status"])
        except Exception as e:
            raise FileNotFoundError(f"Error loading files: {str(e)}")

# Create a global instance
data_loader = LaundromatData()

# === Standalone Tool Functions ===
@tool
def get_price(service_name: str) -> str:
    """Returns the price and unit of a given laundry service by name."""
    match = data_loader.pricing_df[data_loader.pricing_df['Service'].str.lower() == service_name.lower()]
    if not match.empty:
        price = match.iloc[0]['Price (INR)']
        unit = match.iloc[0]['Unit']
        return f"{price} INR per {unit}"
    return "Pricing information not found for that service."

@tool
def list_services() -> str:
    """Returns a list of all services offered at the laundromat."""
    services_list = []
    for _, row in data_loader.services_df.iterrows():
        services_list.append(f"- {row['Service']}: {row['Description']}")
    return "\n".join(services_list)

@tool
def get_order_status(order_id: str) -> str:
    """Returns the status of an order based on its ID."""
    match = data_loader.orders_df[data_loader.orders_df['OrderID'].astype(str).str.upper() == order_id.upper()]
    if not match.empty:
        return f"Order {order_id.upper()} status: {match.iloc[0]['Status']}"
    return "Sorry, no such order ID found."

@tool
def get_pickup_slots() -> str:
    """Returns available pickup slots for the day."""
    return "Available pickup slots: 9 AM, 11 AM, 1 PM, 3 PM, 5 PM, and 7 PM."

@tool
def report_issue(description: str) -> str:
    """Records a customer issue in the issues file."""
    issue_path = 'data/issues.xlsx'
    new_issue = pd.DataFrame([{"Issue": description}])
    if os.path.exists(issue_path):
        existing = pd.read_excel(issue_path)
        updated = pd.concat([existing, new_issue], ignore_index=True)
    else:
        updated = new_issue
    updated.to_excel(issue_path, index=False)
    return "Your issue has been recorded. We'll get back to you soon."

# === LLM Setup ===
llm = LLM(model="gemini/gemini-1.5-flash", api_key=google_api_key)

# === Specialist Agents ===
pricing_specialist = Agent(
    role="Pricing Specialist",
    goal="Provide accurate pricing information for all laundry services",
    backstory="""You are an expert in laundry service pricing. You have access to the complete pricing database 
    and can provide exact costs for any service. You only handle pricing-related queries.""",
    tools=[get_price],
    verbose=True,
    llm=llm,
)

services_specialist = Agent(
    role="Services Specialist", 
    goal="Explain all available laundry services and their details",
    backstory="""You are an expert in laundry services. You know all the services offered, their descriptions, 
    and can help customers understand what's available. You only handle service information queries.""",
    tools=[list_services],
    verbose=True,
    llm=llm,
)

order_specialist = Agent(
    role="Order Tracking Specialist",
    goal="Track and provide order status information",
    backstory="""You are an expert in order tracking. You can look up any order ID and provide current status 
    information. You only handle order status queries.""",
    tools=[get_order_status],
    verbose=True,
    llm=llm,
)

pickup_specialist = Agent(
    role="Pickup Scheduling Specialist",
    goal="Provide pickup slot information and scheduling assistance",
    backstory="""You are an expert in pickup scheduling. You know all available time slots and can help customers 
    understand pickup options. You only handle pickup scheduling queries.""",
    tools=[get_pickup_slots],
    verbose=True,
    llm=llm,
)

issue_specialist = Agent(
    role="Customer Issue Specialist",
    goal="Handle customer complaints and issues",
    backstory="""You are an expert in customer service. You can record customer issues, complaints, and feedback 
    in the system. You only handle customer issue and complaint queries.""",
    tools=[report_issue],
    verbose=True,
    llm=llm,
)

# === Manager Agent ===
manager_agent = Agent(
    role="Customer Service Manager",
    goal="Coordinate with specialist agents to provide comprehensive customer service",
    backstory="""You are an experienced customer service manager who coordinates with specialist agents. 
    You understand customer queries and know which specialist can best help with each type of request.
    You can delegate tasks to:
    - Pricing Specialist: for pricing and cost queries
    - Services Specialist: for service information and descriptions
    - Order Specialist: for order status and tracking
    - Pickup Specialist: for pickup scheduling and time slots
    - Issue Specialist: for complaints and problems
    
    You make intelligent decisions about which specialist to involve based on the customer's needs.""",
    verbose=True,
    llm=llm,
    allow_delegation=True
)

# === Create Tasks Based on Query ===
def create_tasks_for_query(user_query):
    """Create appropriate tasks based on the user query"""
    
    # Manager task - always present to coordinate
    manager_task = Task(
        description=f"""Analyze this customer query and coordinate with the appropriate specialist agents to provide a complete response: "{user_query}"
        
        Determine which specialist(s) can best help with this query and delegate accordingly. Provide a comprehensive and friendly response to the customer.""",
        agent=manager_agent,
        expected_output="A complete, helpful response to the customer's query, coordinating with specialist agents as needed."
    )
    
    return [manager_task]

# === Main Loop ===
def main():
    print("🧺 Welcome to the Laundromat Chatbot! Type 'quit' to exit.\n")
    
    while True:
        try:
            user_query = input("Customer: ").strip()
            if user_query.lower() in ['quit', 'exit']:
                print("Assistant: Thanks for visiting! 👋")
                break
            if not user_query:
                continue

            # Create tasks for the query
            tasks = create_tasks_for_query(user_query)
            
            # Create hierarchical crew
            crew = Crew(
                agents=[manager_agent, pricing_specialist, services_specialist, order_specialist, pickup_specialist, issue_specialist],
                tasks=tasks,
                process=Process.hierarchical,
                manager_llm=llm,
                verbose=True
            )

            result = crew.kickoff()
            print(f"\nAssistant: {result}")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\nAssistant: Goodbye! 👋")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()