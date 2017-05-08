import json
import logging

from datetime import (date, timedelta)

from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from .models import (
    BuildConfig,
    Environment,
    Language,
)

from .common import (
    _get_or_create_environment_objects,
    _get_or_create_language_objects,
    _get_date_by_day,
    _query_api,
)

if settings.DEBUG:
    logger = logging.getLogger('dashboard')
else:
    logger = logging.getLogger('dashboard_prod')

def _populate_build_config_objects(endpoints=settings.OPENSHIFT_API):
    """Populate daily Build Configs and Language objects in the database.
    
    The intent is to do this daily, to get a historical record."""

    choices =  _get_or_create_environment_objects()

    for key in endpoints.keys():
        response = _query_api(
            master_url=endpoints[key]['OPENSHIFT_MASTER'],
            api_token=endpoints[key]['API_TOKEN'],
            endpoint=endpoints[key]['build_endpoint'])

        if response:
            r_dict = response.json()
            for ea_bc in r_dict['items']:
                environment = choices.get(key, '')
                name=ea_bc['metadata']['name']
                namespace=ea_bc['metadata']['namespace']
                build_config=ea_bc['spec']

                try:
                    bc = BuildConfig()
                    bc.environment = environment
                    bc.name = name
                    bc.namespace = namespace
                    bc.build_config = build_config
                    bc.clean_fields()
                    
                    # Setup language object
                    logger.info(bc.build_config['strategy']['sourceStrategy']['from']['name'])
                    bc.language, bc.lang_created = _get_or_create_language_objects(bc.build_config['strategy']['sourceStrategy']['from']['name'])
                    logger.info('{}:{}'.format(bc.language, bc.lang_created))

                    # Setup BuildConfig object
                    today = date.today()
                    obj, created = BuildConfig.objects.get_or_create(
                        environment=bc.environment,
                        namespace=bc.namespace,
                        name=bc.name,
                        last_seen=today,
                        defaults={
                            'build_config': bc.build_config,
                            'language': bc.language,
                        })

                    logger.info('{}:{}'.format(obj, created))

                except KeyError as e:
                    logger.error('{}:KeyError:{}:{}:{}:{}'.format(bc.environment, e, bc.namespace, bc.name, bc.build_config))
                except ValidationError as e:
                    logger.error('{}:ValidationError:{}:{}:{}'.format(bc.environment, e, bc.namespace, bc.name))

def _find_latest_bc_query(today=None, start=0, end=4, env=None, lang=None):
    """ Look back 5 days, if nothing return zero """

    if not today:
        today = date.today()

    if not lang or not env:
        return None 
    elif start == end:
        return None 

    count = 0

    for n in range(start, end):
        which_day=today - timedelta(days=n)
        count = BuildConfig.objects.filter(environment=env).filter(language=lang).filter(last_seen=which_day).count()
        if count:
            break

    return count

def get_image_counts(request, response_type='json', day=None):
    '''Get most recent image counts.  Try today, if empty go back 5 days'''
    
    l = [language for language in Language.objects.all()]
    e = [environment for environment in Environment.objects.all()]

    # Set initial values
    d = {'total_all': 0} 
    for lang in l:
        d['total_{}'.format(lang.language)] = 0
    for env in e:
        d[env.environment] = {'total_all': 0}

    if day:
        new_date = _get_date_by_day(int(day))
        logger.info(new_date)

    if not day or new_date:
        # Loop through envionments
        for env in e:
            for lang in l:
                # default is to look back 5 days, and get a day that has the image
                if day:
                    count = _find_latest_bc_query(today=new_date,start=0, end=1, env=env, lang=lang)
                else:
                    count = _find_latest_bc_query(env=env, lang=lang)
    
                if count:
                    d[env.environment][lang.language] = count
                    d['total_{}'.format(lang.language)] += count # add to totals
                    d[env.environment]['total_all'] += count
                    d['total_all'] += count

    logger.info(d)

    if response_type == 'json':
        return JsonResponse(d)
    else:
        template_name = 'dashboard/display_html.html'
        context = {
            'data': d,
        }

        return render(request, template_name, context)
        

# vim: ai et ts=4 sts=4 sw=4 nu
