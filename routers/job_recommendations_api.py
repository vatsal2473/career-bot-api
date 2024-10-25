from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src import openai_api
from pydantic import BaseModel


router = APIRouter()

class jobRecommendations(BaseModel):
    skills: list

class newJobRecommendations(BaseModel):
    previous_recommendations: list

@router.post("/job_recommendations")
async def job_recommendations(request: jobRecommendations):
    
    skills = request.skills
    skills = ', '.join(skills)

    response = openai_api.generate_job_recommendations(skills)
    return JSONResponse(content=response)


@router.post("/new_job_recommendations")
async def new_job_recommendations(request: newJobRecommendations):
    
    previous_recommendations = request.previous_recommendations
    previous_recommendations = ', '.join(previous_recommendations)
    response = openai_api.generate_new_job_recommendations(previous_recommendations)
    return JSONResponse(content=response)