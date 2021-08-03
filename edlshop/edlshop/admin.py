from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name','email','password','phoneNumber','numCard','address','is_client','is_trader','isBlocked',)
admin.site.register(User,UserAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Card)
admin.site.register(MoneyBack)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','price','delivery','discount','inStock','usernameTrader','dateAdded','mark')
admin.site.register(Article,ArticleAdmin)
admin.site.register(CPU)
admin.site.register(Fan)
admin.site.register(Motherboard)
admin.site.register(RAM)
admin.site.register(GraphicCard)
admin.site.register(DisqueDur)
admin.site.register(Case)
admin.site.register(PowerSupply)
admin.site.register(SoundCard)
admin.site.register(NetworkCard)
admin.site.register(ShoppingCart)
admin.site.register(Demand)
admin.site.register(Notification)
admin.site.register(Report)
admin.site.register(UserReport)
admin.site.register(ArticleReport)
admin.site.register(DemandReport)
admin.site.register(TellMe)
admin.site.register(Rate)
admin.site.register(ArticleRate)
admin.site.register(TraderRate)
admin.site.register(Favorite)
admin.site.register(Review)
admin.site.register(ArticleReview)
admin.site.register(TraderReview)
admin.site.register(Return)
admin.site.register(SlideShow)
admin.site.register(ContactUs)

