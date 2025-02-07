import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to logging.DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Create a global logger instance
logger = logging.getLogger(__name__)
