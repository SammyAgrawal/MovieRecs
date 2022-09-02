from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="profile_pics", blank=True, null=True)

    def __str__(self):
        return(self.user.username)

class Movie(models.Model):
    title = models.CharField(max_length=50)
    
    DRAMA = 'DR'; COMEDY = 'CO'; HORROR = 'HO'; ACTION = 'AC'; ROMANCE = 'RO';
    GENRE_CHOICES = [(DRAMA, 'Drama'), (COMEDY, 'Comedy'), (HORROR, 'Horror'), (ACTION, 'Action'),(ROMANCE, 'Romance')]
    genre = models.CharField(max_length=2, choices=GENRE_CHOICES, blank=True, null=True)

    def __str__(self):
        return(self.title)

    def get_average_rating(self):
        default_rating = 3.0
        rate_total = 0.0
        num_rate = 0.0
        for rating in self.rating_set.all():
            rate_total += rating.value
            num_rate +=1
        if(num_rate>0):
            return(rate_total/num_rate)
        else:
            return(default_rating)


class Rating(models.Model):
    value = models.IntegerField(default=3, validators=[MaxValueValidator(5), MinValueValidator(1)])
    rater = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return(f"Rating: {self.rater} x {self.movie}")