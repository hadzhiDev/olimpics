from django.contrib import admin

from account.models import Application, ProgramingLanguage, SendRequestToEmail


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'phone', 'language',)
    list_display_links = ('id', 'full_name',)
    search_fields = ('id', 'full_name', 'email', 'phone',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(ProgramingLanguage)
class ProgramingLanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(SendRequestToEmail)
class SendRequestToEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'expire_date',)
    list_display_links = ('id', 'application',)
    list_filter = ('application',)
    readonly_fields = ('key', 'created_at', 'updated_at',)
    raw_id_fields = ('application',)
