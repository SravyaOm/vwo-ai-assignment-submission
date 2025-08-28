from crewai import Task
from agents import financial_analyst, investment_advisor, risk_assessor
from tools import read_document_tool

# Task for Financial Analysis
task_analysis = Task(
    description=(
        "Analyze the financial document located at the path: {file_path}. "
        "Your analysis should extract key financial metrics such as Revenue, Net Income, and EPS. "
        "Summarize the company's performance for the quarter, and identify any significant trends or anomalies. "
        "The user's primary area of interest is: {query}."
    ),
    expected_output=(
        "A detailed and well-structured summary of the financial document, including: "
        "1. A list of key financial figures and metrics. "
        "2. A clear summary of the company's operational highlights. "
        "3. A concluding overview of the company's financial health and recent performance."
    ),
    agent=financial_analyst,
    tools=[read_document_tool]
)

# Task for Investment Recommendation
task_investment = Task(
    description=(
        "Using the financial analysis from the previous step, develop concrete investment recommendations. "
        "Address the user's query: '{query}'. "
        "Use the search tool to research current market trends and public sentiment related to the company. "
        "Your recommendation must be well-reasoned, actionable, and directly supported by data from the analysis."
    ),
    expected_output=(
        "A comprehensive investment recommendation report that includes: "
        "1. A clear 'buy', 'sell', or 'hold' strategy. "
        "2. A detailed explanation of the reasoning, supported by both the financial analysis and current market context. "
        "3. Identification of potential growth areas or sectors to monitor."
    ),
    agent=investment_advisor,
    context=[task_analysis]
)

# Task for Risk Assessment
task_risk = Task(
    description=(
        "Based on the preceding financial analysis and investment recommendations, perform a thorough risk assessment. "
        "Identify potential risks, including market risks, operational risks, and any financial red flags present in the document. "
        "Directly relate these risks back to the user's query: '{query}'."
    ),
    expected_output=(
        "A concise risk assessment report that includes: "
        "1. A categorized list of potential risks (e.g., Market, Financial, Operational). "
        "2. A brief explanation of how each identified risk could impact the investment. "
        "3. A final concluding statement on the company's overall risk profile."
    ),
    agent=risk_assessor,
    context=[task_analysis, task_investment]
)