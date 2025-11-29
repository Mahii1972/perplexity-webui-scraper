from os import getenv

from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live
from rich.panel import Panel

from perplexity_webui_scraper import CitationMode, Models, Perplexity, SearchFocus, SourceFocus, TimeRange

load_dotenv()

console = Console()

# Try full cookies first, fall back to session token
cookies = getenv("PERPLEXITY_COOKIES")
token = getenv("PERPLEXITY_SESSION_TOKEN")

if cookies:
    print(f"Using full cookies string ({len(cookies)} chars)")
    client = Perplexity(cookies=cookies)
elif token:
    print(f"Using session token ({len(token)} chars)")
    client = Perplexity(session_token=token)
else:
    print("Error: No PERPLEXITY_COOKIES or PERPLEXITY_SESSION_TOKEN found in .env")
    exit(1)

# Define the query
query = "Explain in a simplified and easy-to-understand way what a chatbot is."

# Configure the prompt request with all available parameters
prompt_config = client.prompt(
    query=query,  # The question to ask
    files=None,  # Optional: file path(s) to attach (single path or list, max 30 files, 50MB each)
    citation_mode=CitationMode.DEFAULT,  # Citation format: DEFAULT, MARKDOWN, or CLEAN
    model=Models.BEST,  # AI model to use (BEST, GPT5, CLAUDE45_SONNET, etc.)
    save_to_library=False,  # Whether to save this query to your library
    search_focus=SearchFocus.WEB,  # Search focus: WEB or WRITING
    source_focus=SourceFocus.WEB,  # Source type(s): WEB, ACADEMIC, SOCIAL, FINANCE (can be a list)
    time_range=TimeRange.ALL,  # Time filter: ALL, TODAY, LAST_WEEK, LAST_MONTH, LAST_YEAR
    language="en-US",  # Language code (e.g., "en-US", "pt-BR")
    timezone=None,  # Timezone code (e.g., "America/New_York", "America/Sao_Paulo")
    coordinates=None,  # Location coordinates as tuple: (latitude, longitude)
)

# Blocking mode (waits for complete response)
try:
    response = prompt_config.run()
    print(f"\n=== RESPONSE DEBUG ===")
    print(f"Title: {response.title}")
    print(f"Answer: {response.answer}")
    print(f"Conversation UUID: {response.conversation_uuid}")
    print(f"Search Results: {response.search_results}")
    print(f"Raw Data: {response.raw_data}")
    print(f"======================\n")
    console.print(Panel(f"[bold green]Answer:[/bold green] {response.answer}", border_style="green"))
except Exception as e:
    print(f"\n=== ERROR DEBUG ===")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    import traceback
    traceback.print_exc()
    print(f"===================\n")
