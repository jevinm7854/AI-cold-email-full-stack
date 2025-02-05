from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, HttpUrl
import chromadb
from fastapi import Request
from typing import List, Optional

app = FastAPI()

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create or get a collection
# collection = chroma_client.get_or_create_collection(name="my_collection")


class Project(BaseModel):
    description: str
    techStack: str
    portfolio: Optional[HttpUrl] = None


class Profile(BaseModel):
    name: str
    email: EmailStr
    background: str
    projects: List[Project]


@app.post("/profile")
async def add_profile(profile: Profile):

    try:

        collection = chroma_client.get_or_create_collection(name="my_collection")
        docs = [project.description for project in profile.projects]
        metadata = [
            {"techStack": project.techStack, "portfolio": str(project.portfolio)}
            for project in profile.projects
        ]
        ids = [f"proj_{i}" for i in range(len(profile.projects))]
        collection.add(documents=docs, ids=ids, metadatas=metadata)

        return {"success": "true"}

    except:
        return {"success": "false"}
