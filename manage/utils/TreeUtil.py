from manage.models import Category

class TreeUtil():

    def getChildNode(self, id):
        childNode = []
        list = Category.objects.filter(pid=id)
        if list.count()>0:
            for item in list:
                childNode.append({'id': item.id, 'name': item.name, 'title': item.title, 'sort': item.sort, 'children': self.getChildNode(item.id)})

        return childNode