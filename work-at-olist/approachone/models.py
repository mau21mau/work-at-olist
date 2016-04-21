from django.db import models
from workatolist import utils

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

    def override_categories(self, file_path):
        """ Given a csv file, it will override Channel's category_set with the categories on it. """
        flat_tree = utils.flat_tree_from_csv(file_path)
        self.category_set.all().delete()
        # If the first row is the column head/title it will skip the first loop iteration.
        if len(flat_tree[0]) > 0:
            if flat_tree[0][0] == 'Category':
                start_loop_at = 1

        inserted = []  # holds the entries already saved as categories
        next_parent = None
        parents = []
        saved_categories = []
        for i in range(start_loop_at, len(flat_tree)):
            current_row = flat_tree[i]
            saved_categories_row = []
            for j in range(0, len(current_row)):
                column = current_row[j]
                # if the current row contains only one entry, it means it's a root node
                if len(current_row) == 1:
                    category = Category(name=column)
                    category.save()
                    self.category_set.add(category)
                    saved_categories_row.append(category)
                else:
                    index_parent = current_row.index(column) - 1
                    # Parent from this entry on the current path
                    strparent = current_row[index_parent] if index_parent >= 0 else None
                    path = []
                    if strparent:
                        path.append(strparent)
                    path.append(column)
                    # check if the current entry was not saved yet.
                    if i-2 < 0 or j-1 < 0:
                        parent = None
                    else:
                        parent = utils.try_catch_index(saved_categories, [i - 2, j - 1])

                    if not utils.is_in(path, inserted):
                        category = Category(name=column, parent=parent)
                        category.save()
                        self.category_set.add(category)
                        saved_categories_row.append(category)
                    else:
                        previous_row = utils.try_catch_index(saved_categories, [i-2], [])
                        for saved_category in previous_row:
                            if saved_category.name == column:
                                saved_categories_row.append(saved_category)
                                break
            saved_categories.append(saved_categories_row)
            inserted.append(current_row)
