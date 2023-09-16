from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=100)
    # 其他视频字段...

    def __str__(self):
        return self.title


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=50)
    content = models.TextField()
    # 其他评论字段...

    def __str__(self):
        return self.content
