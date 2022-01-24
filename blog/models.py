from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import get_user_model


# class PostQuerySet(models.QuerySet):
#     def search(self, query = None):
#         print("serch")
#         qs = self
#         qs = qs.filter(published_date__lte = timezone.now())
#
#         if query is not None:
#             or_lookup = (
#                 Q(text__icontains = query)
#             )
#             qs = qs.filter(or_lookup).distinct()
#         return qs.order_by('published_date')
#
# class PostManager(models.Manager):
#     def get_queryset(self):
#         return PostQuerySet(self.model, using = self._db)
#
#     def search(self, query = None):
#         print('testtesttest',type(query))
#         return self.get_queryset().search(self, query = query)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    # shortText = models.TextField()
    words = models.TextField(default = '')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    # objects = PostManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
