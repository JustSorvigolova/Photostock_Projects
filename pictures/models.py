from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from photostock.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def all_count(self):
        return Picture.objects.filter(category=self.id).count()

    def __str__(self):
        return self.name


class Picture(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='images/', null=True, blank=False)
    small_picture = ImageSpecField(source='picture',
                                   processors=[ResizeToFill(480, 220)],
                                   format='JPEG',
                                   options={'quality': 100})
    description = models.TextField()

    def __str__(self):
        return self.title


#pic = Picture.objects.all()[0]
#print(pic.small_picture.url)
#print(pic.small_picture.width)
