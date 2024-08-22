from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import job_recommendations_api, job_role_details_api
import uvicorn

app = FastAPI()

# add cors allow all
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_recommendations_api.router)
app.include_router(job_role_details_api.router)

@app.get("/")
def read_root():
    return {"status": True, "message": "API is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)