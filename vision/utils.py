import random
import string

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        product_slug = new_slug
    else:
        product_slug = slugify(instance.product_title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(product_slug=product_slug).exists()
    if qs_exists:
        new_slug = "{product_slug}-{randstr}".format(
            product_slug=product_slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return product_slug