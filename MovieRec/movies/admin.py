from django.contrib import admin
from .models import UserProfile, Movie, Rating
# Register your models here.
models = [UserProfile, Movie, Rating]

for model in models:
    admin.site.register(model)

    