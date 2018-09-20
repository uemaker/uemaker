
class ListUtil(object):

    @staticmethod
    def distinct(dict_list, key):
        key_arr = []
        if dict_list:
            for dict in dict_list:
                if dict.get(key) in key_arr:
                    dict_list.pop(dict)
                else:
                    key_arr.append(dict.get(key))
        return dict_list
