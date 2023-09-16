from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, Comment
from .forms import CommentForm


def video_list(request):
    videos = Video.objects.all()
    return render(request, "videos/video_list.html", {"videos": videos})


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, "videos/video_detail.html", {"video": video})


def video_edit(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == "POST":
        # 处理视频标题的修改逻辑
        video.title = request.POST["title"]
        video.save()
        return redirect("videos:video_detail", video_id=video.id)

    return render(request, "videos/video_edit.html", {"video": video})


def add_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # 创建新的评论实例
            comment = Comment()
            comment.video = video
            comment.author = form.cleaned_data["author"]
            comment.content = form.cleaned_data["content"]
            comment.save()
            return redirect("videos:video_detail", video_id=video.id)
    else:
        form = CommentForm()

    return render(request, "videos/add_comment.html", {"video": video, "form": form})
