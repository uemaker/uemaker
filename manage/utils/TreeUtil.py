from manage.models import Category

class TreeUtil(object):

    @staticmethod
    def getChildNode(id):
        childNode = []
        list = Category.objects.filter(pid=id)
        if list.count()>0:
            for item in list:
                childNode.append({'id': item.id, 'name': item.name, 'title': item.title, 'sort': item.sort, 'children': self.getChildNode(item.id)})

        return childNode

    @staticmethod
    def getChildNodeTree(id, level=''):
        childNode = []
        tag = '--'
        list = Category.objects.filter(pid=id)
        if len(list):
            for item in list:
                childNode.append([item.id, level+tag + item.title])
                children = TreeUtil.getChildNodeTree(item.id, level+tag)
                if children and len(children):
                    childNode.extend(children)
        return childNode