def validate_city(city: str) -> str:
    """Валидация названия города."""
    if not city or not all(word.isalpha() for word in city.split()):
        raise ValueError("City name must be a non-empty string of alphabetic characters.")
    return " ".join(word.title() for word in city.split())
