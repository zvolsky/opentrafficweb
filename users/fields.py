import binascii
import os
from django.db import models, DatabaseError
from django.utils.translation import gettext_lazy as _


def get_random_key():
    return binascii.hexlify(os.urandom(20)).decode()


class RandomUniqueKeyField(models.CharField):
    """
    A unique CharField with database index that generates a random string
    of length max_length as default value (new object). It is ensured that
    this value does not exist in the database.
    """
    description = _("Key of length %(max_length)s, unique in the database table.")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 40
        if 'unique' not in kwargs:
            kwargs['unique'] = True
        if 'db_index' not in kwargs and not kwargs['unique']:
            kwargs['db_index'] = True

        super(RandomUniqueKeyField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = super(RandomUniqueKeyField, self).pre_save(model_instance, add)
        if not value:
            value = self.generate_random_unique_key()
            setattr(model_instance, self.attname, value)
        return value

    def generate_random_unique_key(self):
        while True:
            key = get_random_key()
            if hasattr(self, 'model'):
                try:
                    # test the uniqueness
                    if not self.model.objects.filter(**{self.name: key}).exists():
                        return key
                except (DatabaseError, AttributeError):
                    # When the database returns error, we are either called from
                    # south and the table does not exist yet or there is other error.
                    # In both cases we delegate the problem to the later code.
                    return key
            else:
                # We're sometimes called during e.g. South migration without
                # model reference.
                return key

    def deconstruct(self):
        name, path, args, kwargs = super(RandomUniqueKeyField, self).deconstruct()
        return name, path, args, kwargs
