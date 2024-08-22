from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src import openai_api
from pydantic import BaseModel


router = APIRouter()

class jobRecommendations(BaseModel):
    skills: list

@router.post("/job_recommendations")
async def job_recommendations(request: jobRecommendations):
    
    skills = request.skills
    skills = ', '.join(skills)

    response = openai_api.generate_job_recommendations(skills)
    return JSONResponse(content=response)

