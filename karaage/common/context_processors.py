# Copyright 2007-2013 VPAC
#
# This file is part of Karaage.
#
# Karaage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Karaage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Karaage  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings

from karaage.applications.models import Application, ProjectApplication
from django.db.models import Q


def common(request):
    """ Set context with common variables. """
    ctx = {}
    ctx['GRAPH_URL'] = settings.GRAPH_URL
    ctx['org_name'] = settings.ACCOUNTS_ORG_NAME
    ctx['accounts_email'] = settings.ACCOUNTS_EMAIL
    ctx['base_url'] = '%s' % request.META.get('SCRIPT_NAME', '')
    return ctx


def registration(request):
    """ Set context for registration menu. """
    ctx = {}
    if request.user.is_authenticated():
        person = request.user
        my_applications = ProjectApplication.objects.filter(
            applicant=person).exclude(
            state__in=[Application.COMPLETED, Application.ARCHIVED, Application.DECLINED]).count()

        query = Q(project__in=person.leaders.all(), state=Application.WAITING_FOR_LEADER)
        query = query | Q(institute__in=person.delegate.all(), state=Application.WAITING_FOR_DELEGATE)

        project_applications = ProjectApplication.objects.filter(query).count()
        ctx['pending_applications'] = my_applications + project_applications
    return ctx


def admin(request):
    """ Set context for admin menu. """
    ctx = {}
    ctx['pending_applications'] = Application.objects.filter(
            state=Application.WAITING_FOR_ADMIN).count()
    return ctx