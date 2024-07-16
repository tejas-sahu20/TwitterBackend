import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Users,Tweets,Comments
from django.views import View

def SignUp(request):
    # print('go')
    f=request.body.decode('utf-8')
    bod=json.loads(f)
    # return HttpResponse('h')
    name = bod['name']
    email = bod['email']
    password = bod['password']
    # print('go')
    # print(name)
    u=Users.objects.filter(email=email)
    if u.exists():
        return JsonResponse({'message': 'User already exists'})
    u = Users(name=name, email=email,password= password)
    u.save()
    return JsonResponse({'message': 'User created'})

def Login(request):
    f=request.body.decode('utf-8')
    bod=json.loads(f)
    email = bod['email']
    password = bod['password']
    u=Users.objects.filter(email=email)
    if not u.exists():
        return JsonResponse({'message': 'User does not exist'})
    if password==u.first().password:
        return JsonResponse({'message': 'Login successful'})
    return JsonResponse({'message': 'Wrong password'})

def UserDetails(request):
    userID=request.GET.get('userID')
    u=Users.objects.filter(id=userID)
    if not u.exists():
        return JsonResponse({'message': 'User does not exist'})
    return JsonResponse({
        'name':u.first().name,
        'email':u.first().email,
        'userID':u.first().id
    })
def UserFeed(request):
    tweets=Tweets.objects.all()
    feed=[]
    for tweet in tweets:
        comments=[]
        c=Comments.objects.filter(tweet=tweet.id)
        for comment in c:
            comments.append({
                'commentID':comment.id,
                'comment':comment.text,
                'commentCreator':{
                    'userID':comment.user.id,
                    'name':comment.user.name,
                }
            })
        feed.append({
            'postID':tweet.id,
            'postBody':tweet.tweet,
            'comments':comments
        })
    return JsonResponse({'UserFeed':feed})
class PostMethods(View):
    def post(self,request):
        print('go')
        # return JsonResponse({"hi":"ji"})
        f=request.body.decode('utf-8')
        bod=json.loads(f)
        userID=bod['userID']
        postBody=bod['postBody']
        u=Users.objects.filter(id=userID)
        if not u.exists():
            return JsonResponse({'message': 'User does not exist'})
        post=Tweets(user=u.first(),tweet=postBody)
        post.save()
        return JsonResponse({'message':'Tweet created'})
    def get(self,request):
        postID=request.GET.get('postID')
        # print("this is ",postID)
        # return JsonResponse({'ghis':"jiasd"})
        try:
            post = Tweets.objects.get(id=postID)
        except Tweets.DoesNotExist:
            return JsonResponse({'message': 'Tweet does not exist'}, status=404)
        if not post:
            return JsonResponse({'message': 'Tweet does not exist'})
        comments=[]
        for comment in post.comments.all():
            comments.append({
                'id': comment.id,
                'text': comment.text,
                'user': {
                    'id': comment.user.id,
                    'name': comment.user.name,
                },
            })
        return JsonResponse({
            'postID':post.id,
            'postBody':post.tweet,
            'comments':comments
        })
    def patch(self,request):
        f=request.body.decode('utf-8')
        bod=json.loads(f)
        postBody=bod['postBody']
        postID=bod['postID']
        post=Tweets.objects.get(id=postID)
        if not post:
            return JsonResponse({'message': 'Tweet does not exist'})
        post.tweet=postBody
        post.save()
        return JsonResponse({'message':'Tweet updated'})
    def delete(self,request):
        postID=request.GET.get('postID')
        try:
            post = Tweets.objects.get(id=postID)
        except Tweets.DoesNotExist:
            return JsonResponse({'message': 'Tweet does not exist'})
        post.delete()
        return JsonResponse({'message':'Tweet deleted'})




class CommentMethods(View):
    def post(self,request):
        f=request.body.decode('utf-8')
        bod=json.loads(f)
        userID=bod['userID']
        postID=bod['postID']
        commentBody=bod['commentBody']
        u=Users.objects.filter(id=userID)
        if not u.exists():
            return JsonResponse({'message': 'User does not exist'})
        try:
            tweetCommented=Tweets.objects.get(id=postID)
        except Tweets.DoesNotExist:
            return JsonResponse({'message': 'Tweet does not exist'})
        # if not tweetList.exists():
        #     return JsonResponse({'message': 'Tweet does not exist'})
        c=Comments(user=u.first(),tweet=tweetCommented,text=commentBody)
        c.save()
        return JsonResponse({'message':'Comment created'})
    def get(self,request):
        commentID=request.GET.get('commentID')
        try:
            comment = Comments.objects.get(id=commentID)
        except Comments.DoesNotExist:
            return JsonResponse({'message': 'Comment does not exist'})
        return JsonResponse({
            'commentID':comment.id,
            'comment':comment.text,
            'commentCreator':{
                'id': comment.user.id,
                'name': comment.user.name,
            }
        })
    def patch(self,request):
        f=request.body.decode('utf-8')
        bod=json.loads(f)
        commentID=bod['commentID']
        commentBody=bod['commentBody']
        try :
            c=Comments.objects.get(id=commentID)
        except Comments.DoesNotExist:
            return JsonResponse({'message': 'Comment does not exist'})
        c.text=commentBody
        c.save()
        return JsonResponse({'message':'Comment updated'})
    def delete(self,request):
        deleteID=request.GET.get('commentID')
        try:
            c=Comments.objects.get(id=deleteID)
        except Comments.DoesNotExist:
            return JsonResponse({'message': 'Comment does not exist'})
        c.delete()
        return JsonResponse({'message':'Comment deleted'})
