from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.template import RequestContext
from core.decorators import only_post
from core.models import *
from core.services import comment_services, watch_services

__author__ = 'tony'

@login_required
@only_post
def addIssueComment(request):
    issue_id = int(request.POST['issue_id'])
    comment_content = request.POST['content']
    watch_services.watch_issue(request.user, issue_id, Watch.COMMENTED)
    issue = comment_services.add_comment_to_issue(issue_id, comment_content, request.user)
    return redirect(issue.get_view_link())


@login_required
@only_post
def editIssueComment(request):
    comment_id = int(request.POST['comment_id'])
    comment_content = request.POST['content']
    comment = comment_services.edit_comment_of_issue(comment_id, comment_content, request.user)
    return redirect(comment.issue.get_view_link())


def viewIssueCommentHistory(request, comment_id):
    comment = IssueComment.objects.get(pk = comment_id)
    comment_events = IssueCommentHistEvent.objects.filter(comment__id = comment_id).order_by("eventDate")
    return render(request, 'core2/comment_history.html',
        {'comment':comment,
         'comment_events':comment_events,})
