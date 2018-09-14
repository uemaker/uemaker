from manage.models import Category

class CategoryUtil(object):

    @staticmethod
    def getCategoryChilds(module_id, id):
        childNode = []
        list = Category.objects.filter(module_id=module_id, pid=id)
        if list.count() > 0:
            for item in list:
                childNode.append({'id': item.id, 'name': item.name, 'title': item.title, 'sort': item.sort, 'children': CategoryUtil.getChildNode(module_id, item.id)})

        return childNode

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
                    tree.append([item.id, level+tag + item.title])
                children = CategoryUtil.getCategoryTree(module_id, item.id, level+tag)
                if children and len(children):
                    tree.extend(children)
        return tree