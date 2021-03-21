from django.shortcuts import render, redirect
from Home.models import Contact
from django.contrib import messages
from posts.models import Post

def HomePage(request):
    return render(request, "Home/index.html")

def contact(request):
    if request.method == 'POST':   
        name = request.POST['name']     #taking value from the 'name' keyword in the form
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request,'Home/contact.html',{})

def about(request):
    return render(request,'Home/about.html',{})


def search(request):
    query=request.GET['query']
    if len(query)>78 or len(query) == 0:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsTags = Post.objects.filter(tags__icontains=query)
        allPosts =  allPostsTitle.union(allPostsContent, allPostsAuthor, allPostsTags).order_by('-created_at')
    context = {
        'post': allPosts,
        'query': query
    }
    return render(request, 'Home/search.html', context)
