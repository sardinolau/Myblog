from django.contrib import admin
from blog import models
from django.utils.safestring import mark_safe  #可以使用html标签的模块
# Register your models here.
class UserConfig(admin.ModelAdmin):
    def deletes(self,*args):
        return mark_safe("<a href="">删除</a>")
    list_display = ["username","create_time","blog","deletes"]
    # list_display_links = ['blog']  #可以通过点击该字段进入编辑状态
    list_filter = ['create_time']

admin.site.register(models.UserInfo,UserConfig)
admin.site.register(models.Article)
admin.site.register(models.Blog)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Article2Tag)

