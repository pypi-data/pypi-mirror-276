from kozmo_ai.services.teams.config import TeamsConfig
import requests


def send_teams_message(
    config: TeamsConfig,
    message: str,
    title: str = 'Kozmo pipeline run status logs',
) -> None:
    requests.post(
        url=config.webhook_url,
        json={
            'summary': title,
            'sections': [{
                'activityTitle': title,
                'activitySubtitle': message,
            }],
        },
    )
