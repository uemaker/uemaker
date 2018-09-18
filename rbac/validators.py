from django.utils.deconstruct import deconstructible
from django.core.validators import RegexValidator

@deconstructible
def UserNameValidator():
    regex = r'^[\w.@+-]+$'
    message = u'用户名格式错误,允许输入数字、大小写字母及+/-/_/./@ 等字符'
    flags = 0
