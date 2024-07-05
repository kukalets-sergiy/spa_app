import requests
from django.conf import settings

def verify_recaptcha(token):
    recaptcha_secret_key = settings.DRF_RECAPTCHA_SECRET_KEY
    recaptcha_response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': recaptcha_secret_key,
            'response': token
        }
    )
    result = recaptcha_response.json()
    return result.get('success', False)


