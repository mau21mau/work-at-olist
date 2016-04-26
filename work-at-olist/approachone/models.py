from django.conf import settings
from django.db import models
from workatolist import utils


class Category(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def id_key(self):
        return settings.KEY_RESOLVER.encrypt(b'%d' % self.id)

    @staticmethod
    def category_from_key(key):
        dbid = settings.KEY_RESOLVER.decrypt(bytes(key, encoding="utf-8"))
        return Category.objects.get(pk=dbid)

    def has_children(self):
        children = Category.objects.filter(parent=self)
        return True if children.count() > 0 else False

    def children(self):
        return Category.objects.filter(parent=self)

    def get_tree_recursive(self):
        """
        Generates a tree of categories
        This approach is simple and elegant, but it's inefficient for 2 reasons:
        1) because for each recursion performs a database query.
        2) recursion usually is inefficient cause for each recursion tha language generates an instance of the function
        """

        children = self.children()
        tree = {'name': self.name, 'children': []}
        for child in children:
            tree['children'].append(child.get_tree_recursive())

        return tree


class Channel(models.Model):
    name = models.CharField(max_length=100)
    category_set = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name

    def id_key(self):
        return settings.KEY_RESOLVER.encrypt(b'%d' % self.id)

    @staticmethod
    def channel_from_key(key):
        dbid = settings.KEY_RESOLVER.decrypt(bytes(key, encoding="utf-8"))
        return Channel.objects.get(pk=dbid)
