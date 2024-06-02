from django.views.generic import ListView
from django.core.paginator import Paginator
from colorfield.fields import ColorField
from django.db import models
from django.urls import path
from typing import Any
from . import isdarker,iswhiter,hex_to_rgb,brightness

# function django

def allpath(route: str, view, name: str):
    a = []
    if route[-1] == "/":
        a.append(path(route, view, name=name))
        a.append(path(route[:-1], view, name=name))
    else:
        a.append(path(route, view, name=name))
        a.append(path(route + "/", view, name=name))
    return a


# class django



class LBASE(ListView):
	context_paginator_name = "page"
	page_n=0

	def get_paginate_by(self, queryset) -> int | None:
		if len(queryset) >= self.page_n and self.page_n>0:
			return int(len(queryset) / self.page_n)
		else:
			return super().get_paginate_by(queryset)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.paginate_by!=None:
			paginator = Paginator(self.object_list, self.paginate_by)
			page_obj = self.request.GET.get('page')
			paginator = paginator.get_page(page_obj)
			context[self.context_paginator_name]=paginator.paginator.page_range
		return context

# class BModels:
class Color(models.Model):
    color=ColorField(verbose_name="цвет",default='#FF0000')
    
    class Meta:
        abstract = True
    def isdarker(self, porog):
        return isdarker(color=self.color,porog=porog)
    def iswhite(self,porog):
        return iswhiter(color=self.color,porog=porog)
    def hexrgb(self,HEX):
        return hex_to_rgb(HEX)
    def rgbtofloat(self,rgb):
        return brightness(rgb)
