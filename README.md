# Financial Document Analyzer

## 🚀 Project Overview
This project is an AI-powered financial document analysis system built with **CrewAI** and **FastAPI**. It allows users to upload a financial document (e.g., a quarterly report) in PDF format and receive a comprehensive analysis that includes a financial summary, investment recommendations, and a risk assessment.

The system uses a crew of specialized AI agents to perform a multi-step analysis, ensuring a detailed and structured output.

## ⚙️ System Architecture
The application is composed of three main AI agents that work sequentially:

1.  **Financial Analyst**: Reads the document, extracts key financial data, and provides an objective summary.
2.  **Investment Advisor**: Takes the analyst's summary, considers current market trends, and formulates actionable investment advice.
3.  **Risk Assessor**: Reviews both the analysis and the investment advice to identify and report potential risks.



---

## 🐛 Bugs Found and Fixes Implemented

The initial codebase was non-functional due to a combination of satirical content and critical bugs. Here is a summary of the issues and their resolutions:

### 1. **Dependencies and Environment**
* **Bug**: The `requirements.txt` file contained an invalid version for `crewai` (`0.130.0`) and was missing essential libraries (`pypdf` for reading PDFs, `python-dotenv`, `langchain-google-genai`, `langchain-community`).
* **Fix**: Corrected the `crewai` version to a stable release and added all necessary libraries to `requirements.txt`.

### 2. **LLM Configuration**
* **Bug**: The language model was not instantiated. The code had a placeholder `llm = llm` in `agents.py`.
* **Fix**: Implemented proper instantiation of a language model using `ChatGoogleGenerativeAI` from the `langchain-google-genai` library, configured to use a Google API key from a `.env` file.

### 3. **AI Agent Definitions**
* **Bug**: The agents' roles, goals, and backstories were written as jokes, instructing them to produce made-up, unreliable, and unprofessional content. The agent configurations (e.g., `max_iter=1`) were overly restrictive.
* **Fix**: Rewrote the agent prompts to be professional and task-oriented. Removed the superfluous "Verifier" agent and focused on a three-agent crew. Adjusted configurations to allow agents to function effectively.

### 4. **AI Task Definitions**
* **Bug**: The tasks were also satirical and lacked a logical structure. There was no connection or context-sharing between them.
* **Fix**: Redefined the tasks to create a sequential workflow (`Analysis -> Investment Advice -> Risk Assessment`). Implemented `context` passing, so each task builds upon the output of the previous one.

### 5. **Tooling**
* **Bug**: The `FinancialDocumentTool` in `tools.py` was broken. It used an undefined `Pdf` class and was incorrectly defined as an `async` function.
* **Fix**: Replaced the broken implementation with `PyPDFLoader` from `langchain-community` to correctly read and process PDF files. The tool was restructured as a standard synchronous function within a `BaseTool` class for compatibility with CrewAI.

### 6. **Application Logic (`main.py`)**
* **Bug**: The FastAPI application only initialized one agent and one task, ignoring the rest of the defined crew. The `file_path` for the uploaded document was not correctly passed into the CrewAI workflow.
* **Fix**: Reconfigured the `run_crew` function to initialize the complete, three-agent crew and the full sequence of tasks. Ensured the `file_path` is passed into the `crew.kickoff` method's context, making it available to the tools.

---

## ⚡ Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites
* Python 3.9+
* A Google API Key with the Gemini API enabled.

### 1. Clone the Repository
```sh
git clone <your-repo-link>
cd financial-document-analyzer

🏆 Bonus Features Implemented
1. Queue Worker Model (Redis & RQ)
To handle long-running AI analyses without blocking the API, the system was upgraded with a background worker model using Redis and the RQ (Redis Queue) library.

The /analyze endpoint now immediately returns a job_id.

A separate worker.py process listens on the queue and executes the analysis in the background.

2. Database Integration (SQLite & SQLAlchemy)
To persist analysis results, the application was integrated with a database.

An SQLite database (analysis_jobs.db) stores the status and results of each job.

The worker updates the database upon job completion.

A new /results/{job_id} endpoint allows users to retrieve the final analysis from the database at any time.
