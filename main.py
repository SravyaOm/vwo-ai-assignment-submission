import os
import uuid
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from rq import Queue
from redis import Redis

import database as db
from worker import run_analysis_task

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI(title="Financial Document Analyzer API - Upgraded")

redis_conn = Redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'))
q = Queue(connection=redis_conn)

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Provide a comprehensive analysis."),
    db_session: Session = Depends(db.get_db)
):
    try:
        file_path = f"temp_{uuid.uuid4()}.pdf"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        new_job = db.AnalysisJob(id=str(uuid.uuid4()), status="queued")
        db_session.add(new_job)
        db_session.commit()
        db_session.refresh(new_job)

        q.enqueue(run_analysis_task, new_job.id, query.strip(), file_path)

        return {
            "status": "success",
            "message": "Analysis job has been queued.",
            "job_id": new_job.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{job_id}")
async def get_results(job_id: str, db_session: Session = Depends(db.get_db)):
    job = db_session.query(db.AnalysisJob).filter(db.AnalysisJob.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")

    return {
        "job_id": job.id,
        "status": job.status,
        "created_at": job.created_at,
        "result": job.result
    }

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is operational."}