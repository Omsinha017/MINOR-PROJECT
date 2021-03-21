from django.contrib import messages
from posts.models import Post, PostComment
from django.shortcuts import render, redirect, get_object_or_404
from posts.templatetags import extras
from django.http import HttpResponseRedirect
from django.urls import reverse

def AllPosts(request):
    allPosts = Post.objects.all().order_by('-created_at')
    context = {
        'allPosts' : allPosts
    }
    return render(request,"posts/allpost.html",context)

def PostDetail(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views +1
    total_likes = post.total_likes()
    post.save()

    liked = False
    if post.likes.filter(id = request.user.id).exists():
        liked = True

    comments= PostComment.objects.filter(post=post, parent=None)
    replies= PostComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict, 'total_likes': total_likes, 'liked': liked}
    return render(request,"posts/post_detail.html",context)

def UserPosts(request):
    if request.user.is_authenticated:
        qs = Post.objects.filter(user=request.user)
        context = {
            'user' : request.user,
            'posts' : qs
        }
        return render(request,"posts/user_post_list.html",context)


def CreatePost(request):
    if request.user.is_authenticated:
        if request.method == "POST" :
            user = request.user
            title = request.POST['title']
            author = request.POST['author']
            content = request.POST['content']
            tags = request.POST['tags']
            if len(title)<2 or len(author)<3 or len(tags)<2 or len(content)<10:
                messages.error(request, "Please fill the form correctly")
            else:
                obj = Post(user = user, title=title, author=author, content=content, tags=tags)
                obj.save()
                messages.success(request, "Your Post have been successfully Created and Posted")
                return redirect("posts:all")
    return render(request,'posts/post_create_form.html')


def delete_post(request,id=None):
    if request.user.is_authenticated:
        post_to_delete=Post.objects.filter(sno=id)
        post_to_delete.delete()
        messages.success(request, "Your Post have been successfully Deleted")
        return redirect("posts:all")


def post_Comment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=PostComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= PostComment.objects.get(sno=parentSno)
            comment=PostComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
    return redirect(f"/posts/r/{post.slug}")

def LikeView(request,pk):
    post = get_object_or_404(Post, sno= request.POST.get('post_sno'))
    liked = False
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('posts:postdetail', args=[post.slug]))
