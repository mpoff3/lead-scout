from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from agent.agent_setup import setup_crew, post_comment_to_reddit
import traceback
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://lead-scout-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "LeadScout API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

class URLInput(BaseModel):
    url: str

class TaskResult(BaseModel):
    task_description: str
    agent_role: str
    output: str

class AgentResponse(BaseModel):
    project_summary: Optional[str] = None
    marketing_analysis: Optional[str] = None
    reddit_research: Optional[str] = None
    content_marketing: Optional[str] = None
    status: str = "success"
    message: str = ""

@app.post("/api/analyze", response_model=AgentResponse)
async def analyze_url(url_input: URLInput):
    try:
        logger.info(f"Starting analysis for URL: {url_input.url}")
        
        # Setup crew with the provided URL
        logger.info("Setting up crew...")
        crew, adapter = setup_crew(url_input.url)
        
        # Run the crew tasks
        logger.info("Kicking off crew tasks...")
        crew.kickoff()
        
        # Collect results
        logger.info("Collecting task results...")
        results = AgentResponse(
            project_summary=str(crew.tasks[0].output.raw) if hasattr(crew.tasks[0], 'output') else None,
            marketing_analysis=str(crew.tasks[1].output.raw) if hasattr(crew.tasks[1], 'output') else None,
            reddit_research=str(crew.tasks[2].output.raw) if hasattr(crew.tasks[2], 'output') else None,
            content_marketing=str(crew.tasks[3].output.raw) if hasattr(crew.tasks[3], 'output') else None
        )
        
        # Post comment to Reddit if content marketing was successful
        if results.content_marketing:
            logger.info("Posting comment to Reddit...")
            task = f"Post this comment to this Reddit post, use https://old.reddit.com UI instead of new UI:\n {results.content_marketing}"
            await post_comment_to_reddit(task)
        
        # Clean up adapter
        logger.info("Cleaning up adapter...")
        adapter.close()
        
        logger.info("Analysis completed successfully")
        return results
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 