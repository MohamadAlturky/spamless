import questionary

BRAND_COLOR = "bold magenta"
SECONDARY_COLOR = "cyan"
MUTED_COLOR = "dim white"
SUCCESS_STYLE = "bold green"
ERROR_STYLE = "bold red"
PANEL_BORDER = "bright_magenta"
RULE_STYLE = "magenta"

QUESTIONARY_STYLE = questionary.Style(
    [
        ("qmark", "fg:#c678dd bold"),
        ("question", "fg:#ffffff bold"),
        ("pointer", "fg:#56b6c2 bold"),
        ("highlighted", "fg:#56b6c2 bold"),
        ("answer", "fg:#c678dd bold"),
        ("selected", "fg:#98c379"),
        ("instruction", "fg:#5c6370 italic"),
        ("separator", "fg:#5c6370"),
    ]
)
