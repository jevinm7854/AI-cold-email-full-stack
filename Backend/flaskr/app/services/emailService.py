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


def extract_jobs(cleaned_text):
    prompt_extract = PromptTemplate.from_template(
        """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
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
    return res if isinstance(res, list) else [res]
