# -*- coding: utf-8 -*-
import pkgutil
import logging
from Products.CMFCore.utils import getToolByName
# from .mimetypes import registerMimeTypes
import experimental.safe_html_transform


def isNotCurrentProfile(context):
    return context.readDataFile('experimentalsafehtmltransform_marker.txt') is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return
    # Do something during the installation of this package
    installTransform(context)


def installTransform(context, logger=None):
    if logger is None:
        logger = logging.getLogger('experimental.safe_html_transform.safe_html')
    if hasattr(context, 'readDataFile'):
        # Make sure we are working on our add-on
        if isNotCurrentProfile(context):
            return
    else:
        pass
    # registerMimeTypes(context, logger)
    # get the old transform
    pt = getToolByName(context, 'portal_transforms')
    # get name of safe_html transform from our add-on.
    for transforms in [x[1] for x in pkgutil.iter_modules(experimental.safe_html_transform.__path__)
                       if x[1] != 'mimetypes']:
        # check for our transform name in the portal_tranform
        if transforms in pt:
            pt.unregisterTransform(transforms)
            logger.info('Unregistered %s' % transforms)
        if transforms == 'experimental_safe_html':
            pt.manage_addTransform(transforms, 'experimenatal.safe_html_transform.%s' % transforms)
            logger.info('Regstered %s' % transforms)
