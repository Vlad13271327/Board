import re
from django.template.defaultfilters import register

censor_list = ['айтишник', 'богомол', 'крапива']
censor_pattern = re.compile(rf'({"|".join(map(re.escape, censor_list))})', flags=re.IGNORECASE)


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError('Заменяемое значение должно быть строкой')

    # Замена совпадений на звездочки
    return censor_pattern.sub(lambda match: '*' * len(match.group()), value)