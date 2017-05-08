import logging
import requests
from datetime import date

from django.conf import settings
from django.http import JsonResponse

from .models import (
    BuildConfig,
    Environment,
    Language,
)

if settings.DEBUG:
    logger = logging.getLogger('dashboard')
else:
    logger = logging.getLogger('dashboard_prod')

def _get_or_create_environment_objects(openshift_api=settings.OPENSHIFT_API):
    """Populate Environment objects in the database and return dictionary map"""

    choices = {}

    for k in openshift_api.keys():
        obj, created = Environment.objects.get_or_create(environment=k)
        choices[k] = obj
        logger.info('{}, {}'.format(obj, created))

    return choices

def _get_or_create_language_objects(language='Unknown'):

    language_trimmed = language.split(':')[0]
    lang_obj, lang_created = Language.objects.get_or_create(
        language=language_trimmed,
        description=language_trimmed)

    return (lang_obj, lang_created)

def _query_api(
    master_url=settings.OPENSHIFT_API['NP']['OPENSHIFT_MASTER'],
    api_token=settings.OPENSHIFT_API['NP']['API_TOKEN'],
    endpoint='/oapi/v1/buildconfigs'):
    """ Query the API and return response"""

    openshift_api_url = 'https://' + master_url
    openshift_api_get_endpoint = openshift_api_url + endpoint
    bearer_token_header = {'Authorization': 'Bearer ' + api_token }

    try:
        response = requests.get(openshift_api_get_endpoint,headers=bearer_token_header, timeout=2.0)
    except requests.ConnectTimeout as e:
        logger.error(e)
        return None
    except requests.ConnectionError as e:
        logger.error(e)
        return None

    if not response.ok:
       logger.error(response.status_code)
       return None
    else:
        return response

def _get_date_by_day(day=1):

    today = date.today()
    try:
        new_date = today.replace(day=day)
        logger.info(new_date)
        return new_date
    except ValueError as e:
        logger.error(e)
        return

def custom_page_not_found_json_view(request):
    return JsonResponse(status=404, data={'message': 'page not found'})

# vim: ai et ts=4 sts=4 sw=4 nu ru
