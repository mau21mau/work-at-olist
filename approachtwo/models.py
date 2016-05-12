from django.conf import settings
from workatolist import utils
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def id_key(self):
        return utils.encrypt(settings.SECRET_KEY, '%d' % self.id).decode("utf-8")

    @staticmethod
    def category_from_key(key):
        dbid = utils.decrypt(settings.SECRET_KEY, key)
        return Category.objects.get(pk=dbid)

    def get_tree(self):
        tree = self.get_children_recursive()
        tree['data']['relationships']['parents'] = self.get_parents_recursive()
        return tree

    def get_parents_recursive(self, parents=None):
        parent_attrs = {}
        parents = [] if not parents else parents
        if self.parent:
            parent_attrs['name'] = self.parent.name
            parent_attrs['uui'] = self.parent.id_key().decode("utf-8")
            parents.append(parent_attrs)
            self.parent.get_parents_recursive(parents)
        return parents


class Channel(models.Model):
    name = models.CharField(max_length=100)
    category_set = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name

    def id_key(self):
        return utils.encrypt(settings.SECRET_KEY, '%d' % self.id).decode("utf-8")

    @staticmethod
    def channel_from_key(key):
        dbid = utils.decrypt(settings.SECRET_KEY, key)
        return Channel.objects.get(pk=dbid)

    def root_category_set(self):
        return self.category_set.filter(parent=None)
