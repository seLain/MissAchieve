from django.contrib import admin
from achievements.models import Mission, MissionProxy, KeywordMission

admin.site.register(Mission)
admin.site.register(MissionProxy)
admin.site.register(KeywordMission)