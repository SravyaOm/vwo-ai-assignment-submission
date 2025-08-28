import os
from redis import Redis
from rq import Queue, Worker
from sqlalchemy.orm import Session

import database as db
from crewai import Crew, Process
from agents import financial_analyst, investment_advisor, risk_assessor
from tasks import task_analysis, task_investment, task_risk

def run_analysis_task(job_id: str, query: str, file_path: str):
    """
    The long-running task that updates the database with the result.
    """
    db_session: Session = next(db.get_db())
    job = db_session.query(db.AnalysisJob).filter(db.AnalysisJob.id == job_id).first()
    
    if not job:
        return "Job not found in database."

    try:
        job.status = "in_progress"
        db_session.commit()

        financial_crew = Crew(
            agents=[financial_analyst, investment_advisor, risk_assessor],
            tasks=[task_analysis, task_investment, task_risk],
            process=Process.sequential,
            verbose=2
        )
        result = financial_crew.kickoff({'query': query, 'file_path': file_path})
        
        job.status = "completed"
        job.result = str(result)
        db_session.commit()

    except Exception as e:
        job.status = "failed"
        job.result = f"An error occurred: {str(e)}"
        db_session.commit()
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        db_session.close()

if __name__ == '__main__':
    listen = ['default']
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    conn = Redis.from_url(redis_url)

    # -- VVV CHANGED BLOCK VVV --
    # Create a list of Queue objects, each properly configured with a connection
    queues = [Queue(name, connection=conn) for name in listen]
    
    # Pass the list of configured queues to the Worker
    worker = Worker(queues, connection=conn)
    worker.work()
    # -- ^^^ CHANGED BLOCK ^^^ --