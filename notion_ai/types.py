from dataclasses import dataclass

@dataclass
class HelpMeWrite:
    prompt: str
    type: str = "helpMeWrite"
    pageTitle: str = ''
    previousContent: str = ''
    restContent: str = ''
