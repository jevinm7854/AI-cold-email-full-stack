from ...config.dbSetup import mysql
from ...config.dbSetup import chroma_client
from ...config.logger import logger


def createUserDB(name, email, id, background, technicalSkills):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO coldEmail.users (id, name, email, background, technicalSkills) VALUES (%s, %s, %s, %s, %s)",
            (id, name, email, background, technicalSkills),
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

        docs = [
            project.get("techStack", "") for project in projects
        ]  # Ensure description is not None
        metadata = [
            {
                "description": project.get(
                    "description", ""
                ),  # Default empty string if missing
                "portfolio": str(
                    project.get("portfolio", "")
                ),  # Convert None to empty string
            }
            for project in projects
        ]
        ids = [
            f"project_{i+1}" for i in range(len(projects))
        ]  # Unique IDs for each project

        collection.add(documents=docs, ids=ids, metadatas=metadata)

        res = chroma_client.list_collections(5)
        logger.info(f"Chroma collections: {res}")
        logger.info("Chroma collection created successfully")

        return {
            "message": "Chroma collection created successfully",
            "collection_id": id,
        }

    except Exception as e:
        logger.error(f"Error creating Chroma collection: {e}", exc_info=True)
        return {"error": str(e)}


def getUserDetails(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM coldEmail.users WHERE id = %s", (id,))
        user = cur.fetchone()
        if user:
            return {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "background": user[3],
                "technicalSkills": user[4],
            }
        else:
            return {"message": "User not found"}
    except Exception as e:
        return {"error": str(e)}

def getChromaDetails(id):
    try:
        collection = chroma_client.get_collection(id)
        if collection:
            documents = collection.get()  # Fetch all documents
            return {"message": "Collection found", "documents": documents}
        else:
            return {"message": "Collection not found"}
    except Exception as e:
        return {"error": str(e)}