from django.conf import settings
from django.db import models
from django_mysql.models import EnumField # http://django-mysql.readthedocs.io/en/latest/model_fields/enum_field.html
from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class Keyword(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    keyword_text = models.CharField(max_length=200)
    last_search_date = models.DateTimeField('last search date', null=True)
    date_added = models.DateTimeField('date added')

class KeywordsInSocialMedia(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    social_media_type = EnumField(choices=['twitter', 'reddit'])

class SearchResults(models.Model):
    keyword_in_social_media = models.ForeignKey(KeywordsInSocialMedia, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    link_to_content = models.CharField(max_length=500)
    date_added = models.DateTimeField('date added')

    @staticmethod
    def get_search_results_by_user_id(user_id):

        sql = "SELECT social_searchresults.id, social_searchresults.title, social_searchresults.link_to_content, social_keywordsinsocialmedia.social_media_type, social_searchresults.date_added " \
                "FROM social_searchresults " \
                "JOIN social_keywordsinsocialmedia on social_keywordsinsocialmedia.id = social_searchresults.keyword_in_social_media_id " \
                "JOIN social_keyword ON social_keyword.id = social_keywordsinsocialmedia.keyword_id " \
                "WHERE user_id = %s " \
                "ORDER BY social_searchresults.id desc" % user_id

        cursor = connection.cursor()
        cursor.execute(sql)
        result = dictfetchall(cursor)

        return result

    @staticmethod
    def get_search_results_by_ids_for_user_id(user_id, ids):
        sql = "SELECT social_searchresults.id, social_searchresults.title, social_searchresults.link_to_content, social_keywordsinsocialmedia.social_media_type, social_searchresults.date_added " \
              "FROM social_searchresults " \
              "JOIN social_keywordsinsocialmedia on social_keywordsinsocialmedia.id = social_searchresults.keyword_in_social_media_id " \
              "JOIN social_keyword ON social_keyword.id = social_keywordsinsocialmedia.keyword_id " \
              "WHERE user_id = %s " \
                    "AND social_searchresults.id IN (%s) " \
              "ORDER BY social_searchresults.id desc" % (user_id, ids)

        cursor = connection.cursor()
        cursor.execute(sql)
        result = dictfetchall(cursor)

        return result
