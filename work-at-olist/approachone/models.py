from django.db import models


class Category(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=100)
    category_set = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name
