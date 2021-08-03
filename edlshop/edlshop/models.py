from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone


class User(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    
    is_client = models.BooleanField(default=False)
    is_trader = models.BooleanField(default=False)

    numCard = models.CharField(max_length=15,null=True)
    phoneNumber = models.CharField(max_length=15,null=True)
    address = models.TextField(null=True)
    imageProfile = models.FileField(upload_to='profile/', null=True)
    isBlocked = models.BooleanField(null=True,default=False)

    def __str__(self):
        if self.is_trader:
            type = "trander"
        else:
            type = "client"
        return self.first_name+" "+self.last_name+" ["+type+"]"

class Category (models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class Card(models.Model):
    cardNumber = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    mmyy = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class MoneyBack(models.Model):
    cardFrom = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='cardfrom')
    cardTo = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='cardto')
    price = models.FloatField()
    dateAdded = models.DateTimeField()

class Article(models.Model):
    name = models.CharField(max_length=255)
    shortDescription = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='image/')
    price = models.FloatField()
    delivery = models.FloatField()
    discount = models.FloatField()
    inStock = models.IntegerField()
    usernameTrader = models.ForeignKey(User, on_delete=models.CASCADE)
    dateAdded = models.DateTimeField(default=timezone.now)
    category = models.ManyToManyField(Category,related_name='category')
    mark = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class CPU(Article):
    processorModel = models.CharField(max_length=15)
    pocessorSupport = models.CharField(max_length=10)


class Fan(Article):
    processorSupport = models.CharField(max_length=255)
    Length = models.PositiveIntegerField()
    Width = models.PositiveIntegerField()


class Motherboard(Article):
    processorSupport = models.CharField(max_length=10)
    frequencyMemory = models.CharField(max_length=255)
    typeMemory = models.CharField(max_length=10)
    maximumRAMslot = models.PositiveIntegerField()
    slotNumber = models.PositiveIntegerField()
    connectorGraphic = models.CharField(max_length=255)
    audioChipset = models.CharField(max_length=10)
    networkStandard = models.CharField(max_length=255)
    Length = models.PositiveIntegerField()
    Width = models.PositiveIntegerField()


class RAM(Article):
    capacity = models.PositiveIntegerField()
    frequencyMemory = models.CharField(max_length=10)
    typeMemory = models.CharField(max_length=10)


class GraphicCard(Article):
    bus = models.CharField(max_length=30)
    videoMemorySize = models.PositiveIntegerField()
    typeMemory = models.CharField(max_length=30)
    Length = models.PositiveIntegerField()
    Width = models.PositiveIntegerField()


types = [
    ('SSD', 'ssd'),
    ('HDD', 'hdd')
]


class DisqueDur(Article):
    type = models.CharField(choices=types, max_length=30)
    capacity = models.PositiveIntegerField()


class Case(Article):
    maxLengthGraphicCard = models.PositiveIntegerField()
    maxHeightCPUfan = models.PositiveIntegerField()
    maxLengthPowerSupply = models.PositiveIntegerField()
    maxLengthMotherboard = models.PositiveIntegerField()


class PowerSupply(Article):
    Length = models.PositiveIntegerField()
    Width = models.PositiveIntegerField()


class SoundCard(Article):
    audioChipset = models.CharField(max_length=10)


class NetworkCard(Article):
    networkStandard = models.CharField(max_length=255)


class ShoppingCart(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    partNumber = models.IntegerField()
    price = models.FloatField()
    delivery = models.FloatField()


class Demand(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    dateAdded = models.DateTimeField(default=timezone.now)
    price = models.FloatField()
    delivery = models.FloatField()
    advancement = models.CharField(max_length=20)
    partNumber = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Notification(models.Model):
    dateAdded = models.DateTimeField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    vue = models.BooleanField()
    Text = models.TextField()
    image_url = models.URLField()
    url = models.URLField()


class Report(models.Model):
    usernameFrom = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    dateAdded = models.DateTimeField()


class UserReport(Report):
    usernameReported = models.ForeignKey(User, on_delete=models.CASCADE)


class ArticleReport(Report):
    articleRaported = models.ForeignKey(Article, on_delete=models.CASCADE)


class DemandReport(Report):
    demandRaported = models.ForeignKey(Demand, on_delete=models.CASCADE)


class TellMe(models.Model):
    usernameCustomer = models.ForeignKey(User, on_delete=models.CASCADE)
    articleId = models.ForeignKey(Article, on_delete=models.CASCADE)
    dateAdded = models.DateTimeField(default=timezone.now)


class Rate(models.Model):
    usernameUser = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()
    dateAdded = models.DateTimeField(default=timezone.now)


class ArticleRate(Rate):
    ArticleId = models.ForeignKey(Article, on_delete=models.CASCADE)


class TraderRate(Rate):
    usernameTrader = models.ForeignKey(User, on_delete=models.CASCADE)


class Favorite(models.Model):
    usernameCustomer = models.ForeignKey(User, on_delete=models.CASCADE)
    articleId = models.ForeignKey(Article, on_delete=models.CASCADE)
    dateAdded = models.DateTimeField()


class Review(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    dateAdded = models.DateTimeField()


class ArticleReview(Review):
    ArticleId = models.ForeignKey(Article, on_delete=models.CASCADE)


class TraderReview(Review):
    usernameTrader = models.ForeignKey(User, on_delete=models.CASCADE)


class Return(models.Model):
    dateAdded = models.DateTimeField(default=timezone.now)
    codeReturn = models.IntegerField()
    isAccepted = models.BooleanField(null=True,default=False)
    isConsulted = models.BooleanField(null=True,default=False)
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class SlideShow(models.Model):
    image = models.FileField(upload_to='slidshow/')
    url = models.CharField(max_length=255)


class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField(max_length=255)