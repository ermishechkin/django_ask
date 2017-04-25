# -*- coding: utf8

from django.conf import settings

class PaginatorError(Exception):
    def __init__(self, arg):
        self.arg = arg
    def __unicode__(self):
        return self.arg


def paginate(question_list, page, obj_per_page=10):
    page_visible = int(settings.PAGE_VISIBLE)
    page_total = int(len(question_list) / obj_per_page)
    if len(question_list) % obj_per_page > 0:
        page_total = page_total + 1
    obj_total = int(len(question_list))
    page_current = int(page)

    if page_total == 0 and page_current == 1:
        return ([],[])
    if page_current < 1 or page_current > page_total:
        raise PaginatorError("Bad page's index")

    page_end = page_current + int(page_visible / 2)
    if page_end > page_total:
        page_end = page_total

    page_begin = page_current - (page_visible - (page_end - page_current))
    if page_begin < 1:
        page_begin = 1

    page_end += page_visible - (page_end-page_begin)
    if page_end > page_total:
        page_end = page_total

    obj_begin = (page_current - 1) * obj_per_page
    obj_end = obj_begin + obj_per_page
    if obj_end > obj_total:
        obj_end = obj_total

    objs = question_list[obj_begin:obj_end]

    pages = [ { 'index' : i, 'active' : i == page_current } \
        for i in range(page_begin, page_end + 1)]

    return (objs, pages)
