from django.contrib import admin
from .models import Haha, Dislike, Angry, Poop, Nauseated

class BaseReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_post_id', 'post')

    def get_post_id(self, obj):
        return obj.post.id if obj.post else None
    get_post_id.short_description = 'Post ID'

class HahaAdmin(BaseReactionAdmin):
    pass

class DislikeAdmin(BaseReactionAdmin):
    pass

class AngryAdmin(BaseReactionAdmin):
    pass

class PoopAdmin(BaseReactionAdmin):
    pass

class NauseatedAdmin(BaseReactionAdmin):
    pass

admin.site.register(Haha, HahaAdmin)
admin.site.register(Dislike, DislikeAdmin)
admin.site.register(Angry, AngryAdmin)
admin.site.register(Poop, PoopAdmin)
admin.site.register(Nauseated, NauseatedAdmin)
