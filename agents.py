import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import search_tool, read_document_tool

# Load environment variables from a .env file
load_dotenv()

# Initialize the Gemini Language Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Define the Financial Analyst Agent
financial_analyst = Agent(
    role="Expert Financial Analyst",
    goal="Analyze the provided financial document to extract key data, summarize performance, and identify major financial trends relevant to the user's query: {query}",
    backstory=(
        "You are an experienced financial analyst with a keen eye for detail and a deep understanding of financial statements. "
        "You excel at interpreting complex financial data and presenting it in a clear, concise, and insightful manner."
    ),
    llm=llm,
    tools=[read_document_tool, search_tool],
    allow_delegation=False,
    verbose=True,
    memory=True
)

# Define the Investment Advisor Agent
investment_advisor = Agent(
    role="Seasoned Investment Advisor",
    goal="Provide strategic investment advice and recommendations based on the financial analysis. Your advice must be tailored to the user's query: {query}",
    backstory=(
        "You are a veteran investment advisor with a proven track record of success. You specialize in translating in-depth financial analysis "
        "into actionable investment strategies, taking into account current market conditions and risk tolerance."
    ),
    llm=llm,
    tools=[search_tool],
    allow_delegation=True,
    verbose=True,
    memory=True
)

# Define the Risk Assessor Agent
risk_assessor = Agent(
    role="Financial Risk Assessment Specialist",
    goal="Identify and evaluate potential financial and market risks based on the provided financial document and analysis. Focus on risks that are relevant to the user's query: {query}",
    backstory=(
        "You are a meticulous risk assessor who excels at identifying potential pitfalls and vulnerabilities in financial reports. "
        "You provide a balanced and comprehensive view of risks, helping to inform a well-rounded investment strategy."
    ),
    llm=llm,
    tools=[search_tool],
    allow_delegation=False,
    verbose=True,
    memory=True
)