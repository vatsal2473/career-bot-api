from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src import openai_api, google_api
from pydantic import BaseModel


router = APIRouter()

class jobRoleDetails(BaseModel):
    job_role: str


@router.post("/job_role_details")
async def job_role_details(request: jobRoleDetails):
    
    job_role = request.job_role
    
    response = openai_api.generate_job_role_details(job_role)
    response = google_api.generate_links(response)

    return JSONResponse(content=response)
