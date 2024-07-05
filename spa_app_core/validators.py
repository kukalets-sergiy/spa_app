from django.core.validators import RegexValidator


alphanumeric = RegexValidator(r"^[\w]*$", "This field can contain only numbers, letters, and underscores.")

phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
)
