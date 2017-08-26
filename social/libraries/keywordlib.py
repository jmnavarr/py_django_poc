from social.models import Keyword, KeywordsInSocialMedia, SearchResults
from django.utils import timezone
from social.libraries.reddit import search as reddit_search
from social.libraries.twitter import search as twitter_search

def search(keyword_id):
    keyword = Keyword.objects.get(pk=keyword_id)
    keywords_in_social_media = KeywordsInSocialMedia.objects.filter(keyword_id=keyword_id)

    for keyword_in_social_media in keywords_in_social_media:
        search_result = {}

        if keyword_in_social_media.social_media_type == 'reddit':
            search_result = reddit_search(keyword.keyword_text)

        if keyword_in_social_media.social_media_type == 'twitter':
            search_result = twitter_search(keyword.keyword_text)

        if any(search_result):
            search_record = SearchResults(title=search_result['title'],
                                       link_to_content=search_result['url'],
                                       keyword_in_social_media_id=keyword_in_social_media.id,
                                       date_added=timezone.now())
            search_record.save()

    keyword.last_search_date = timezone.now()
    keyword.save()
