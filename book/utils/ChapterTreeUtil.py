from book.models import Chapter


class ChapterTreeUtil(object):

    @staticmethod
    def getChapterChilds(book_id, id=0):
        childNode = []
        list = Chapter.objects.filter(book_id=book_id, pid=id).values('id', 'pid', 'code', 'title', 'sort')
        if len(list) > 0:
            for item in list:
                childNode.append({'id': item['id'], 'code': item['code'], 'title': item['title'], 'sort': item['sort'],
                                  'children': ChapterTreeUtil.getChapterList(book_id, item['id'])})

        return childNode

    @staticmethod
    def getChapterList(book_id, id=0, level=0):
        tree = []
        tag = '|---'
        level += 1
        list = Chapter.objects.filter(book_id=book_id, pid=id).order_by('id').values('id', 'pid', 'code', 'title', 'sort')

        if len(list):
            for item in list:
                data = {'id': item['id'], 'code': item['code'], 'title': item['title'], 'sort': item['sort'], }
                if id:
                    data['title'] = (level-1) * tag + data['code'] + data['title']
                tree.append(data)
                children = ChapterTreeUtil.getChapterList(book_id, item['id'], level)
                if children and len(children):
                    tree.extend(children)

        return tree

    @staticmethod
    def getChapterTree(book_id, id, level='', top=''):
        tree = []
        tag = '--'
        list = Chapter.objects.filter(book_id=book_id, pid=id).values('id', 'pid', 'code', 'title', 'sort')
        has_top = False
        if top.strip() != '':
            has_top = True
            tree.append(['0', top])
        if len(list):
            for item in list:
                if not id and not has_top:
                    tree.append([item['id'], item['title']])
                else:
                    tree.append([item['id'], level + tag + item['code'] + item['title']])
                children = ChapterTreeUtil.getChapterTree(book_id, item['id'], level + tag)
                if children and len(children):
                    tree.extend(children)
        return tree

