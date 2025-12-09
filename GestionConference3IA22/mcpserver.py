import sys
sys.path.append(r"C:\Users\USER\Desktop\django_correction\WorkshopDjango2526-3IA2\GestionConference3IA22")
import os
import django
from mcp.server.fastmcp import FastMCP
from asgiref.sync import sync_to_async

# Initialize Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestionConference3IA2.settings")
django.setup()

# Import Django models after setup
from ConferenceApp.models import Conference
from SessionApp.models import Session

# Create an MCP server
mcp = FastMCP("Conference Assistant")


# Décorateur pour définir un outil MCP exécutable de manière asynchrone
@mcp.tool()
async def list_conferences() -> str:
    """List all available conferences."""

    # Fonction interne synchrone pour récupérer les conférences (appelée via sync_to_async)
    @sync_to_async
    def _get_conferences():
        return list(Conference.objects.all())

    # Appel asynchrone pour obtenir les données
    conferences = await _get_conferences()

    if not conferences:
        return "No conferences found."

    # Construction de la chaîne de texte
    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date})"
        for c in conferences
    ])
@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Get details of a specific conference by name."""

    @sync_to_async
    def _get_conference():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"

    conference = await _get_conference()

    if conference == "MULTIPLE":
        return (
            f"Multiple conferences found matching '{name}'. "
            "Please be more specific."
        )

    if not conference:
        return f"Conference '{name}' not found."

    return (
        f"Name: {conference.name}\n"
        f"Theme: {conference.get_theme_display()}\n"
        f"Location: {conference.location}\n"
        f"Dates: {conference.start_date} to {conference.end_date}\n"
        f"Description: {conference.description}"
    )

@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """List sessions for a specific conference."""

    @sync_to_async
    def _get_sessions():
        try:
            conference = Conference.objects.get(name__icontains=conference_name)
            return list(conference.sessions.all()), conference
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None

    # Run database lookup asynchronously
    result, conference = await _get_sessions()

    # Handle edge cases
    if result == "MULTIPLE":
        return (
            f"Multiple conferences found matching '{conference_name}'. "
            "Please be more specific."
        )

    if conference is None:
        return f"Conference '{conference_name}' not found."

    sessions = result

    if not sessions:
        return f"No sessions found for conference '{conference.name}'."

    # Build session list
    session_list = []
    for s in sessions:
        session_list.append(
            f"- {s.title} ({s.start_time} - {s.end_time}) in {s.room}\n"
            f"  Topic: {s.topic}"
        )

    return "\n".join(session_list)
@mcp.tool()
async def filter_conferences_by_theme(theme: str) -> str:
    """Filter conferences by theme keyword."""
    
    @sync_to_async
    def _get_filtered_conferences():
        return list(Conference.objects.filter(theme__icontains=theme))

    conferences = await _get_filtered_conferences()

    if not conferences:
        return f"No conferences found with theme containing '{theme}'."

    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date})"
        for c in conferences
    ])
from datetime import datetime

@mcp.tool()
async def filter_conferences_by_date(start_date: str) -> str:
    """
    Filter conferences that start on or after a given date (format: YYYY-MM-DD).
    """
    
    try:
        date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."

    @sync_to_async
    def _get_filtered_conferences():
        return list(Conference.objects.filter(start_date__gte=date_obj))

    conferences = await _get_filtered_conferences()

    if not conferences:
        return f"No conferences starting on or after {start_date}."

    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date})"
        for c in conferences
    ])

# Launch the server
if __name__ == "__main__":
    mcp.run(transport="stdio")

