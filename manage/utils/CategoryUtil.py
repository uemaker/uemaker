from manage.models import Category


class CategoryUtil(object):

    @staticmethod
    def getCategoryChilds(module_id, id=0):
        childNode = []
        list = Category.objects.filter(module_id=module_id, pid=id)
        if list.count() > 0:
            for item in list:
                childNode.append({'id': item.id, 'name': item.name, 'title': item.title, 'sort': item.sort,
                                  'children': CategoryUtil.getCategoryChilds(module_id, item.id)})

        return childNode

    @staticmethod
    def getCategoryList(module_id, id=0, level=0):
        tree = []
        tag = '|---'
        level += 1
        list = Category.objects.filter(module_id=module_id, pid=id).order_by('sort', 'id')
        if len(list):
            for item in list:
                data = {'id': item.id, 'name': item.name, 'title': item.title, 'sort': item.sort, }
                if id:
                    print(level)
                    data['title'] = (level-1) * tag + data['title']
                tree.append(data)
                children = CategoryUtil.getCategoryList(module_id, item.id, level)
                if children and len(children):
                    tree.extend(children)

        return tree

    @staticmethod
    def getCategoryTree(module_id, id, level='', top=''):
        tree = []
        tag = '--'
        list = Category.objects.filter(module_id=module_id, pid=id)
        has_top = False
        if top.strip() != '':
            has_top = True
            tree.append(['0', top])
        if len(list):
            for item in list:
                if not id and not has_top:
                    tree.append([item.id, item.title])
                else:
                    tree.append([item.id, level + tag + item.title])
                children = CategoryUtil.getCategoryTree(module_id, item.id, level + tag)
                if children and len(children):
                    tree.extend(children)
        return tree
