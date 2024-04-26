from django.contrib import admin

from .models import Company, Share, Data, Portfolio, Composed_of

admin.site.register(Company)
admin.site.register(Share)
admin.site.register(Data)
admin.site.register(Portfolio)
admin.site.register(Composed_of)
