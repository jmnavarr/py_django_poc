from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv

from social.models import Keyword, KeywordsInSocialMedia, SearchResults
from django.utils import timezone
from forms import KeywordsForm

from social.libraries import keywordlib
from django.core.mail import EmailMessage

# /social
@login_required(login_url='/')
def index(request):
    form = KeywordsForm(request.POST or None)
    keywords_list = Keyword.objects.filter(user_id=request.user.id).order_by('-date_added')

    context = {
        'keywords_list': keywords_list,
        'form': form
    }

    return render(request, 'social/keywords.html', context)

# /
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        context = {}
        return render(request, 'social/login.html', context)

# /logout
def logout_view(request):
    logout(request)
    return redirect('login_view')

# /social/process_login
def process_login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user is not None:                # user is authenticated
        login(request, user)
        return redirect('index')
    else:                               # did not authenticate
        return redirect('login_view')

# /social/add_keyword
@login_required(login_url='/')
def add_keyword(request):
    form = KeywordsForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            keyword_record = Keyword(user_id=request.user.id, keyword_text=request.POST['keyword'], date_added=timezone.now())
            keyword_record.save()

            if request.POST.get('reddit', False):
                reddit_record = KeywordsInSocialMedia(keyword_id=keyword_record.id, social_media_type='reddit')
                reddit_record.save()

            if request.POST.get('twitter', False):
                twitter_record = KeywordsInSocialMedia(keyword_id=keyword_record.id, social_media_type='twitter')
                twitter_record.save()

    return redirect('index')

@login_required(login_url='/')
def search(request, keyword_id):
    keywordlib.search(keyword_id)

    return redirect('index')

@login_required(login_url='/')
def searchresults(request):
    searchresults_list = SearchResults.get_search_results_by_user_id(request.user.id)

    context = {
        'searchresults_list': searchresults_list,
    }

    return render(request, 'social/searchresults.html', context)

@login_required(login_url='/')
def get_searchresults_csv(request):
    ids = request.GET.get('ids', '')

    if len(ids) > 0:
        searchresults_list = SearchResults.get_search_results_by_ids_for_user_id(request.user.id, ids)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="searchresults.csv"'

        writer = csv.writer(response)

        writer.writerow(['ID', 'Title', 'Link to Content', 'Social Media Type', 'Date Added'])

        for searchresult in searchresults_list:
            writer.writerow([searchresult['id'], searchresult['title'], searchresult['link_to_content'], searchresult['social_media_type'], searchresult['date_added']])

        email = EmailMessage(
            'Search Results CSV',
            'Search results attached',
            'no-reply@socialmentions.com',
            [request.user.email]
        )

        email.attach('searchresults.csv', response.getvalue(), 'text/csv')
        email.send()

        return response
    else:
        return HttpResponse('No data available to export')

