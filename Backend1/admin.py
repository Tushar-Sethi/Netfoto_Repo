from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Post)
admin.site.register(models.Category)
admin.site.register(models.People)
admin.site.register(models.Images)
admin.site.register(models.Comment)
admin.site.register(models.ProductAvailability)
admin.site.register(models.product_details)
admin.site.register(models.Claim_free_photos_questions)

