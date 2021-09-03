from django.contrib import (
    admin,
    messages,
)

from .models import (
    Friend,
    FriendList
)
from .utils import export_to_xlsx


def action_export_to_xlsx(modeladmin, request, queryset):
    full_filepath = export_to_xlsx(queryset)
    modeladmin.message_user(
        request,
        f'Spreadsheet successfully exported to: {full_filepath}',
        messages.SUCCESS,
    )

action_export_to_xlsx.short_description = "Export to Excel Spreadsheet"


@admin.register(FriendList)
class FriendListAdmin(admin.ModelAdmin):
    actions = (action_export_to_xlsx,)


admin.site.register(Friend)