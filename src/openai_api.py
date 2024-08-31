from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

def generate_job_recommendations(skills):
    completion = client.chat.completions.create(
        model="gpt-4o",
        response_format= { "type": "json_object" },
        messages=[
            {
                "role": "system",
                "content": """
you will give me a list of 5-10 job recommendations based on skills of a person, the response should be in a JSON format, for example:

skills: python, machine learning, data science
{"job_recommendations": ["data scientist", "machine learning engineer", "python developer", "data analyst", "data engineer", "software engineer", "research scientist", "ai engineer", "ai researcher", "ai scientist"]}
"""
            },
            {
                "role": "user",
                "content": f"skills: {skills}"
            }
        ]
    )

    response = completion.choices[0].message.content
    response = json.loads(response)
    return response

def generate_job_role_details(job_role):
    completion = client.chat.completions.create(
        model="gpt-4o",
        response_format= { "type": "json_object" },
        messages=[
            {
                "role": "system",
                "content": """
for a particular job role, provide its description, avg salary, 3 recommended youtube video titles, 3 recommended books, name of 4 famous personalities in that field, and 3 recommended online courses, the response should be in a JSON format, for example:

job_role: data scientist
{
    "job_role_details": {
        "description": "Data scientists are big data wranglers, gathering and analyzing large sets of structured and unstructured data. They need to analyze, process, and model data then interpret the results to create actionable plans for companies and other organizations. Data scientists are analytical experts who utilize their skills in both technology and social science to find trends and manage data. They use industry knowledge, contextual understanding, skepticism of existing assumptions - to uncover solutions to business challenges.", 
        "avg_salary": "$120,000", 
        "youtube_videos": [
            {
                "title": "video1",
            },
            {
                "title": "video2",
            },
            {
                "title": "video3",
            }
        ], 
        "books": [
            {
                "title": "book1",
                "author": "author1"
            },
            {
                "title": "book2",
                "author": "author2"
            },
            {
                "title": "book3",
                "author": "author3"
            }
        ], 
        "famous_personalities": [
            {
                "name": "person1",
                "profile": "profile1"
            },
            {
                "name": "person2",
                "profile": "profile2"
            },
            {
                "name": "person3",
                "profile": "profile3"
            },
            {
                "name": "person4",
                "profile": "profile4"
            }
        ], 
        "online_courses": [
            {
                "name": "course1",
                "link": "link1"
            },
            {
                "name": "course2",
                "link": "link2"
            },
            {
                "name": "course3",
                "link": "link3"
            }
        ]
    }
}
"""
            },
            {
                "role": "user",
                "content": f"job_role: {job_role}"
            }
        ]
    )

    response = completion.choices[0].message.content
    response = json.loads(response)
    return response