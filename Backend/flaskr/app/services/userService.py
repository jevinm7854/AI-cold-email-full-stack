from ...config.dbSetup import mysql
from ...config.dbSetup import chroma_client
from ...config.logger import logger


def createUserDB(name, email, id, background):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO coldEmail.users (id, name, email, background) VALUES (%s, %s, %s, %s)",
            (id, name, email, background),
        )
        logger.info("User created successfully in DB")
        mysql.connection.commit()
        return {"id": id, "message": "User created successfully", "status": 201}
    except Exception as e:
        return {"error": str(e)}



def createUserChroma(id, data):
    try:
        collection = chroma_client.create_collection(name=f"{str(id)}")

        projects = data.get("projects", [])  # Extract projects directly from data

        logger.info(f"Projects: {projects}")

        if not projects:
            logger.warning("No projects found in the request data.")
            return {"message": "No projects to add to ChromaDB"}

        docs = [project.get("description", "") for project in projects]  # Ensure description is not None
        metadata = [
            {
                "techstack": project.get("techStack", ""),  # Default empty string if missing
                "portfolio": str(project.get("portfolio", "")),  # Convert None to empty string
            }
            for project in projects
        ]
        ids = [f"project_{i+1}" for i in range(len(projects))]  # Unique IDs for each project

        collection.add(documents=docs, ids=ids, metadatas=metadata)

        res = chroma_client.list_collections(5)
        logger.info(f"Chroma collections: {res}")
        logger.info("Chroma collection created successfully")

        return {"message": "Chroma collection created successfully", "collection_id": id}

    except Exception as e:
        logger.error(f"Error creating Chroma collection: {e}", exc_info=True)
        return {"error": str(e)}
