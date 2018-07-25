# -*- coding:utf-8 -*-

import six
from django.db import models
from django.contrib.contenttypes.models import ContentType


def update_model(obj, info, fields=None):
    """
    Updates an object of Django model instance with given info, optionally limited to certain fields only.
    :param obj: a Django model instance
    :param info: a dict
    :param fields: optional, only update these fields.
    :return: updated obj (saved)
    """
    updated_fields = set()
    for key, val in six.iteritems(info):
        if fields is None or key in fields:
            setattr(obj, key, val)
        updated_fields.add(key)

    if updated_fields:
        obj.save(updated_fields=list(updated_fields))

    return obj


def get_model_class(model):
    """
    Deduct the model class from given input.
    :param model: a '<app>.<model>' string, or a django model instance, or a model class
    :return: django model class
    """
    if isinstance(model, six.string_types):
        if '.' in model:
            app_label, model_name = model.split('.')
            model_name = model_name.lower()
            return ContentType.objects.get(app_label=app_label, model=model_name)
        else:
            model_name = model.lower()
            return ContentType.objects.get(model=model_name)
    elif issubclass(model, models.Model):
        return model
    elif isinstance(model, models.Model):
        return model.__class__
    else:
        raise ValueError(u"Not a valid model representation: {}".format(repr(model)))