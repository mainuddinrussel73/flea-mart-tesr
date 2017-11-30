from django.shortcuts import render,get_object_or_404
from firstapp.forms import UserForm,UserProfileInform
import json
from firstapp.models import UserProfileInfo,User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login as auth_login,logout
from User.forms import SellItemInfoForm,CommentsForm
from User.models import SellItemInfo,Chat,Notification,Comments,ServerInfo,Auctions
from django.core import serializers
from django.forms.models import model_to_dict
from itertools import chain,cycle
from itertools import zip_longest
import re
from collections import Counter
import string
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import RedirectView
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from django.core import serializers
# json_serializer = serializers.get_serializer("json")()
# companies = json_serializer.serialize(Notification.objects.all().order_by('id')[:5], ensure_ascii=False)

# Create your views here.

other = None
nam = ""
iteuploader = None
slugg_ = None


@login_required
def bid(request,slug=None):
    item = SellItemInfo.objects.get(slug=slug);
    return render(request, 'firstapp/auction_details.html', { "item" : item })



@login_required
def bids(request):
    if request.method == 'POST':
        co = request.POST['co']
        slug = request.POST['slug']

        print(co)
        it = SellItemInfo.objects.get(slug=slug);
        print(it)
        itt  = Auctions.objects.filter(item=it).update(bids=F('bids')+1,biders=request.user.username)
        i  = Auctions.objects.get(item=it)
        co = i.bids


        return JsonResponse({ "bid" : co })
    else:
        return HttpResponse('Request must be POST.')


@login_required
def check(request):

    if request.method == "POST":
        status = request.POST.get('status', None)
        slug =   request.POST.get('slug', None)
        print(status)
        print(slug)
        it = SellItemInfo.objects.filter(slug=slug).update(isAuction=True)
        itr = SellItemInfo.objects.get(slug=slug)
        print(itr)
        o =  Auctions.objects.filter(item=itr)
        print(o)
        if o.count()==0:
            obj = Auctions(uploader=request.user,item=itr,bids=0,biders=request.user.username,isAuction=True)
            obj.save()
        # ggg = list(obj.values('isAuction'))
        # print(ggg)
    return HttpResponse(slug)

@login_required
def auctions(request):
    obj = Auctions.objects.filter(isAuction=True).exclude(uploader=request.user)
    print(obj)
    args = {
        "items" : obj,
        "count" : obj.count()
    }
    return render(request, 'firstapp/auction.html', args,)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
class PostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(SellItemInfo, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        ne = 0
        if user.is_authenticated():
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
                obj.likecount-=1
                ne = obj.likecount
                obj.save()
            else:
                liked = True
                obj.likes.add(user)
                obj.likecount+=1
                ne = obj.likecount
                obj.save()
            updated = True
        data = {
            "updated": updated,
            "liked": liked,
            "ne"   :  ne
        }
        return Response(data)


@login_required
def deleteitem(request,slug=None):
    obj = SellItemInfo.objects.filter(slug=slug)
    if(obj.count()>0):
        obj.delete()

    obj1 = SellItemInfo.objects.filter(uploader=request.user)
    args = {
        "items" : obj1
    }
    return render(request, 'firstapp/profile.html', args,)

@login_required
def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        global other
        global iteuploader
        other = request.POST.get('hide', None)
        itemname = request.POST.get('itemname', None)
        iteuploader = request.POST.get('iteuploader', None)
        # print('asdfa'+itemname)
        if other != request.user.username:
            c = Chat(user=request.user, message=msg,fromm=other,to=request.user.username)
        else:
            c = Chat(user=request.user, message=msg,fromm=nam,to=request.user.username)
        counter = SellItemInfo.objects.get(item_name=itemname)
        n = Notification(user=request.user,to=request.user.username,fromm=other,count=counter.get_slug(),description=msg)
        m = Notification.objects.filter(user=request.user,count=counter.get_slug())
        if msg != '':
            c.save()
        if m.count()==0 and request.user.username != iteuploader:
            n.save()
        return JsonResponse({ 'msg': msg, 'user': c.user.username })
    else:
        return HttpResponse('Request must be POST.')

@login_required
def Messages(request):
    c = Chat.objects.all()
    # print('otnerr')
    # print(c.user.username)
    return render(request, 'firstapp/messages.html', {'chat': c,'other':other,'iteuploader':iteuploader })




@login_required
def Likesupdate(request,slug=None):

    if request.is_ajax():
        obj = SellItemInfo.objects.filter(slug=slug)

        obj_ = []

        obj_ = list(obj.values('likecount'))
        # print(json.dumps(obj_))
        return HttpResponse(json.dumps(obj_))


@login_required
def Notifications(request,username='main'):
    # counter = Notification.objects.all()
    #
    # # print(c.description)
    # return render(request, 'firstapp/notification.html', {'counter': counter})
    if request.is_ajax():
        counter = Notification.objects.exclude(to=request.user)
        hhh = list(counter.values('to','description','count','id'))
        bonus = UserProfileInfo.objects.exclude(user=request.user)
        ggg = list(bonus.values('user','profilepic','user_id'))
        items = SellItemInfo.objects.filter(uploader=request.user)
        it = list(items.values('slug','uploader'))
        lll = []
        u = 0
        result = list(counter.values('user','to','description','count','fromm'))


        for f, b in zip(ggg,result):
            for o in it:

                if(b.get('count')==o.get('slug') ):
                    nnn = {
                        'id' : f.get('user'),
                        'profilepic' : f.get('profilepic'),
                        'to' : b.get('to'),
                        'description' : b.get('description'),
                        'count' : b.get('count'),
                        'fromm' : b.get('fromm')
                    }
                    lll.insert(u,nnn)
                    u+=1

        # print(json.dumps(lll))

        return HttpResponse(json.dumps(lll))
def compare(s1, s2):
    remove = string.punctuation + string.whitespace
    return s1.translate(None, remove) == s2.translate(None, remove)
def combine(list1, list2):
    list1 = iter(list1)
    for item2 in list2:
        if item2 == list2[0]:
            item1 = next(list1)
        yield ''.join(map(str, (item1, item2)))



@login_required
def userhome(request,username='main'):
    u = User.objects.get(username=request.user.username)
    counter = Notification.objects.exclude(user=request.user)



    items_list = SellItemInfo.objects.all().order_by("-timestemp")
    it = SellItemInfo.objects.values('item_type').distinct()
    queary = request.GET.get("q")
    if queary :
        items_list = items_list.filter(
                Q(slug__icontains=queary) |
                Q(item_name__icontains=queary) |
                Q(item_location__icontains=queary)|
                Q(item_type__icontains=queary)
                ).distinct()

    paginator = Paginator(items_list,5)
    page_request_var = 'page'

    page = request.GET.get(page_request_var)
    try :
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except:
        items = paginator.page(paginator.num_pages)

    print(items_list)
    args = {'items' : items,'counter' : counter ,"c" : counter.count(),"page_request_var" : page_request_var,"it":it }
    return render(request,'firstapp/userhome.html',args)

@login_required
def userprofile(request,username='main',pk=None):
    i = ServerInfo.objects.all()
    # print(list(i.values('videos')))
    if pk:
        user = User.objects.get(pk=pk)
        username = user.username


    else:
        user = request.user
        username = user.username

    items = SellItemInfo.objects.filter(uploader=user)
    args = {'user': user,'items' : items,'i':i}
    return render(request, 'firstapp/profile.html', args,)



@login_required
def Comment(request):


    if request.method == 'POST':
        co = request.POST['co']
        slug = request.POST['slug']

        # print(slug)
        # print(co)
        item = SellItemInfo.objects.get(slug=slug);
        username = request.user.username
        c = Comments(user=request.user,item=item,username=request.user.username,content=co)

        if co != '':
             c.save()

        return JsonResponse({ 'comm': co, 'user': request.user.username,'timestemp':c.timestemp,'profilepic' : request.user.userprofileinfo.profilepic.url })
    else:
        return HttpResponse('Request must be POST.')
@login_required
def showitem(request,slug=None,id=None):


    instance = get_object_or_404(SellItemInfo,slug=slug);
    # instance = SellItemInfo.objects.get(item_name=item_name)
    comments = Comments.objects.filter(item=instance);


    c = Chat.objects.all()
    v = Chat.objects.filter(fromm=other,user=request.user)
    # u = request.get('id')
    global nam
    namw = ""
    global slug_
    slug_ = slug
    obj = get_object_or_404(SellItemInfo, slug=slug)
    user = request.user
    liked = False
    if user.is_authenticated():
        if user in obj.likes.all():
            liked = "Unlike"
        else:
            liked = "Like"

    if slug!=None and request.user==instance.uploader:
        try:
            ins = Notification.objects.get(count=slug)
            i = Notification.objects.get(count=slug)
            namw = i.to

            ins.delete()

        except ObjectDoesNotExist:
            ins = None
            i = None
            namw = ""


        # print(ins)


    # for r in instance:
        # r.delete()
    nam = namw

    args = {
        "instance" : instance,
        'chat': c,
        'nam' : nam,
        "liked": liked,
        "obj" : obj,
        "comments" : comments,
        "v"    : v



     }
    return render(request, 'firstapp/details.html', args,)

@login_required
def sellitem(request):

    isposted = False

    if request.method == "POST":
        # userform = UserForm(data=request.POST)
        selliteminfo = SellItemInfoForm(data=request.POST)

        if selliteminfo.is_valid():
            # user = userform.save()
            # user.set_password(user.password)
            # user.save()

            item = selliteminfo.save(commit=False)
            item.uploader = request.user
            item.save()
            # profile.user = user

            if 'item_pic' in request.FILES:
                item.item_pic = request.FILES['item_pic']

            item.save()
            isposted = True

        else :
            print('Not possible')
    else:
        # userform = UserForm()
        selliteminfo = SellItemInfoForm()  #sett item forms

    return render(request,'firstapp/sellitem.html',
    {

        'selliteminfo':selliteminfo,
        'isposted':isposted
    })
