# Copyright 2007-2010 VPAC
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

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import datetime

from karaage.requests.models import ProjectCreateRequest
from karaage.projects.utils import add_user_to_project
from karaage.requests.forms import ProjectRegistrationForm
from karaage.util import log_object as log
from karaage.util.email_messages import send_project_request_email, send_project_approved_email, send_project_rejected_email


def project_registration(request):
    """
    This is for a new user wanting to start a project
    """
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)

        if form.is_valid():
            project_request = form.save()

            # Send email to Institute Delegate for approval
            send_project_request_email(project_request)
            return HttpResponseRedirect(reverse('project_created', args=[project_request.id]))
    else:     
        form = ProjectRegistrationForm()

    return render_to_response('requests/project_request_form.html', { 'form': form, }, context_instance=RequestContext(request))


def project_created(request, project_request_id):
    project_request = get_object_or_404(ProjectCreateRequest, pk=project_request_id)
    project = project_request.project
    person = project_request.person
    
    log(person.user, project, 1, 'Requested project for approval')
    
    return render_to_response('requests/project_created.html', locals(), context_instance=RequestContext(request))


@login_required
def approve_project(request, project_request_id):
    project_request = get_object_or_404(ProjectCreateRequest, pk=project_request_id)
    project = project_request.project
    institute = project.institute
    project_leaders = project.leaders.all()

    # Make sure the request is coming from the institutes' delegate
    if not request.user == institute.delegate.user:
        if not request.user == institute.active_delegate.user:
            return HttpResponseForbidden('<h1>Access Denied</h1>')
    
    project.activate()

    log(request.user, project, 2, 'Approved Project')
    for leader in project_leaders:
        messages.info(request, "Project approved successfully and a notification email has been sent to %s" % leader)

        if not leader.user.is_active:
            leader.activate()
        
        if project_request.needs_account:
            add_user_to_project(leader, project)
 
    send_project_approved_email(project_request)    
    project_request.delete()

    return HttpResponseRedirect(reverse('kg_user_profile'))


@login_required
def reject_project(request, project_request_id):
    project_request = get_object_or_404(ProjectCreateRequest, pk=project_request_id)
    project = project_request.project
    institute = project.institute
    project_leaders = project.leaders.all()

    # Make sure the request is coming from the institutes delegate
    if not request.user == institute.delegate.user:
        if not request.user == institute.active_delegate.user:
            return HttpResponseForbidden('<h1>Access Denied</h1>')

    send_project_rejected_email(project_request)

    log(request.user, project, 2, 'Rejected Project')
    for leader in project_leaders:
        messages.info(request, "Project rejected and a notification email has been sent to %s" % leader)
    
    project_request.delete()
    project.delete()
    for leader in project_leaders:
        if not leader.user.is_active:
            leader.delete()
            user.delete()

    return HttpResponseRedirect(reverse('kg_user_profile'))

    
@login_required
def request_detail(request, project_request_id):
    project_request = get_object_or_404(ProjectCreateRequest, pk=project_request_id)

    project = project_request.project
    person = project_request.project.leaders.all()[0]

    # Make sure the request is coming from the institutes delegate
    if not request.user == project.institute.delegate.user:
        if not request.user == project.institute.active_delegate.user:
            return HttpResponseForbidden('<h1>Access Denied</h1>')

    
    return render_to_response('requests/project_request_detail.html', locals(), context_instance=RequestContext(request))

    
