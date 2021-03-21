from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.utils.timezone import now

User = get_user_model()

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="posts",on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    tags = models.CharField(max_length=200)
    slug  = models.SlugField(blank=True, unique=True)
    created_at = models.DateTimeField(default=now)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return (self.title + ' by ' + self.author)

class PostComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username



def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(post_pre_save_receiver, sender=Post)
