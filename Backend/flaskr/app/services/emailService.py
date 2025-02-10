from ...config.dbSetup import mysql
from ...config.dbSetup import chroma_client
from ...config.logger import logger
from ...config.llmConfig import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_community.document_loaders import WebBaseLoader
from ...utils.clean_text import clean_text


def scrape_website(url_input):
    try:
        loader = WebBaseLoader([url_input])
        raw_content = loader.load().pop().page_content
        data = clean_text(raw_content)
        return data
    except Exception as e:
        logger.error(f"Error scraping website {url_input}: {e}")
        return None


def query_vectorDB(id, skills):
    collection = chroma_client.get_collection(id)
    if not collection or not skills:
        return None
    skills = ",".join(skills)
    return collection.query(query_texts=skills, n_results=2).get("metadatas", [])


def extract_jobs(cleaned_text):
    prompt_extract = PromptTemplate.from_template(
        """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `responsibilities`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
    )
    chain_extract = prompt_extract | llm
    res = chain_extract.invoke(input={"page_data": cleaned_text})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(res.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")

    return [res]


def write_email(job, links, name, background, technicalSkills):
    prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCIPTION:
        {job_description}

        ### ROLE:
        You are {user_name}

        ### BACKGROUND:
        {user_background}

        ### TECHNICAL SKILLS:
        {user_technical_skills}
        
        ### PROJECTS:
        {link_list}.

        ### TASK:
        Write a personalized and professional cold email tailored to the client, addressing their job description and highlighting your relevant skills, experience, and projects. Include the project link if it exists. 

        The email should be less than 40 lines, directly addressing the job description and client’s requirements. Use a professional, persuasive tone with no preamble or unnecessary content. Ignore the things from the job descrption that you don't have experience with. It should include a signoff

        
        ### **Email Template (NO PREAMBLE)**:
        """
    )
    chain_email = prompt_email | llm
    res = chain_email.invoke(
        {
            "job_description": str(job),
            "link_list": links,
            "user_name": name,
            "user_background": background,
            "user_technical_skills": technicalSkills,
        }
    )
    return res.content
