from django.conf import settings
from django.db import models
from workatolist import utils


class Category(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def id_key(self):
        return utils.encrypt(settings.SECRET_KEY, '%d' % self.id)

    @staticmethod
    def category_from_key(key):
        dbid = utils.decrypt(settings.SECRET_KEY, key)
        return Category.objects.get(pk=dbid)

    def has_children(self):
        children = Category.objects.filter(parent=self)
        return True if children.count() > 0 else False

    def children(self):
        return Category.objects.filter(parent=self)

    def get_tree(self):
        tree = self.get_children_recursive()
        tree['data']['relationships']['parents'] = self.get_parents_recursive()
        return tree

    def get_children_recursive(self):
        """
        Generates a tree of categories
        This approach is simple and elegant, but it's inefficient for 2 reasons:
        1) because for each recursion performs a database query.
        2) recursion usually is inefficient cause for each recursion tha language generates an instance of the function
        """

        children = self.children()
        tree = {
            'data': {
                'type': 'category',
                'uuid': self.id_key().decode("utf-8"),
                'attributes': {
                    'name': self.name,
                },
                'relationships': {
                    'children': [],
                    'parents': [],
                }
            }
        }
        for child in children:
            tree['data']['relationships']['children'].append(child.get_children_recursive())
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
        return utils.encrypt(settings.SECRET_KEY, '%d' % self.id)

    @staticmethod
    def channel_from_key(key):
        dbid = utils.decrypt(settings.SECRET_KEY, key)
        return Channel.objects.get(pk=dbid)

    def root_categories(self):
        return self.category_set.filter(parent__isnull=True)
