from rest_framework import serializers
from approachtwo.models import Channel, Category


class CategorySerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('data',)

    def get_data(self, instance):
        return {
            "type": "Category",
            "uuid": instance.id_key(),
            "attributes": {
                "name": instance.name,
            },
            "relationships": {
                "children": self.get_children_recursive(),
            },
        }

    def get_children_recursive(self, child=None):
        """
        Generates a tree of categories structured according to JSON API standards.
        """
        if not child:
            children = self.instance.get_children()
            category = self.instance
        else:
            children = child.get_children()
            category = child
        tree = {
            'data': {
                'type': 'category',
                'uuid': category.id_key(),
                'attributes': {
                    'name': category.name,
                },
                'relationships': {
                    'children': [],
                    'parents': [],
                }
            }
        }
        for child in children:
            tree['data']['relationships']['children'].append(self.get_children_recursive(child))
        return tree


class ChannelSerializer(serializers.ModelSerializer):
    category_set = CategorySerializer(many=True)

    class Meta:
        model = Channel
        fields = ('id_key', 'name', 'category_set')

