from django.template.defaultfilters import register

censor_list = [
    'айтишник', 'богомол' , 'крапива'
]

@register.filter()
def censor(value):
    for word in censor_list:
        try:
            if not isinstance(str): # если аргумент не строкового типа, то вызывается исключение
                raise TypeError('Заменяемое значение должно быть строкой')
            return str(value).replace("*" * len(word))
        except TypeError as e:
            print(str(e))
            return value