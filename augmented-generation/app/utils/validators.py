import re

def sanitize_input(text):
    """Sanitize user input to prevent XSS and other issues."""
    if not text:
        return text
    # Remove any potentially dangerous characters
    sanitized = re.sub(r'[<>]', '', text)
    sanitized = re.sub(r'^\"{1,2}|\'{1,2}$', '', sanitized)
    sanitized = re.sub(r'[\x00-\x1F\x7F]', '', sanitized)
    sanitized = re.sub(r'(?:\b(?:script|alert|eval)\b)', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    return sanitized.strip()


def validate_prompt(prompt):
    """Validate prompt length and content."""
    if not prompt:
        return False, "Prompt is required"

    if len(prompt) > 1000:
        return False, "Prompt too long, maximum 1000 characters"
    if len(prompt) < 5:
        return False, "Prompt too short, minimum 10 characters"

    return True, "Valid prompt"
