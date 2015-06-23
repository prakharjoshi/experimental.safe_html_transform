# -*- coding: utf-8 -*-
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName


def isNotCurrentProfile(context):
    return context.readDataFile('experimentalsafehtmltransform_marker.txt') is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return
    # Do something during the installation of this package
    site = context.getSite()
    installPortalTransforms(site)


def updateSafeHtml(out, portal):
    print >> out, 'Update safe_html...'
    safe_html_id = 'safe_html'
    safe_html_module = "Products.PortalTransforms.transforms.safe_html"
    experimental_safe_html_id = 'experimental_safe_html'
    experimental_safe_html_module = 'experimental.safe_html_transform.safe_html'
    pt = getToolByName(portal, 'portal_transforms')
    for id in pt.objectIds():
        transform = getattr(pt, id)
        if transform.id == safe_html_id and \
                transform.module == safe_html_module:
            try:
                transform.get_parameter_value('disable_transform')
            except KeyError:
                print >> out, '  replace safe_html (%s, %s) ...' % (
                    transform.name(), transform.module)
                try:
                    pt.unregisterTransform(id)
                    pt.manage_addTransform(experimental_safe_html_id, experimental_safe_html_module)
                except:
                    raise
                else:
                    print >> out, '  ...done'

    print >> out, '...done'


def installPortalTransforms(portal):
    out = StringIO()
    updateSafeHtml(out, portal)
