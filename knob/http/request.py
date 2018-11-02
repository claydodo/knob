# -*- coding:utf-8 -*-

import six
import json


def get_request_para(request, **kwargs):
    para = {}
    if request.method in ['POST', 'PUT', 'PATCH']:
        try:
            json_str = request.body.decode('utf-8') if six.PY3 else request.body
            json_para = json.loads(json_str, strict=False)
            if isinstance(json_para, dict):
                para.update(json_para)
        except Exception as e:
            pass
    para.update(request.GET.dict())

    for k, parser in six.iteritems(kwargs):
        if callable(parser) and k in para:
            para[k] = parser(para[k])

    return para
