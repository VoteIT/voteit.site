""" Fanstatic lib"""
from fanstatic import Library
from fanstatic import Resource

from voteit.core.fanstaticlib import voteit_main_css


voteit_site_lib = Library('voteit_site', 'static')

voteit_site = Resource(voteit_site_lib, 'styles.css', depends=(voteit_main_css,))
