""" Blended Context 
"""
from django.http import HttpRequest
from blended.functions import builtins
from blended_django.blended_hostlib.backend import FileSystemBackend
from blended_django.blended_hostlib.network import Network
from blended_django.blended_hostlib.controller import Controller
from blended_django.blended_django_app.functions import  *
from blended.djangotags.loader import template_from_string
from blended_django.blended_django_app.helpers import IMAGE_CACHE_DIR, BLENDED_DIR, CURRENT_ACCOUNT, PACKAGE_NAME
from django.template import Library, Context, RequestContext, Variable, TemplateSyntaxError

from blended_django.blended_django_app.functions import render_code


def get_context(request):
    
    # Media Cache Dir
    if not os.path.exists(IMAGE_CACHE_DIR):
        os.makedirs(IMAGE_CACHE_DIR)

    network = Network()
    #network, user_pk = manage_session_key(None, None, network)
    current_account = CURRENT_ACCOUNT
    blended_dir = BLENDED_DIR
    current_dir = os.path.join(blended_dir, current_account)

    backend = FileSystemBackend(
        current_dir, blended_dir=blended_dir,
        current_account=current_account, blended_directory_path=blended_dir)
    controller = Controller(network, backend)
    # dynamically built package_name
    packageName = "%s/%s"%(CURRENT_ACCOUNT,PACKAGE_NAME)
    
    theme_obj = controller.get_package(package_name=packageName, format='context')
    
    
    context = {'theme': theme_obj,
               'css_links': generate_css_links,
               'image': image,
               'theme_data': theme_data,
               'nav_links': nav_links,
               'hash': blended_hash,
               'home': blended_home}
    context.update(builtins())
    
    # breakpoint()
    
    return context
