from django.core.checks import messages
from django.db.models.query import FlatValuesListIterable
from django.shortcuts import redirect, render
from .models import *
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from random import randint
from django.core.mail import send_mail
from django.conf import settings

import requests

# Create your views here.
def home(request):
    #send_mail("subject", "content", settings.EMAIL_HOST_USER, ['jolabol725@awinceo.com'], fail_silently=False)
    role = request.session.get('role', "")
    best = Article.objects.filter(price__gte =5000)[:6]
    new = Article.objects.all()[:12]

    if role == "trander":
        return render(request, "trander_home.html")
    return render(request, "home.html",{'best':best,'new':new})

def trander_home(request):
    return render(request, "trander_home.html")

def login(request):
    id = request.session.get('id', "")
    role = request.session.get('role', "")
    if id == "":
        message = False
        if request.method == 'POST':
            email=request.POST['email']
            psw=request.POST['password']
            try:
                auth = User.objects.get(email=email,password=psw)
                request.session['email'] = auth.email
                request.session['id'] = auth.id
                request.session['first_name'] = auth.first_name
                request.session['last_name'] = auth.last_name
                if auth.is_client:
                    request.session['role'] = 'client'
                else:
                    request.session['role'] = 'trander'
                if auth.imageProfile == "":
                    request.session['imageProfile'] = "pas de photo"
                else:
                    request.session['imageProfile'] = auth.imageProfile
                if auth.is_client:
                    return redirect(home, {'auth':auth})
                    
                    #return render(request, "home.html", {'auth':auth})
                elif auth.is_trader:
                    return render(request, "trander_home.html", {'auth':auth})
                else:
                    message = True
                    return render(request, "login.html", {'message':message})
            except:
                auth = False 
        return render(request, "login.html", {'message':message})
    elif role == "trander":
        return render(request, "trander_home.html")
    else:
        return redirect(home)

def signup(request):
    email = request.session.get('email', "")
    role = request.session.get('role', "")
    if email == "":
        if request.method == 'POST':
            fisrt=request.POST['fisrt']
            last=request.POST['last']
            email=request.POST['email']
            psw=request.POST['psw']
            re_psw=request.POST['re_psw']
            try:
                client=request.POST['client']
            except:
                commercent=request.POST['commercent']
                client='off'

            if psw==re_psw and client=='on':
                User.objects.create(email=email,first_name=fisrt,last_name=last,password=psw,is_client=True)
                send_mail("Creation compte", "creation de votre compte fait avec succès en tant que client", settings.EMAIL_HOST_USER, ['xibeja1411@0ranges.com'], fail_silently=False)
                return redirect(login)
            
            if psw==re_psw and commercent=='on':
                User.objects.create(email=email,first_name=fisrt,last_name=last,password=psw,is_trader=True)
                send_mail("Creation compte", "creation de votre compte fait avec succès en tant que commerçant", settings.EMAIL_HOST_USER, ['xibeja1411@0ranges.com'], fail_silently=False)
                return redirect(login)
        
        return render(request, "signup.html")
    elif role == "trander":
        return render(request, "trander_home.html")
    else:
        return redirect(home)


def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect(home)


def gestionArticles(request):
    role = request.session.get('role', "")
    if role == "trander":
        id=request.session['id']
        
        page_number = request.GET.get('page',1)
       
        try:
            articles = Article.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(articles, 6)
            page_obj = paginator.get_page(page_number) 
        except:
            articles = None
            paginator = None

        return render(request, "trander/gestion_articles.html", {"page_obj":page_obj})
    else:
        return render(request, "home.html")

def addArticles(request):
    role = request.session.get('role', "")
    categorie = Category.objects.all()
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            image=request.FILES['image']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            categoryid = request.POST.get('category', None)
            category = Category.objects.get(pk=categoryid)
            mark=request.POST['mark']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                obj = Article.objects.create(name=name,shortDescription=shortDescription,description=description,image=image,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),usernameTrader=user,mark=mark)
                obj.category.add(category)
            except:
                return render(request, "trander/add_article.html",{'categorie':categorie,"message":message})

            try:
                articles = Article.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(articles, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_articles.html", {'page_obj':page_obj,"message":message})
        else:
            return render(request, "trander/add_article.html",{'categorie':categorie})

def deleteArticles(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        message = True
        id=request.session['id']
        try:
            obj = Article.objects.filter(pk=pk).delete()
        except:
            return render(request, "trander/add_article.html",{"message":message})

        try:
            articles = Article.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(articles, 6)
            page_obj = paginator.get_page(1) 
        except:
            page_obj = None
            
        return render(request, "trander/gestion_articles.html", {'page_obj':page_obj,"message":message})
    else:
        return render(request, "home.html")

def updateArticles(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        if request.method == 'POST':
            message = True
            a = Article.objects.get(pk=pk)
            stock = a.inStock
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            mark=request.POST['mark']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                Article.objects.filter(pk=pk,usernameTrader=user).update(name=name,shortDescription=shortDescription,description=description,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),mark=mark)
                try:
                    tellMes = TellMe.objects.filter(articleId=pk)
                    if stock == 0:
                        for i in tellMes:
                            send_mail("Nouveau produit ajouter", "le article "+name+" est on stock", settings.EMAIL_HOST_USER, [i.usernameCustomer.email], fail_silently=False)
                except:
                    pass
            except:
                return render(request, "trander/update_article.html",{"message":message})

            try:
                articles = Article.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(articles, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_articles.html", {'page_obj':page_obj,"message":message})
        else:
            id=request.session['id']
            try:
                print("-----------")
                article = Article.objects.filter(pk=pk,usernameTrader=id)[0]
                print(article)
                print("-----------")
            except:
                article = None
                
            return render(request, "trander/update_article.html", {'article':article})
    else:
        return render(request, "home.html")


# CPU
def gestioncpus(request):
    role = request.session.get('role', "")
    if role == "trander":
        id=request.session['id']
        
        page_number = request.GET.get('page',1)
       
        try:
            cpus = CPU.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(cpus, 6)
            page_obj = paginator.get_page(page_number) 
        except:
            cpus = None
            paginator = None

        return render(request, "trander/gestion_cpus.html", {"page_obj":page_obj})
    else:
        return render(request, "home.html")

def addcpus(request):
    role = request.session.get('role', "")
    categorie = Category.objects.all()
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            image=request.FILES['image']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            categoryid = request.POST.get('category', None)
            category = Category.objects.get(pk=categoryid)
            mark=request.POST['mark']
            processorModel=request.POST['processorModel']
            pocessorSupport=request.POST['pocessorSupport']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                obj = CPU.objects.create(name=name,shortDescription=shortDescription,description=description,image=image,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),usernameTrader=user,mark=mark,processorModel=processorModel,pocessorSupport=pocessorSupport)
                obj.category.add(category)
            except:
                return render(request, "trander/add_cpu.html",{'categorie':categorie,"message":message})

            try:
                cpus = CPU.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(cpus, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_cpus.html", {'page_obj':page_obj,"message":message})
        else:
            return render(request, "trander/add_cpu.html",{'categorie':categorie})

def deletecpus(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        message = True
        id=request.session['id']
        try:
            obj = CPU.objects.filter(pk=pk).delete()
        except:
            return render(request, "trander/gestion_cpus.html",{"message":message})

        try:
            cpus = CPU.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(cpus, 6)
            page_obj = paginator.get_page(1) 
        except:
            page_obj = None
            
        return render(request, "trander/gestion_cpus.html", {'page_obj':page_obj,"message":message})
    else:
        return render(request, "home.html")

def updatecpus(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            mark=request.POST['mark']

            processorModel=request.POST['processorModel']
            pocessorSupport=request.POST['pocessorSupport']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                CPU.objects.filter(pk=pk,usernameTrader=user).update(name=name,shortDescription=shortDescription,description=description,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),mark=mark,processorModel=processorModel,pocessorSupport=pocessorSupport)
            except:
                return render(request, "trander/update_cpu.html",{"message":message})

            try:
                cpus = CPU.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(cpus, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_cpus.html", {'page_obj':page_obj,"message":message})
        else:
            id=request.session['id']
            try:
                cpu = CPU.objects.filter(pk=pk,usernameTrader=id)[0]
                
            except:
                cpu = None
                
            return render(request, "trander/update_cpu.html",{'cpu':cpu})
    else:
        return render(request, "home.html")

#FAN
def gestionfans(request):
    role = request.session.get('role', "")
    if role == "trander":
        id=request.session['id']
        
        page_number = request.GET.get('page',1)
       
        try:
            fans = Fan.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(fans, 6)
            page_obj = paginator.get_page(page_number) 
        except:
            cpus = None
            paginator = None

        return render(request, "trander/gestion_fans.html", {"page_obj":page_obj})
    else:
        return render(request, "home.html")

def addfans(request):
    role = request.session.get('role', "")
    categorie = Category.objects.all()
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            image=request.FILES['image']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            categoryid = request.POST.get('category', None)
            category = Category.objects.get(pk=categoryid)
            mark=request.POST['mark']
            
            processorSupport=request.POST['processorSupport']
            Width=request.POST['Width']
            Length=request.POST['Length']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                obj = Fan.objects.create(name=name,shortDescription=shortDescription,description=description,image=image,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),usernameTrader=user,mark=mark,processorSupport=processorSupport,Length=int(Length),Width=int(Width))
                obj.category.add(category)
            except:
                return render(request, "trander/add_fan.html",{'categorie':categorie,"message":message})

            try:
                fans = Fan.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(fans, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_fans.html", {'page_obj':page_obj,"message":message})
        else:
            return render(request, "trander/add_fan.html",{'categorie':categorie})

def deletefans(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        message = True
        id=request.session['id']
        try:
            obj = Fan.objects.filter(pk=pk).delete()
        except:
            return render(request, "trander/gestion_fans.html",{"message":message})

        try:
            fans = Fan.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(fans, 6)
            page_obj = paginator.get_page(1) 
        except:
            page_obj = None
            
        return render(request, "trander/gestion_fans.html", {'page_obj':page_obj,"message":message})
    else:
        return render(request, "home.html")

def updatefans(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            mark=request.POST['mark']

            processorSupport=request.POST['processorSupport']
            Width=request.POST['Width']
            Length=request.POST['Length']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                Fan.objects.filter(pk=pk,usernameTrader=user).update(name=name,shortDescription=shortDescription,description=description,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),mark=mark,Width=int(Width),processorSupport=processorSupport,Length=int(Length))
            except:
                return render(request, "trander/update_fan.html",{"message":message})

            try:
                fans = Fan.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(fans, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_fans.html", {'page_obj':page_obj,"message":message})
        else:
            id=request.session['id']
            try:
                fan = Fan.objects.filter(pk=pk,usernameTrader=id)[0]
                
            except:
                fan = None
                
            return render(request, "trander/update_fan.html",{'fan':fan})
    else:
        return render(request, "home.html")


#Motherboard
def gestionmotherboards(request):
    role = request.session.get('role', "")
    if role == "trander":
        id=request.session['id']
        
        page_number = request.GET.get('page',1)
       
        try:
            motherboards = Motherboard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(motherboards, 6)
            page_obj = paginator.get_page(page_number) 
        except:
            motherboards = None
            paginator = None

        return render(request, "trander/gestion_motherboards.html", {"page_obj":page_obj})
    else:
        return render(request, "home.html")

def addmotherboard(request):
    role = request.session.get('role', "")
    categorie = Category.objects.all()
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            image=request.FILES['image']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            categoryid = request.POST.get('category', None)
            category = Category.objects.get(pk=categoryid)
            mark=request.POST['mark']
            
            processorSupport=request.POST['processorSupport']
            frequencyMemory=request.POST['frequencyMemory']
            typeMemory=request.POST['typeMemory']
            maximumRAMslot=request.POST['maximumRAMslot']
            slotNumber=request.POST['slotNumber']
            connectorGraphic=request.POST['connectorGraphic']
            audioChipset=request.POST['audioChipset']
            networkStandard=request.POST['networkStandard']
            Length=request.POST['Length']
            Width=request.POST['Width']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                obj = Motherboard.objects.create(name=name,shortDescription=shortDescription,description=description,image=image,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),usernameTrader=user,mark=mark,processorSupport=processorSupport,Length=int(Length),Width=int(Width),frequencyMemory=frequencyMemory,typeMemory=typeMemory,maximumRAMslot=int(maximumRAMslot),slotNumber=int(slotNumber),connectorGraphic=connectorGraphic,audioChipset=audioChipset,networkStandard=networkStandard)
                obj.category.add(category)
            except:
                return render(request, "trander/add_motherboard.html",{'categorie':categorie,"message":message})

            try:
                motherboards = Motherboard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(motherboards, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_motherboards.html", {'page_obj':page_obj,"message":message})
        else:
            return render(request, "trander/add_motherboard.html",{'categorie':categorie})

def deletemotherboard(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        message = True
        id=request.session['id']
        try:
            obj = Motherboard.objects.filter(pk=pk).delete()
        except:
            return render(request, "trander/gestion_motherboards.html",{"message":message})

        try:
            motherboards = Motherboard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(motherboards, 6)
            page_obj = paginator.get_page(1) 
        except:
            page_obj = None
            
        return render(request, "trander/gestion_motherboards.html", {'page_obj':page_obj,"message":message})
    else:
        return render(request, "home.html")

def updatemotherboard(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            mark=request.POST['mark']

            processorSupport=request.POST['processorSupport']
            frequencyMemory=request.POST['frequencyMemory']
            typeMemory=request.POST['typeMemory']
            maximumRAMslot=request.POST['maximumRAMslot']
            slotNumber=request.POST['slotNumber']
            connectorGraphic=request.POST['connectorGraphic']
            audioChipset=request.POST['audioChipset']
            networkStandard=request.POST['networkStandard']
            Width=request.POST['Width']
            Length=request.POST['Length']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                Motherboard.objects.filter(pk=pk,usernameTrader=user).update(name=name,shortDescription=shortDescription,description=description,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),mark=mark,Width=int(Width),processorSupport=processorSupport,Length=int(Length),frequencyMemory=frequencyMemory,typeMemory=typeMemory,maximumRAMslot=int(maximumRAMslot),slotNumber=int(slotNumber),connectorGraphic=connectorGraphic,audioChipset=audioChipset,networkStandard=networkStandard)
            except:
                return render(request, "trander/update_motherboard.html",{"message":message})

            try:
                motherboards = Motherboard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(motherboards, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_motherboards.html", {'page_obj':page_obj,"message":message})
        else:
            id=request.session['id']
            try:
                motherboard = Motherboard.objects.filter(pk=pk,usernameTrader=id)[0]
                
            except:
                motherboard = None
                
            return render(request, "trander/update_motherboard.html",{'article':motherboard})
    else:
        return render(request, "home.html")

#RAM
def gestionrams(request):
    role = request.session.get('role', "")
    if role == "trander":
        id=request.session['id']
        
        page_number = request.GET.get('page',1)
       
        try:
            articles = RAM.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(articles, 6)
            page_obj = paginator.get_page(page_number) 
        except:
            articles = None
            paginator = None

        return render(request, "trander/gestion_rams.html", {"page_obj":page_obj})
    else:
        return render(request, "home.html")

def addram(request):
    role = request.session.get('role', "")
    categorie = Category.objects.all()
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            image=request.FILES['image']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            categoryid = request.POST.get('category', None)
            category = Category.objects.get(pk=categoryid)
            mark=request.POST['mark']

            capacity=request.POST['capacity']
            frequencyMemory=request.POST['frequencyMemory']
            typeMemory=request.POST['typeMemory']

            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                obj = RAM.objects.create(name=name,shortDescription=shortDescription,description=description,image=image,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),usernameTrader=user,mark=mark,capacity=int(capacity),frequencyMemory=frequencyMemory,typeMemory=typeMemory)
                obj.category.add(category)
            except:
                return render(request, "trander/add_ram.html",{'categorie':categorie,"message":message})

            try:
                articles = RAM.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(articles, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_rams.html", {'page_obj':page_obj,"message":message})
        else:
            return render(request, "trander/add_ram.html",{'categorie':categorie})

def deleteram(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        message = True
        id=request.session['id']
        try:
            obj = RAM.objects.filter(pk=pk).delete()
        except:
            return render(request, "trander/add_ram.html",{"message":message})

        try:
            articles = RAM.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(articles, 6)
            page_obj = paginator.get_page(1) 
        except:
            page_obj = None
            
        return render(request, "trander/gestion_rams.html", {'page_obj':page_obj,"message":message})
    else:
        return render(request, "home.html")

def updateram(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            mark=request.POST['mark']

            capacity=request.POST['capacity']
            frequencyMemory=request.POST['frequencyMemory']
            typeMemory=request.POST['typeMemory']

            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                RAM.objects.filter(pk=pk,usernameTrader=user).update(name=name,shortDescription=shortDescription,description=description,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),mark=mark,capacity=int(capacity),frequencyMemory=frequencyMemory,typeMemory=typeMemory)
            except:
                return render(request, "trander/update_ram.html",{"message":message})

            try:
                articles = RAM.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(articles, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_rams.html", {'page_obj':page_obj,"message":message})
        else:
            id=request.session['id']
            try:
                article = RAM.objects.filter(pk=pk,usernameTrader=id)[0]
            except:
                article = None
                
            return render(request, "trander/update_ram.html", {'article':article})
    else:
        return render(request, "home.html")

#graphic card
def gestiongraphiccard(request):
    role = request.session.get('role', "")
    if role == "trander":
        id=request.session['id']
        
        page_number = request.GET.get('page',1)
       
        try:
            graphicCards = GraphicCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(graphicCards, 6)
            page_obj = paginator.get_page(page_number) 
        except:
            graphicCards = None
            paginator = None

        return render(request, "trander/gestion_graphiccards.html", {"page_obj":page_obj})
    else:
        return render(request, "home.html")

def addgraphiccard(request):
    role = request.session.get('role', "")
    categorie = Category.objects.all()
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            image=request.FILES['image']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            categoryid = request.POST.get('category', None)
            category = Category.objects.get(pk=categoryid)
            mark=request.POST['mark']
            
            bus=request.POST['bus']
            videoMemorySize=request.POST['videoMemorySize']
            typeMemory=request.POST['typeMemory']

            Width=request.POST['Width']
            Length=request.POST['Length']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                obj = GraphicCard.objects.create(name=name,shortDescription=shortDescription,description=description,image=image,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),usernameTrader=user,mark=mark,bus=bus,videoMemorySize=int(videoMemorySize),typeMemory=typeMemory,Length=int(Length),Width=int(Width))
                obj.category.add(category)
            except:
                return render(request, "trander/add_graphiccard.html",{'categorie':categorie,"message":message})

            try:
                graphicCards = GraphicCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(graphicCards, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_graphiccards.html", {'page_obj':page_obj,"message":message})
        else:
            return render(request, "trander/add_graphiccard.html",{'categorie':categorie})

def deletegraphiccard(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        message = True
        id=request.session['id']
        try:
            obj = GraphicCard.objects.filter(pk=pk).delete()
        except:
            return render(request, "trander/gestion_graphiccards.html",{"message":message})

        try:
            graphicCards = GraphicCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(graphicCards, 6)
            page_obj = paginator.get_page(1) 
        except:
            page_obj = None
            
        return render(request, "trander/gestion_graphiccards.html", {'page_obj':page_obj,"message":message})
    else:
        return render(request, "home.html")

def updategraphiccard(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            mark=request.POST['mark']

            bus=request.POST['bus']
            videoMemorySize=request.POST['videoMemorySize']
            typeMemory=request.POST['typeMemory']

            Width=request.POST['Width']
            Length=request.POST['Length']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                GraphicCard.objects.filter(pk=pk,usernameTrader=user).update(name=name,shortDescription=shortDescription,description=description,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),mark=mark,Width=int(Width),bus=bus,videoMemorySize=int(videoMemorySize),typeMemory=typeMemory,Length=int(Length))
            except:
                return render(request, "trander/update_graphiccard.html",{"message":message})

            try:
                graphicCards = GraphicCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(graphicCards, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_graphiccards.html", {'page_obj':page_obj,"message":message})
        else:
            id=request.session['id']
            try:
                graphicCards = GraphicCard.objects.filter(pk=pk,usernameTrader=id)[0]
                
            except:
                graphicCards = None
                
            return render(request, "trander/update_graphiccard.html",{'article':graphicCards})
    else:
        return render(request, "home.html")

#DiskDur
def gestionDisqueDurs(request):
    role = request.session.get('role', "")
    if role == "trander":
        id=request.session['id']
        
        page_number = request.GET.get('page',1)
       
        try:
            disqueDurs = DisqueDur.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(disqueDurs, 6)
            page_obj = paginator.get_page(page_number) 
        except:
            disqueDurs = None
            paginator = None

        return render(request, "trander/gestion_diskdurs.html", {"page_obj":page_obj})
    else:
        return render(request, "home.html")

def addDisqueDur(request):
    role = request.session.get('role', "")
    categorie = Category.objects.all()
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            image=request.FILES['image']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            categoryid = request.POST.get('category', None)
            category = Category.objects.get(pk=categoryid)
            mark=request.POST['mark']
            
            type=request.POST['type']
            capacity=request.POST['capacity']

            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                obj = DisqueDur.objects.create(name=name,shortDescription=shortDescription,description=description,image=image,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),usernameTrader=user,mark=mark,type=type,capacity=int(capacity))
                obj.category.add(category)
            except:
                return render(request, "trander/add_diskdur.html",{'categorie':categorie,"message":message})

            try:
                disqueDurs = DisqueDur.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(disqueDurs, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_diskdurs.html", {'page_obj':page_obj,"message":message})
        else:
            return render(request, "trander/add_diskdur.html",{'categorie':categorie})

def deleteDisqueDur(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        message = True
        id=request.session['id']
        try:
            obj = DisqueDur.objects.filter(pk=pk).delete()
        except:
            return render(request, "trander/gestion_diskdurs.html",{"message":message})

        try:
            disqueDurs = DisqueDur.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(disqueDurs, 6)
            page_obj = paginator.get_page(1) 
        except:
            page_obj = None
            
        return render(request, "trander/gestion_diskdurs.html", {'page_obj':page_obj,"message":message})
    else:
        return render(request, "home.html")

def updateDisqueDur(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            mark=request.POST['mark']

            type=request.POST['type']
            capacity=request.POST['capacity']

            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                DisqueDur.objects.filter(pk=pk,usernameTrader=user).update(name=name,shortDescription=shortDescription,description=description,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),mark=mark,type=type,capacity=int(capacity))
            except:
                return render(request, "trander/update_diskdur.html",{"message":message})

            try:
                disqueDurs = DisqueDur.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(disqueDurs, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_diskdurs.html", {'page_obj':page_obj,"message":message})
        else:
            id=request.session['id']
            try:
                disqueDurs = DisqueDur.objects.filter(pk=pk,usernameTrader=id)[0]
                
            except:
                disqueDurs = None
                
            return render(request, "trander/update_diskdur.html",{'article':disqueDurs})
    else:
        return render(request, "home.html")



#CASE
def gestionCases(request):
    role = request.session.get('role', "")
    if role == "trander":
        id=request.session['id']
        
        page_number = request.GET.get('page',1)
       
        try:
            cases = Case.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(cases, 6)
            page_obj = paginator.get_page(page_number) 
        except:
            cases = None
            paginator = None

        return render(request, "trander/gestion_cases.html", {"page_obj":page_obj})
    else:
        return render(request, "home.html")

def addCase(request):
    role = request.session.get('role', "")
    categorie = Category.objects.all()
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            image=request.FILES['image']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            categoryid = request.POST.get('category', None)
            category = Category.objects.get(pk=categoryid)
            mark=request.POST['mark']

            maxLengthGraphicCard=request.POST['maxLengthGraphicCard']
            maxHeightCPUfan=request.POST['maxHeightCPUfan']
            maxLengthPowerSupply=request.POST['maxLengthPowerSupply']
            maxLengthMotherboard=request.POST['maxLengthMotherboard']


            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                obj = Case.objects.create(name=name,shortDescription=shortDescription,description=description,image=image,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),usernameTrader=user,mark=mark,maxLengthGraphicCard=int(maxLengthGraphicCard),maxHeightCPUfan=int(maxHeightCPUfan),maxLengthPowerSupply=int(maxLengthPowerSupply),maxLengthMotherboard=int(maxLengthMotherboard))
                obj.category.add(category)
            except:
                return render(request, "trander/add_case.html",{'categorie':categorie,"message":message})

            try:
                cases = Case.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(cases, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_cases.html", {'page_obj':page_obj,"message":message})
        else:
            return render(request, "trander/add_case.html",{'categorie':categorie})

def deleteCase(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        message = True
        id=request.session['id']
        try:
            obj = Case.objects.filter(pk=pk).delete()
        except:
            return render(request, "trander/add_article.html",{"message":message})

        try:
            cases = Case.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(cases, 6)
            page_obj = paginator.get_page(1) 
        except:
            page_obj = None
            
        return render(request, "trander/gestion_cases.html", {'page_obj':page_obj,"message":message})
    else:
        return render(request, "home.html")

def updateCase(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            mark=request.POST['mark']

            maxLengthGraphicCard=request.POST['maxLengthGraphicCard']
            maxHeightCPUfan=request.POST['maxHeightCPUfan']
            maxLengthPowerSupply=request.POST['maxLengthPowerSupply']
            maxLengthMotherboard=request.POST['maxLengthMotherboard']

            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                Case.objects.filter(pk=pk,usernameTrader=user).update(name=name,shortDescription=shortDescription,description=description,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),mark=mark,maxLengthGraphicCard=int(maxLengthGraphicCard),maxHeightCPUfan=int(maxHeightCPUfan),maxLengthPowerSupply=int(maxLengthPowerSupply),maxLengthMotherboard=int(maxLengthMotherboard))
            except:
                return render(request, "trander/update_case.html",{"message":message})

            try:
                cases = Case.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(cases, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_cases.html", {'page_obj':page_obj,"message":message})
        else:
            id=request.session['id']
            try:
                article = Case.objects.filter(pk=pk,usernameTrader=id)[0]
            except:
                article = None
                
            return render(request, "trander/update_case.html", {'article':article})
    else:
        return render(request, "home.html")

#PowerSupply
def gestionPowerSupplys(request):
    role = request.session.get('role', "")
    if role == "trander":
        id=request.session['id']
        
        page_number = request.GET.get('page',1)
       
        try:
            powerSupplys = PowerSupply.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(powerSupplys, 6)
            page_obj = paginator.get_page(page_number) 
        except:
            powerSupplys = None
            paginator = None

        return render(request, "trander/gestion_powersupplys.html", {"page_obj":page_obj})
    else:
        return render(request, "home.html")

def addPowerSupply(request):
    role = request.session.get('role', "")
    categorie = Category.objects.all()
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            image=request.FILES['image']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            categoryid = request.POST.get('category', None)
            category = Category.objects.get(pk=categoryid)
            mark=request.POST['mark']
            Width=request.POST['Width']
            Length=request.POST['Length']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                obj = PowerSupply.objects.create(name=name,shortDescription=shortDescription,description=description,image=image,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),usernameTrader=user,mark=mark,Width=int(Width),Length=int(Length))
                obj.category.add(category)
            except:
                return render(request, "trander/add_powersupply.html",{'categorie':categorie,"message":message})

            try:
                powerSupplys = PowerSupply.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(powerSupplys, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_powersupplys.html", {'page_obj':page_obj,"message":message})
        else:
            return render(request, "trander/add_powersupply.html",{'categorie':categorie})

def deletePowerSupply(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        message = True
        id=request.session['id']
        try:
            obj = PowerSupply.objects.filter(pk=pk).delete()
        except:
            return render(request, "trander/add_case.html",{"message":message})

        try:
            powerSupplys = PowerSupply.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(powerSupplys, 6)
            page_obj = paginator.get_page(1) 
        except:
            page_obj = None
            
        return render(request, "trander/gestion_powersupplys.html", {'page_obj':page_obj,"message":message})
    else:
        return render(request, "home.html")

def updatePowerSupply(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            mark=request.POST['mark']
            Width=request.POST['Width']
            Length=request.POST['Length']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                PowerSupply.objects.filter(pk=pk,usernameTrader=user).update(name=name,shortDescription=shortDescription,description=description,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),mark=mark,Width=int(Width),Length=int(Length))
            except:
                return render(request, "trander/update_powersupply.html",{"message":message})

            try:
                powerSupplys = PowerSupply.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(powerSupplys, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_powersupplys.html", {'page_obj':page_obj,"message":message})
        else:
            id=request.session['id']
            try:
                article = PowerSupply.objects.filter(pk=pk,usernameTrader=id)[0]
                
            except:
                article = None
                
            return render(request, "trander/update_powersupply.html", {'article':article})
    else:
        return render(request, "home.html")

#SoundCard
def gestionSoundCards(request):
    role = request.session.get('role', "")
    if role == "trander":
        id=request.session['id']
        
        page_number = request.GET.get('page',1)
       
        try:
            soundCards = SoundCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(soundCards, 6)
            page_obj = paginator.get_page(page_number) 
        except:
            soundCards = None
            paginator = None

        return render(request, "trander/gestion_soundcards.html", {"page_obj":page_obj})
    else:
        return render(request, "home.html")

def addSoundCard(request):
    role = request.session.get('role', "")
    categorie = Category.objects.all()
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            image=request.FILES['image']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            categoryid = request.POST.get('category', None)
            category = Category.objects.get(pk=categoryid)
            mark=request.POST['mark']
            audioChipset=request.POST['audioChipset']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                obj = SoundCard.objects.create(name=name,shortDescription=shortDescription,description=description,image=image,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),usernameTrader=user,mark=mark,audioChipset=audioChipset)
                obj.category.add(category)
            except:
                return render(request, "trander/add_soundcard.html",{'categorie':categorie,"message":message})

            try:
                soundCards = SoundCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(soundCards, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_soundcards.html", {'page_obj':page_obj,"message":message})
        else:
            return render(request, "trander/add_soundcard.html",{'categorie':categorie})

def deleteSoundCard(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        message = True
        id=request.session['id']
        try:
            obj = SoundCard.objects.filter(pk=pk).delete()
        except:
            return render(request, "trander/add_soundcard.html",{"message":message})

        try:
            soundCards = SoundCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(soundCards, 6)
            page_obj = paginator.get_page(1) 
        except:
            page_obj = None
            
        return render(request, "trander/gestion_soundcards.html", {'page_obj':page_obj,"message":message})
    else:
        return render(request, "home.html")

def updateSoundCard(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            mark=request.POST['mark']

            audioChipset=request.POST['audioChipset']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                SoundCard.objects.filter(pk=pk,usernameTrader=user).update(name=name,shortDescription=shortDescription,description=description,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),mark=mark,audioChipset=audioChipset)
            except:
                return render(request, "trander/update_soundcard.html",{"message":message})

            try:
                soundCards = SoundCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(soundCards, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_soundcards.html", {'page_obj':page_obj,"message":message})
        else:
            id=request.session['id']
            try:
                article = SoundCard.objects.filter(pk=pk,usernameTrader=id)[0]
                
            except:
                article = None
                
            return render(request, "trander/update_soundcard.html", {'article':article})
    else:
        return render(request, "home.html")


#NetworkCard
def gestionNetworkCards(request):
    role = request.session.get('role', "")
    if role == "trander":
        id=request.session['id']
        
        page_number = request.GET.get('page',1)
       
        try:
            networkCards = NetworkCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(networkCards, 6)
            page_obj = paginator.get_page(page_number) 
        except:
            networkCards = None
            paginator = None

        return render(request, "trander/gestion_networkcards.html", {"page_obj":page_obj})
    else:
        return render(request, "home.html")

def addNetworkCard(request):
    role = request.session.get('role', "")
    categorie = Category.objects.all()
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            image=request.FILES['image']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            categoryid = request.POST.get('category', None)
            category = Category.objects.get(pk=categoryid)
            mark=request.POST['mark']
            networkStandard=request.POST['networkStandard']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                obj = NetworkCard.objects.create(name=name,shortDescription=shortDescription,description=description,image=image,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),usernameTrader=user,mark=mark,networkStandard=networkStandard)
                obj.category.add(category)
            except:
                return render(request, "trander/add_networkcard.html",{'categorie':categorie,"message":message})

            try:
                networkCards = NetworkCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(networkCards, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_networkcards.html", {'page_obj':page_obj,"message":message})
        else:
            return render(request, "trander/add_networkcard.html",{'categorie':categorie})

def deleteNetworkCard(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        message = True
        id=request.session['id']
        try:
            obj = NetworkCard.objects.filter(pk=pk).delete()
        except:
            return render(request, "trander/add_networkcard.html",{"message":message})

        try:
            networkCards = NetworkCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
            paginator = Paginator(networkCards, 6)
            page_obj = paginator.get_page(1) 
        except:
            page_obj = None
            
        return render(request, "trander/gestion_networkcards.html", {'page_obj':page_obj,"message":message})
    else:
        return render(request, "home.html")

def updateNetworkCard(request,pk):
    role = request.session.get('role', "")
    if role == "trander":
        if request.method == 'POST':
            message = True
            name=request.POST['name']
            shortDescription=request.POST['shortDescription']
            description=request.POST['description']
            price=request.POST['price']
            delivery=request.POST['delivery']
            discount=request.POST['discount']
            inStock=request.POST['inStock']
            mark=request.POST['mark']

            networkStandard=request.POST['networkStandard']
            id=request.session['id']
            user = User.objects.get(pk=id)
            try:
                NetworkCard.objects.filter(pk=pk,usernameTrader=user).update(name=name,shortDescription=shortDescription,description=description,price=float(price),delivery=float(delivery),discount=float(discount),inStock=int(inStock),mark=mark,networkStandard=networkStandard)
            except:
                return render(request, "trander/gestion_networkcards.html",{"message":message})

            try:
                networkCards = NetworkCard.objects.order_by("dateAdded").filter(usernameTrader=id).reverse()
                paginator = Paginator(networkCards, 6)
                page_obj = paginator.get_page(1) 
            except:
                page_obj = None
                
                
            return render(request, "trander/gestion_networkcards.html", {'page_obj':page_obj,"message":message})
        else:
            id=request.session['id']
            try:
                article = NetworkCard.objects.filter(pk=pk,usernameTrader=id)[0]
                
            except:
                article = None
                
            return render(request, "trander/update_networkcard.html", {'article':article})
    else:
        return render(request, "home.html")


#articles

def articles(request):

    page_number = request.GET.get('page',1)

    search = request.GET.get('search','')
    category = request.GET.get('category','')
    new = request.GET.get('new','')
    best = request.GET.get('best','')
    pulsvendeur = request.GET.get('pulsvendeur','')

    if search !='':
        articles = Article.objects.filter(name__contains=search,shortDescription__contains=search,description__contains=search,).order_by("dateAdded").reverse()
        link = "search"
        value = search

    if category !='':
        categorylist = Category.objects.filter(name=category)
        articles = Article.objects.filter(category=categorylist[0]).order_by("dateAdded").reverse()
        link = "category"
        value = category

    if new !='':
        articles = Article.objects.order_by("dateAdded").reverse()
        link = "new"
        value = new

    if best !='':
        articles = Article.objects.order_by("dateAdded").reverse()
        link = "best"
        value = best

    if pulsvendeur !='':
        articles = Article.objects.order_by("dateAdded")
        link = "pulsvendeur"
        value = pulsvendeur


    size = 12
    try:
        paginator = Paginator(articles, size)
        page_obj = paginator.get_page(page_number) 
    except:
        articles = Article.objects.order_by("dateAdded").reverse()
        paginator = Paginator(articles, size)
        page_obj = paginator.get_page(page_number)
        link = "all"
        value = "true"

    return render(request, "main/articles.html", {"page_obj":page_obj,"link":link,"value":value})



#articles

def article(request,pk):

    article=Article.objects.get(pk=pk)
    print(article.id)
    return render(request, "main/article.html", {'article':article})


#profile

def profile(request,pk):
    id=request.session.get('id',0)
    if id == pk:
        isYourProfile = True
    else:
        isYourProfile = False
    try:
        user=User.objects.get(pk=pk)
    except:
        user=None
    try:
        card = Card.objects.get(user=user)
    except:
        card = None
    return render(request, "main/profile.html", {'user':user,'isYourProfile':isYourProfile,'card':card})



#profile

def profilePhotoUpadte(request):
    id=request.session.get('id',0)
    print("------")
    print(id)
    if id == 0:
        return home
    else:
        image=request.FILES['image']

        user = User.objects.get(pk=id)
        user.imageProfile = image
        user.save()

    try:
        user=User.objects.get(pk=id)
    except:
        user=None
    try:
        card = Card.objects.get(user=user)
    except:
        card = None
    return render(request, "main/profile.html", {'user':user,'isYourProfile':True,'card':card})

#deletecard

def deletecard(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        user = User.objects.get(pk=id)
        card = Card.objects.get(user=user)
        card.delete()
    try:
        user=User.objects.get(pk=id)
    except:
        user=None
    try:
        card = Card.objects.get(user=user)
    except:
        card = None
    return render(request, "main/profile.html", {'user':user,'isYourProfile':True,'card':card})


def addcard(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        num=request.POST['num']
        name=request.POST['name']
        mmyy=request.POST['mmyy']
        cvv=request.POST['cvv']
        user = User.objects.get(pk=id)
        card = Card.objects.create(cardNumber=num,name=name,mmyy=mmyy,cvv=cvv,user=user)
    try:
        user=User.objects.get(pk=id)
    except:
        user=None
    try:
        card = Card.objects.get(user=user)
    except:
        card = None
    return render(request, "main/profile.html", {'user':user,'isYourProfile':True,'card':card})

def updatedata(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        fisrt=request.POST['fisrt']
        last=request.POST['last']
        numcart=request.POST['numcart']
        email=request.POST['email']
        tel=request.POST['tel']
        adresse=request.POST['Adresse']
        user = User.objects.get(pk=id)
        user.first_name=fisrt
        user.last_name=last
        user.numCard=numcart
        user.email=email
        user.phoneNumber=tel
        user.address=adresse
        user.save()

    try:
        user=User.objects.get(pk=id)
    except:
        user=None
    try:
        card = Card.objects.get(user=user)
    except:
        card = None
    return render(request, "main/profile.html", {'user':user,'isYourProfile':True,'card':card})



def passwordUpdate(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        old=request.POST['old']
        password=request.POST['pass']
        newpass=request.POST['newpass']
        user = User.objects.get(pk=id)
        if password == newpass and old == user.password:
            user.password = password
            user.save()

    try:
        user=User.objects.get(pk=id)
    except:
        user=None
    try:
        card = Card.objects.get(user=user)
    except:
        card = None
    return render(request, "main/profile.html", {'user':user,'isYourProfile':True,'card':card})




def addshopcard(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:

        user = User.objects.get(pk=id)
        if request.method == 'POST':
            count=request.POST["count"]
            if count == "":
                count = 1
            
            idproduct=request.POST["idproduct"]
            article = Article.objects.get(pk=idproduct)
            if article.discount == 0:
                price = article.price
            else:    
                price = article.price - (article.price * article.discount)/ 100

            delivery = article.delivery
            ShoppingCart.objects.create(article=article,user=user,partNumber=count,price=price,delivery=delivery)

        shoppingCarts = ShoppingCart.objects.filter(user=user)
        card = Card.objects.filter(user=user)
        prixTotal = 0
        liversionTotal = 0
        for s in shoppingCarts:
            prixTotal += s.price * s.partNumber
            liversionTotal += s.article.delivery

    return render(request, "main/painer.html",{'shoppingCarts':shoppingCarts,'prixTotal':prixTotal,'liversionTotal':liversionTotal,'card':card})


def deleteItemFromCard(request,pk):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        s = ShoppingCart.objects.filter(pk=pk)
        s.delete()
        user = User.objects.get(pk=id)
        

        shoppingCarts = ShoppingCart.objects.filter(user=user)
        card = Card.objects.filter(user=user)
        prixTotal = 0
        liversionTotal = 0
        for s in shoppingCarts:
            prixTotal += s.price * s.partNumber
            liversionTotal += s.article.delivery

    return render(request, "main/painer.html",{'shoppingCarts':shoppingCarts,'prixTotal':prixTotal,'liversionTotal':liversionTotal,'card':card})

def validerPainer(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:

        user = User.objects.get(pk=id)
        if request.method == 'POST':
            num=request.POST['num']
            name=request.POST['name']
            mmyy=request.POST['mmyy']
            cvv=request.POST['cvv']
            Card.objects.create(cardNumber=num,name=name,mmyy=mmyy,cvv=cvv,user=user)

        card = Card.objects.get(user=user)
        print(card.cardNumber)
        print(card.name)
        print(card.mmyy)
        print(card.cvv)
        shoppingCarts = ShoppingCart.objects.filter(user=user)
        prixtotale = 0
        for s in shoppingCarts:
            prixtotale += s.price * s.partNumber + s.delivery

        context = {
            'cardNumber':card.cardNumber,
            'name':card.name,
            'mmyy':card.mmyy,
            'cvv':card.cvv,
            'prixtotale':prixtotale
        }
        print(context)
        data = requests.post('http://127.0.0.1:2000/paiement/',context)
        print(data.json()['message'])
        if data.json()['message'] == 'opération bien fait':
            for s in shoppingCarts:
                s.article.inStock = s.article.inStock - s.partNumber
                s.article.save()
                Demand.objects.create(article=s.article,price=s.price,delivery=s.delivery,advancement="en traitement",partNumber=s.partNumber,user=user)
                s.delete()
        else:
            card = Card.objects.filter(user=user)
            prixTotal = 0
            liversionTotal = 0
            for s in shoppingCarts:
                prixTotal += s.price * s.partNumber
                liversionTotal += s.article.delivery

            return render(request, "main/painer.html",{'shoppingCarts':shoppingCarts,'prixTotal':prixTotal,'liversionTotal':liversionTotal,'card':card,'message':data.json()['message']})
        
        return redirect(demmand)



def achatverfication(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:

        user = User.objects.get(pk=id)
        if request.method == 'POST':
            count=request.POST["count"]
            print(count)
            if count == "":
                count = 1
            
            idproduct=request.POST["idproduct1"]
            print(idproduct)
            article = Article.objects.get(pk=idproduct)
            card = Card.objects.filter(user=user)
            
            return render(request, "main/achat.html",{'shoppingCart':article,'card':card,'c':count})

        return home


def achat(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:

        user = User.objects.get(pk=id)
        card = Card.objects.filter(user=user)
        if request.method == 'POST':
            if not card:
                num=request.POST['num']
                name=request.POST['name']
                mmyy=request.POST['mmyy']
                cvv=request.POST['cvv']
                card = Card.objects.create(cardNumber=num,name=name,mmyy=mmyy,cvv=cvv,user=user)

            pk=request.POST['art']
            part=request.POST['part']
        article = Article.objects.get(pk=pk)
        if article.discount == 0:
            price = article.price
        else:    
            price = article.price - (article.price * article.discount)/ 100

        delivery = article.delivery
        prixtotale = delivery+price
        card = Card.objects.get(user=user)
        context = {
            'cardNumber':card.cardNumber,
            'name':card.name,
            'mmyy':card.mmyy,
            'cvv':card.cvv,
            'prixtotale':prixtotale
        }
        data = requests.post('http://127.0.0.1:2000/paiement/',context)
        if data.json()['message'] == 'opération bien fait':
            Demand.objects.create(article=article,price=price,delivery=delivery,advancement="en traitement",partNumber=part,user=user)
            article.inStock = article.inStock - int(part)
            article.save()
        else:
            pass
 
    return redirect(demmand)

def demmand(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        
        page_number = request.GET.get('page',1)
       
        try:
            user = User.objects.get(pk=id)
            demands = Demand.objects.order_by("dateAdded").filter(user=user).reverse()
            paginator = Paginator(demands, 10)
            page_obj = paginator.get_page(page_number) 
        except:
            demands = None
            paginator = None

        return render(request, "main/demmand.html", {'page_obj':page_obj})

def AccepterDemmandclient(request,pk):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        demand = Demand.objects.get(pk=pk)
        print("--=-=-==---")
        print(demand.advancement)
        demand.advancement = 'Terminer'
        demand.save()

        page_number = request.GET.get('page',1)
       
        try:
            user = User.objects.get(pk=id)
            demands = Demand.objects.order_by("dateAdded").filter(user=user).reverse()
            paginator = Paginator(demands, 10)
            page_obj = paginator.get_page(page_number)
            date = datetime.today() - timedelta(days=3)
        except:
            demands = None
            paginator = None

        return render(request, "main/historique.html", {'page_obj':page_obj,'date':date})

def DeleteDemmand(request,pk):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        message = True
        user = User.objects.get(pk=id)
        try:
            demand = Demand.objects.get(pk=pk)
            card = Card.objects.get(user=user) 
            prixtotale = (demand.price + demand.delivery)*demand.partNumber
            context = {
                'cardNumber':card.cardNumber,
                'name':card.name,
                'mmyy':card.mmyy,
                'cvv':card.cvv,
                'prixtotale':prixtotale
            }
            data = requests.post('http://127.0.0.1:2000/back/',context)
            if data.json()['message'] == 'Votre solde est bien récupéré':
                demand.delete()
            else:
                pass
        except:
            message =False
        
        page_number = request.GET.get('page',1)
       
        try:
            user = User.objects.get(pk=id)
            demands = Demand.objects.order_by("dateAdded").filter(user=user).reverse()
            paginator = Paginator(demands, 10)
            page_obj = paginator.get_page(page_number) 
        except:
            demands = None
            paginator = None

        return render(request,"main/demmand.html",{'page_obj':page_obj,'message':message})


def historique(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        
        page_number = request.GET.get('page',1)
       
        try:
            user = User.objects.get(pk=id)
            demands = Demand.objects.order_by("dateAdded").filter(user=user).reverse()
            paginator = Paginator(demands, 10)
            page_obj = paginator.get_page(page_number)
            date = datetime.today() - timedelta(days=3)
        except:
            demands = None
            paginator = None

        return render(request, "main/historique.html", {'page_obj':page_obj,'date':date})

def ReturnDemmand(request,pk):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        try:
            user = User.objects.get(pk=id)
            demand = Demand.objects.get(pk=pk)
            codeReturn = randint(100000000000,999999999999)
            u = Return.objects.create(demand=demand,codeReturn=codeReturn,user=user)
            u.save()
            demand.advancement = "verfication retour"
        except:
            pass
        

        return redirect(ReturnDemmandPage)

def ReturnDemmandPage(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        
        page_number = request.GET.get('page',1)
        print('page_number')
        try:
            print('------1-------')
            user = User.objects.get(pk=id)
            print('-----2-----')
            returns = Return.objects.filter(user=user)
            print(returns)
            #returns = Return.objects.order_by("dateAdded").filter(user=user).reverse()
            print('-----3----')
            paginator = Paginator(returns, 10)
            print('------4-----')
            page_obj = paginator.get_page(page_number) 
            print('-----5-----')
            print(page_obj)
        except:
            returns = None
            paginator = None

        return render(request,"main/return.html",{'page_obj':page_obj})


def addListAttendPage(request,pk):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        usernameCustomer = User.objects.get(pk=id)
        articleId = Article.objects.get(pk=pk)
        TellMe.objects.create(usernameCustomer=usernameCustomer,articleId=articleId)

    return redirect(ListAttendPage)

def deleteListAttendPage(request,pk):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        tellme = TellMe.objects.get(pk=pk)
        tellme.delete()

    return redirect(ListAttendPage)


def ListAttendPage(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        
        page_number = request.GET.get('page',1)
        print('page_number')
        try:
            print('------1-------')
            user = User.objects.get(pk=id)
            print('-----2-----')
            tellMes = TellMe.objects.filter(usernameCustomer=user)
            print(tellMes)
            print('-----3----')
            paginator = Paginator(tellMes, 10)
            print('------4-----')
            page_obj = paginator.get_page(page_number) 
            print('-----5-----')
            print(page_obj)
        except:
            tellMes = None
            paginator = None

        return render(request,"main/listattend.html",{'page_obj':page_obj})

def outOfStock(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        
        page_number = request.GET.get('page',1)
        print('page_number')
        try:
            print('------1-------')
            user = User.objects.get(pk=id)
            print('-----2-----')
            articles = Article.objects.filter(usernameTrader=user,inStock=0)
            print('-----3----')
            paginator = Paginator(articles, 10)
            print('------4-----')
            page_obj = paginator.get_page(page_number) 
            print('-----5-----')
            print(page_obj)
        except:
            articles = None
            paginator = None

        return render(request,"trander/outstock.html",{'page_obj':page_obj})

def demmand_t(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        
        page_number = request.GET.get('page',1)
        print('page_number')
        try:
            user = User.objects.get(pk=id)
            articles = Article.objects.filter(usernameTrader=user)
            demmands = []
            for i in articles:
                demmands += Demand.objects.filter(article=i).order_by('dateAdded').reverse()
            print('====-===')
            print(demmands)
            paginator = Paginator(demmands, 10)
            page_obj = paginator.get_page(page_number)
            print(page_obj)
        except:
            demmands = None
            paginator = None

        return render(request,"trander/demmand.html",{'page_obj':page_obj})

def acceptDemmand(request,pk):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:


        demmands = Demand.objects.get(pk=pk)
        demmands.advancement = 'en transport'
        demmands.save()
        
        return redirect(demmand_t)


def returnarticle(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        
        page_number = request.GET.get('page',1)
        print('page_number')
        try:
            user = User.objects.get(pk=id)
            articles = Article.objects.filter(usernameTrader=user)
            print("[][-]][-]]]")
            demmands = []
            for i in articles:
                demmands += Demand.objects.filter(article=i).order_by('dateAdded').reverse()
            print(demmands)
            returns = []
            for i in demmands:
                returns += Return.objects.filter(demand=i.id).order_by('dateAdded').reverse()
            print('====-===')
            print(returns)
            paginator = Paginator(returns, 10)
            page_obj = paginator.get_page(page_number)
            print(page_obj)
        except:
            returns = None
            paginator = None

        return render(request,"trander/articleRender.html",{'page_obj':page_obj})

def acceptReturn(request,pk):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:


        returns = Return.objects.get(pk=pk)
        returns.isAccepted = True
        returns.isConsulted = True
        returns.save()
        user = returns.demand.user
        card = Card.objects.get(user=user)
        prixtotale = returns.demand.price * returns.demand.partNumber + returns.demand.delivery
        context = {
                'cardNumber':card.cardNumber,
                'name':card.name,
                'mmyy':card.mmyy,
                'cvv':card.cvv,
                'prixtotale':prixtotale
        }
        data = requests.post('http://127.0.0.1:2000/back/',context)
        if data.json()['message'] == 'Votre solde est bien récupéré':
            message = True
        else:
            message = False

        return redirect(returnarticle)

def refuserReturn(request,pk):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:


        returns = Return.objects.get(pk=pk)
        returns.isAccepted = False
        returns.isConsulted = True
        returns.save()
        
        return redirect(returnarticle)


def statistique(request):
    id=request.session.get('id',0)
    if id == 0:
        return home
    else:
        
        page_number = request.GET.get('page',1)
       
        try:
            user = User.objects.get(pk=id)
            demands = Demand.objects.order_by("dateAdded").filter(user=user).reverse()
            paginator = Paginator(demands, 10)
            page_obj = paginator.get_page(page_number)
            date = datetime.today() - timedelta(days=3)
        except:
            demands = None
            paginator = None

        return render(request, "trander/statistique.html", {'page_obj':page_obj,'date':date})

def confpc(request):
    id=request.session.get('id',0)
   
    cpu=0
    fan=0
    motherboard=0
    ram=0
    graphicCard=0
    disqueDur=0
    case=0
    powerSupply=0
    soundCard=0
    networkCard=0
        
    if cpu == 0:
        cpus = CPU.objects.all()
        cpus_onces = None
    else:
        cpus_onces = CPU.objects.get(pk=cpu)
        cpus = None

    if fan == 0:
        fans = Fan.objects.all()
        fans_onces = None
    else:
        fans_onces = Fan.objects.get(pk=cpu)
        fans = None

    if motherboard == 0:
        motherboards = Motherboard.objects.all()
        motherboards_onces = None
    else:
        motherboards_onces = Motherboard.objects.get(pk=cpu)
        motherboards = None


    if ram == 0:
        rams = RAM.objects.all()
        rams_onces = None
    else:
        rams_onces = RAM.objects.get(pk=cpu)
        rams = None


    if graphicCard == 0:
        graphicCards = GraphicCard.objects.all()
        graphicCards_onces = None
    else:
        graphicCards_onces = GraphicCard.objects.get(pk=cpu)
        graphicCards = None


    if disqueDur == 0:
        disqueDurs = DisqueDur.objects.all()
        disqueDurs_onces = None
    else:
        disqueDurs_onces = DisqueDur.objects.get(pk=cpu)
        disqueDurs = None

    

    if case == 0:
        cases = Case.objects.all()
        cases_onces = None
    else:
        cases_onces = Case.objects.get(pk=cpu)
        cases = None


    if powerSupply == 0:
        powerSupplys = PowerSupply.objects.all()
        powerSupplys_onces = None
    else:
        powerSupplys_onces = PowerSupply.objects.get(pk=cpu)
        powerSupplys = None



    if soundCard == 0:
        soundCards = SoundCard.objects.all()
        soundCards_onces = None
    else:
        soundCards_onces = SoundCard.objects.get(pk=cpu)
        soundCards = None


    if networkCard == 0:
        networkCards = NetworkCard.objects.all()
        networkCards_onces = None
    else:
        networkCards_onces = NetworkCard.objects.get(pk=cpu)
        networkCards = None

    prix = 0

    return render(request, "client/conf_pc.html", {
        'cpus':cpus,
        'fans':fans,
        'motherboards':motherboards,
        'rams':rams,
        'graphicCards':graphicCards,
        'disqueDurs':disqueDurs,
        'cases':cases,
        'powerSupplys':powerSupplys,
        'soundCards':soundCards,
        'networkCards':networkCards,

        'cpus_onces':cpus_onces,
        'fans_onces':fans_onces,
        'motherboards_onces':motherboards_onces,
        'rams_onces':rams_onces,
        'graphicCards_onces':graphicCards_onces,
        'disqueDurs_onces':disqueDurs_onces,
        'cases_onces':cases_onces,
        'powerSupplys_onces':powerSupplys_onces,
        'soundCards_onces':soundCards_onces,
        'networkCards_onces':networkCards_onces,

        'prix':prix,
    })


def cpuselected(request):
    id=request.session.get('id',0)
   
    fan=0
    motherboard=0
    ram=0
    graphicCard=0
    disqueDur=0
    case=0
    powerSupply=0
    soundCard=0
    networkCard=0
    
        
    
    cpus_onces = CPU.objects.get(pk=4)
    print(cpus_onces)
    cpus = None

    cpu = 0
    if fan == 0:
        fans = Fan.objects.all()
        fans_onces = None
    else:
        fans_onces = Fan.objects.get(pk=cpu)
        fans = None

    if motherboard == 0:
        motherboards = Motherboard.objects.all()
        motherboards_onces = None
    else:
        motherboards_onces = Motherboard.objects.get(pk=cpu)
        motherboards = None


    if ram == 0:
        rams = RAM.objects.all()
        rams_onces = None
    else:
        rams_onces = RAM.objects.get(pk=cpu)
        rams = None


    if graphicCard == 0:
        graphicCards = GraphicCard.objects.all()
        graphicCards_onces = None
    else:
        graphicCards_onces = GraphicCard.objects.get(pk=cpu)
        graphicCards = None


    if disqueDur == 0:
        disqueDurs = DisqueDur.objects.all()
        disqueDurs_onces = None
    else:
        disqueDurs_onces = DisqueDur.objects.get(pk=cpu)
        disqueDurs = None

    

    if case == 0:
        cases = Case.objects.all()
        cases_onces = None
    else:
        cases_onces = Case.objects.get(pk=cpu)
        cases = None


    if powerSupply == 0:
        powerSupplys = PowerSupply.objects.all()
        powerSupplys_onces = None
    else:
        powerSupplys_onces = PowerSupply.objects.get(pk=cpu)
        powerSupplys = None



    if soundCard == 0:
        soundCards = SoundCard.objects.all()
        soundCards_onces = None
    else:
        soundCards_onces = SoundCard.objects.get(pk=cpu)
        soundCards = None


    if networkCard == 0:
        networkCards = NetworkCard.objects.all()
        networkCards_onces = None
    else:
        networkCards_onces = NetworkCard.objects.get(pk=cpu)
        networkCards = None

    prix = 4500

    return render(request, "client/conf_pc1.html", {
        'cpus':cpus,
        'fans':fans,
        'motherboards':motherboards,
        'rams':rams,
        'graphicCards':graphicCards,
        'disqueDurs':disqueDurs,
        'cases':cases,
        'powerSupplys':powerSupplys,
        'soundCards':soundCards,
        'networkCards':networkCards,

        'cpus_onces':cpus_onces,
        'fans_onces':fans_onces,
        'motherboards_onces':motherboards_onces,
        'rams_onces':rams_onces,
        'graphicCards_onces':graphicCards_onces,
        'disqueDurs_onces':disqueDurs_onces,
        'cases_onces':cases_onces,
        'powerSupplys_onces':powerSupplys_onces,
        'soundCards_onces':soundCards_onces,
        'networkCards_onces':networkCards_onces,

        'prix':prix,
    })

def fanselected(request):
    id=request.session.get('id',0)
   
    fan=0
    motherboard=0
    ram=0
    graphicCard=0
    disqueDur=0
    case=0
    powerSupply=0
    soundCard=0
    networkCard=0
    
    
    cpus_onces = CPU.objects.get(pk=4)
    print(cpus_onces)
    cpus = None

    cpu = 0
    
    fans_onces = Fan.objects.get(pk=19)
    fans = None

    if motherboard == 0:
        motherboards = Motherboard.objects.all()
        motherboards_onces = None
    else:
        motherboards_onces = Motherboard.objects.get(pk=cpu)
        motherboards = None


    if ram == 0:
        rams = RAM.objects.all()
        rams_onces = None
    else:
        rams_onces = RAM.objects.get(pk=cpu)
        rams = None


    if graphicCard == 0:
        graphicCards = GraphicCard.objects.all()
        graphicCards_onces = None
    else:
        graphicCards_onces = GraphicCard.objects.get(pk=cpu)
        graphicCards = None


    if disqueDur == 0:
        disqueDurs = DisqueDur.objects.all()
        disqueDurs_onces = None
    else:
        disqueDurs_onces = DisqueDur.objects.get(pk=cpu)
        disqueDurs = None

    

    if case == 0:
        cases = Case.objects.all()
        cases_onces = None
    else:
        cases_onces = Case.objects.get(pk=cpu)
        cases = None


    if powerSupply == 0:
        powerSupplys = PowerSupply.objects.all()
        powerSupplys_onces = None
    else:
        powerSupplys_onces = PowerSupply.objects.get(pk=cpu)
        powerSupplys = None



    if soundCard == 0:
        soundCards = SoundCard.objects.all()
        soundCards_onces = None
    else:
        soundCards_onces = SoundCard.objects.get(pk=cpu)
        soundCards = None


    if networkCard == 0:
        networkCards = NetworkCard.objects.all()
        networkCards_onces = None
    else:
        networkCards_onces = NetworkCard.objects.get(pk=cpu)
        networkCards = None

    prix = 7590

    return render(request, "client/conf_pc2.html", {
        'cpus':cpus,
        'fans':fans,
        'motherboards':motherboards,
        'rams':rams,
        'graphicCards':graphicCards,
        'disqueDurs':disqueDurs,
        'cases':cases,
        'powerSupplys':powerSupplys,
        'soundCards':soundCards,
        'networkCards':networkCards,

        'cpus_onces':cpus_onces,
        'fans_onces':fans_onces,
        'motherboards_onces':motherboards_onces,
        'rams_onces':rams_onces,
        'graphicCards_onces':graphicCards_onces,
        'disqueDurs_onces':disqueDurs_onces,
        'cases_onces':cases_onces,
        'powerSupplys_onces':powerSupplys_onces,
        'soundCards_onces':soundCards_onces,
        'networkCards_onces':networkCards_onces,

        'prix':prix,
    })


def moderselected(request):
    id=request.session.get('id',0)
   
    fan=0
    motherboard=0
    ram=0
    graphicCard=0
    disqueDur=0
    case=0
    powerSupply=0
    soundCard=0
    networkCard=0
    
    
    cpus_onces = CPU.objects.get(pk=4)
    print(cpus_onces)
    cpus = None

    cpu = 0
    
    fans_onces = Fan.objects.get(pk=19)
    fans = None

    
    motherboards_onces = Motherboard.objects.get(pk=6)
    motherboards = None


    if ram == 0:
        rams = RAM.objects.all()
        rams_onces = None
    else:
        rams_onces = RAM.objects.get(pk=cpu)
        rams = None


    if graphicCard == 0:
        graphicCards = GraphicCard.objects.all()
        graphicCards_onces = None
    else:
        graphicCards_onces = GraphicCard.objects.get(pk=cpu)
        graphicCards = None


    if disqueDur == 0:
        disqueDurs = DisqueDur.objects.all()
        disqueDurs_onces = None
    else:
        disqueDurs_onces = DisqueDur.objects.get(pk=cpu)
        disqueDurs = None

    

    if case == 0:
        cases = Case.objects.all()
        cases_onces = None
    else:
        cases_onces = Case.objects.get(pk=cpu)
        cases = None


    if powerSupply == 0:
        powerSupplys = PowerSupply.objects.all()
        powerSupplys_onces = None
    else:
        powerSupplys_onces = PowerSupply.objects.get(pk=cpu)
        powerSupplys = None



    if soundCard == 0:
        soundCards = SoundCard.objects.all()
        soundCards_onces = None
    else:
        soundCards_onces = SoundCard.objects.get(pk=cpu)
        soundCards = None


    if networkCard == 0:
        networkCards = NetworkCard.objects.all()
        networkCards_onces = None
    else:
        networkCards_onces = NetworkCard.objects.get(pk=cpu)
        networkCards = None

    prix = 120900

    return render(request, "client/conf_pc3.html", {
        'cpus':cpus,
        'fans':fans,
        'motherboards':motherboards,
        'rams':rams,
        'graphicCards':graphicCards,
        'disqueDurs':disqueDurs,
        'cases':cases,
        'powerSupplys':powerSupplys,
        'soundCards':soundCards,
        'networkCards':networkCards,

        'cpus_onces':cpus_onces,
        'fans_onces':fans_onces,
        'motherboards_onces':motherboards_onces,
        'rams_onces':rams_onces,
        'graphicCards_onces':graphicCards_onces,
        'disqueDurs_onces':disqueDurs_onces,
        'cases_onces':cases_onces,
        'powerSupplys_onces':powerSupplys_onces,
        'soundCards_onces':soundCards_onces,
        'networkCards_onces':networkCards_onces,

        'prix':prix,
    })


def ramselected(request):
    id=request.session.get('id',0)
   
    fan=0
    motherboard=0
    ram=0
    graphicCard=0
    disqueDur=0
    case=0
    powerSupply=0
    soundCard=0
    networkCard=0
    
    
    cpus_onces = CPU.objects.get(pk=4)
    print(cpus_onces)
    cpus = None

    cpu = 0
    
    fans_onces = Fan.objects.get(pk=19)
    fans = None

    
    motherboards_onces = Motherboard.objects.get(pk=6)
    motherboards = None


    
    rams_onces = RAM.objects.get(pk=7)
    rams = None


    if graphicCard == 0:
        graphicCards = GraphicCard.objects.all()
        graphicCards_onces = None
    else:
        graphicCards_onces = GraphicCard.objects.get(pk=cpu)
        graphicCards = None


    if disqueDur == 0:
        disqueDurs = DisqueDur.objects.all()
        disqueDurs_onces = None
    else:
        disqueDurs_onces = DisqueDur.objects.get(pk=cpu)
        disqueDurs = None

    

    if case == 0:
        cases = Case.objects.all()
        cases_onces = None
    else:
        cases_onces = Case.objects.get(pk=cpu)
        cases = None


    if powerSupply == 0:
        powerSupplys = PowerSupply.objects.all()
        powerSupplys_onces = None
    else:
        powerSupplys_onces = PowerSupply.objects.get(pk=cpu)
        powerSupplys = None



    if soundCard == 0:
        soundCards = SoundCard.objects.all()
        soundCards_onces = None
    else:
        soundCards_onces = SoundCard.objects.get(pk=cpu)
        soundCards = None


    if networkCard == 0:
        networkCards = NetworkCard.objects.all()
        networkCards_onces = None
    else:
        networkCards_onces = NetworkCard.objects.get(pk=cpu)
        networkCards = None

    prix = 17000

    return render(request, "client/conf_pc4.html", {
        'cpus':cpus,
        'fans':fans,
        'motherboards':motherboards,
        'rams':rams,
        'graphicCards':graphicCards,
        'disqueDurs':disqueDurs,
        'cases':cases,
        'powerSupplys':powerSupplys,
        'soundCards':soundCards,
        'networkCards':networkCards,

        'cpus_onces':cpus_onces,
        'fans_onces':fans_onces,
        'motherboards_onces':motherboards_onces,
        'rams_onces':rams_onces,
        'graphicCards_onces':graphicCards_onces,
        'disqueDurs_onces':disqueDurs_onces,
        'cases_onces':cases_onces,
        'powerSupplys_onces':powerSupplys_onces,
        'soundCards_onces':soundCards_onces,
        'networkCards_onces':networkCards_onces,

        'prix':prix,
    })

def graphselecte(request):
    id=request.session.get('id',0)
   
    fan=0
    motherboard=0
    ram=0
    graphicCard=0
    disqueDur=0
    case=0
    powerSupply=0
    soundCard=0
    networkCard=0

    cpus_onces = CPU.objects.get(pk=4)
    print(cpus_onces)
    cpus = None

    cpu = 0
    
    fans_onces = Fan.objects.get(pk=19)
    fans = None

    
    motherboards_onces = Motherboard.objects.get(pk=6)
    motherboards = None


    
    rams_onces = RAM.objects.get(pk=7)
    rams = None


    
    graphicCards_onces = GraphicCard.objects.get(pk=8)
    graphicCards = None


    if disqueDur == 0:
        disqueDurs = DisqueDur.objects.all()
        disqueDurs_onces = None
    else:
        disqueDurs_onces = DisqueDur.objects.get(pk=cpu)
        disqueDurs = None

    

    if case == 0:
        cases = Case.objects.all()
        cases_onces = None
    else:
        cases_onces = Case.objects.get(pk=cpu)
        cases = None


    if powerSupply == 0:
        powerSupplys = PowerSupply.objects.all()
        powerSupplys_onces = None
    else:
        powerSupplys_onces = PowerSupply.objects.get(pk=cpu)
        powerSupplys = None



    if soundCard == 0:
        soundCards = SoundCard.objects.all()
        soundCards_onces = None
    else:
        soundCards_onces = SoundCard.objects.get(pk=cpu)
        soundCards = None


    if networkCard == 0:
        networkCards = NetworkCard.objects.all()
        networkCards_onces = None
    else:
        networkCards_onces = NetworkCard.objects.get(pk=cpu)
        networkCards = None

    prix = 280030

    return render(request, "client/conf_pc4.html", {
        'cpus':cpus,
        'fans':fans,
        'motherboards':motherboards,
        'rams':rams,
        'graphicCards':graphicCards,
        'disqueDurs':disqueDurs,
        'cases':cases,
        'powerSupplys':powerSupplys,
        'soundCards':soundCards,
        'networkCards':networkCards,

        'cpus_onces':cpus_onces,
        'fans_onces':fans_onces,
        'motherboards_onces':motherboards_onces,
        'rams_onces':rams_onces,
        'graphicCards_onces':graphicCards_onces,
        'disqueDurs_onces':disqueDurs_onces,
        'cases_onces':cases_onces,
        'powerSupplys_onces':powerSupplys_onces,
        'soundCards_onces':soundCards_onces,
        'networkCards_onces':networkCards_onces,

        'prix':prix,
    })