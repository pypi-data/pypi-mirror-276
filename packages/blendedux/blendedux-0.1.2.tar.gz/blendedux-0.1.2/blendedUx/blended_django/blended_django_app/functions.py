from __future__ import absolute_import 
import os
import json
import math
import sys
import jinja2

from os.path import relpath

import hashlib

from blended.jinjaenv import BlendedEnvironment
from blended.functions import builtins as context_functions
from django import template
from blended.djangotags.loader import template_from_string
from blended_django.blended_django_app.transform import image as get_image_path
from blended_django.blended_django_app.helpers import ROOT_DIR, IMAGE_CACHE_DIR, COMPILE_DIR, BLENDED_DIR, SRC, CURRENT_ACCOUNT, BASE_DIR
from blended_django.blended_hostlib.controller import Controller
from blended_django.blended_hostlib.backend import FileSystemBackend
from blended_django.blended_hostlib.network import Network
from blended_django.blended_hostlib.exceptions import BlendedException
from django.template import Context, Template, Library


try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin


src = os.path.join(BLENDED_DIR, SRC)


#width x height

def image(image_dict_obj, height=None, width=None, filters=None):
    """
    """
    if filters:
        if ((height == 0) or height) and ((width == 0) or width):
            pass
        elif not (height and width):
            print("Please pass height and width before using filters! error in:%s)" % image_dict_obj)
            sys.exit(0)
    elif height or width:
        filters = 'series(fill, crop(smart))'
    else:
        pass
    try:
        if height:
            float(height)
        if width:
            float(width)
    except ValueError:
        raise BlendedException(
            "Please pass numerical value of height and width before using filters. Default values are (0, 0)! error in:%s)" % image_dict_obj)
        sys.exit(0)
    try:
        relative_path = image_dict_obj.get('path')
        output = get_image_path(relative_path, height=height, width=width, filters=filters)
        url = '/media/%s' % (relpath(output, IMAGE_CACHE_DIR))
    except jinja2.exceptions.UndefinedError as exc:
        filename = exc.message.rsplit('attribute ')[1].replace("'", "")
        url = '/media/not_found/%s' % (filename)
    return url


def theme_data(theme_object, block, template):
    """
    using block and theme template,
    generates a dictionary that returns correct grid values from the theme object
    """
    template =  '%s.html' % template
    grid_all = theme_object['theme']['meta']['grid']['all']
    block_all = theme_object['theme']['meta']['grid']['templates'][template]['all']
    block_dict = theme_object['theme']['meta']['grid']['templates'][template]['blocks'][block]
    grid_all.update(block_all)
    grid_all.update(block_dict)
    return grid_all



def nav_links(theme, template_name):
    """
    :param theme:
    :return:
    """
    blended_dir = BLENDED_DIR
    current_account = theme.get('current_account')
    account = theme.get('account')
    path = theme.get('theme_path')
    theme_name = theme.get('theme_name')
    account_path = os.path.join(blended_dir, current_account)
    relative_path = path.split(account_path)[1]
    if relative_path.startswith(os.sep):
        relative_path = relative_path.split(os.sep, 1)[1]
    if relative_path.endswith('lib'):
        relative_path = '%s/%s' % (relative_path, account)
    url = '/preview/%s/%s/templates/%s' % (relative_path, theme_name, template_name)
    return url

def generate_css_links(theme_object):
    """
    function to generate css file path dynamically.
    """
    
    blended_dir = BLENDED_DIR
    urls = []
    network = Network()
    backend = FileSystemBackend()# does backend take's compile directory path to initialize just for save_css call?
    current_account = CURRENT_ACCOUNT
    backend.directory_path = os.path.join(blended_dir, current_account)
    controller = Controller(network, backend)
    theme_name = theme_object.get('theme_name')
    css_path = theme_object.get('meta', {}).get('css', {})
    source_path = css_path.get('source', '')
    rendered_require = css_path.get('render_required')
    #compile_files = css_path.get('compile_targets')
    context = {'theme': dict(theme_object)}
    
    compiled_path = os.path.join(COMPILE_DIR, 'css')

    for css_path in source_path:
        css_path = os.path.relpath(css_path)
        if css_path.endswith('.css'):
            css_file_path = css_path.rsplit('.css', 1)[0]
            splited_source_path = css_file_path.split(os.sep)
        else:
            splited_source_path = css_path.split(os.sep)

        if len(splited_source_path) > 0:
            css = content_at_source(splited_source_path, theme_object)

        if not css:
            try:
                #which directory will backend get initialize for ?
                if css_path.endswith('.css'):
                    css_file_path = css_path.rsplit('.css', 1)[0]
                    splited_source_path = css_file_path.split(os.sep)
                else:
                    splited_source_path = css_path.split(os.sep)
                theme_slug = splited_source_path.pop(0)
                try:
                    dependent_theme_object = controller.get_package(theme_slug, 'context')
                except (IOError, OSError):
                    print("failure in reading css from path %s" % (css_path))
            except BlendedException as exc:
                raise BlendedException(exc)
            css = content_at_source(splited_source_path, dependent_theme_object)
        
        if isinstance(css, str):
            file_path = os.path.join(compiled_path, css_file_path.rsplit(os.sep, 1)[-1])
            if(rendered_require):
                css = render_code(css, context)
            try:
                path = backend.save_css(file_path, css)
            except BlendedException as exc:
                raise BlendedException(exc)
            else:
                # split_path = path.split(os.path.join(BASE_DIR, "my_project"))
                split_path = path.split(COMPILE_DIR)
                # breakpoint()
                css_file_url ='static'+split_path[1]
                urls.append(css_file_url)
        else:
            urls = read_css_directory(css, compiled_path, rendered_require, urls, backend, context)
    # breakpoint()
    
    return urls

def read_css_directory(css, compiled_path, rendered_require, urls, backend, context):
    """
    :param css:
    :param compile_path:
    :param rendered_require:
    :param urls:
    :return:
    """
    for each_file, file_content in css.items():
        file_path = os.path.join(compiled_path, each_file)
        if isinstance(file_content, dict):
            urls = read_css_directory(file_content, file_path, rendered_require, urls, backend, context)
        if (rendered_require):
            # css_content = env.from_string(file_content)
            file_content = render_code(file_content, context)

        try:
            path = backend.save_css(file_path, file_content)
        except BlendedException as exc:
            raise BlendedException(exc)
        else:
            split_path = path.split(COMPILE_DIR)
            css_file_url = split_path[1]
            urls.append(css_file_url)
    return urls

# def render_code(file_content, context):
#     #return  file_content
#     """
#     :param file_content: compiled template content
#     :param context: theme_object or context
#     :return: rendered content of template.
#     """
    
#     template = template_from_string(file_content)
#     context.update({'image': image,
#                    'css_links': generate_css_links,
#                    'theme_data': theme_data,
#                    'nav_links': nav_links,
#                    'home': blended_home,
#                    'hash': blended_hash})
#     context.update(context_functions())
#     context = Context(context)
#     return template.render(context)

def render_code(file_content, context):
    template = env.from_string(file_content)
    return template.render(context)

def content_at_source(splited_path_list, theme_object, directory_file={}):
    """
    :param splited_path_list:
    :param theme_object:
    :param directory_file:
    :return: directory_file
    """
    while(splited_path_list):
        index_value = splited_path_list.pop(0)
        theme_data = theme_object.get(index_value, {})
        if len(splited_path_list) > 0:
            directory_file = content_at_source(splited_path_list, theme_data, directory_file)
        else:
            if isinstance(theme_data, str):
                directory_file = theme_data
            else:
                directory_file.update(theme_data)

    return directory_file

def blended_hash(layout, prefix=None) :
    if layout :
        try:
            hash_value = hashlib.md5(repr(layout).encode('utf-8')).hexdigest()
            if prefix:
                prefix = prefix.replace(" ", "_")
                if prefix[0].isalpha() or prefix[0]=='_':
                    hash_value =prefix+hash_value
                else:
                    hash_value = "Prefix must start with 'alphabat' or '_'"
            else:
                hash_value ="layout_"+hash_value
        except Exception as e:
            hash_value = e
        return hash_value

def blended_home():
    """
    """
    return ''
    #return blended_urls.urlList[-1]

register = Library()
register.tag('image', image)
register.tag('theme_data', theme_data)   # change from media
register.tag('nav_links', nav_links)     # change from media
register.tag('css_links', generate_css_links)
register.tag('home', blended_home)
register.tag('hash', blended_hash)


env = BlendedEnvironment()
from blended.functions import blendedround
env.globals.update({
                    'css_links': generate_css_links,
                    'nav_links': nav_links,
                    'image': image,
                    'home': blended_home,
                    'theme_data':theme_data,
                    'hash': blended_hash
                    })
