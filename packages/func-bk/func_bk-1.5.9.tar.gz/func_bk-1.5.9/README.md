add function 

sejango - 3 arguments form(django),key(in form cleaned data),var(return if key is not find)


adder - dict,**kwargs 
add to dict all arguments kwargs



iswhiter(color(HEX),porog) - color=color for checking, porog = threshold for lightening
isdarker(color(HEX),porog) - color=color for checking, porog = threshold for darkering
brighness(rgb(RGB)) - rgb to float
hex_to_rgb(hex_xolor(HEX)) - you know


find(lst,sim) - lst=list sim=obj for searching, find obj inlist and return he index
 
listrand(min,max,kol): return random list


IsKeyInDict(data, key): return bool: isvalid key in data



stepen(number,stepan): degree of number
	
faktorial(number): you know
	
chibo(number): number of chibonachi
	
summa(number):summ 
example:
    a=12
    print(summ(a))
this code return 3



call_methods_by_partial_name(class_instance, partial_name, *args, **kwargs): use all METHODS(function in class) with partial name


CFBPN=call_methods_by_partial_name
Mcall=call_methods_by_partial_name



call_functions_by_partial_name(partial_name, *args, **kwargs): use all function with partial name

CFBPN=call_functions_by_partial_name
Fcall=call_functions_by_partial_name

DJANGO:


function for django:


allpath(route: str, view, name: str): It is used to create a list of URL routes that support both the presence and absence of a trailing slash

example_1:
    urlpatterns = [
        path('', views.index, name='index'),
        *allpath('post/', views.post.as_view(), name='post'), ]

example_2:
    urlpatterns = [
        path('', views.index, name='index'),
        *allpath('post', views.post.as_view(), name='post'), ]

note: since it returns the list, you need to use * to unpack the list

class for django:


Color:
    abstract model
    for inheritance models add to model variable: color and function: isdarker, iswhite, hexrgb, rgbtofloat 


LBASE:
    
    add:
        context_paginator_name = name paginator for context
        page_n =  page-quantity for correct work need paginate_by
        page_n:
            if len(queryset)>=page_n:
                return (calculations for a given number of pages)
            else:
                return=paginate_by

    example:
    class index(LBASE):
        model=Tovar
        template_name="mains/icecream_list.html"
        context_object_name='date'
        paginate_by=5
        paginate_orphans=2
        page_n=5 ...


FAST_API:

path(): this is django path for fast api, He have args from FastAPI.get() or FastAPI.post etc, new arguments=
        app:your app FastAPI
        func:function from your FastAPI
        type:str, type:'get','post','put','delete','patch'(register is not important)
example:
    urls.py:
        from func_bk.fast_api import path
        from fastapi import FastAPI
        import main


        def initi(app: FastAPI):
            path(app,main.hello,'post','/')
    main.py:
        from fastapi import FastAPI, Request
        from urls import initi
        app=FastAPI()

        def hello():
            return 'hello world'
        
        initi(app)




BForm: class for inheritance form

Label: label for form

example:
    form.py:
        from fast_api import Label,BForm

        class form_user(BForm):
            num1=Label('number','num1')
            num2=Label('number','num2')
            def as_p(self):
                a=super().as_p()
                print(a)
                return a
    main.py:
        from fastapi import FastAPI, Request
        from fastapi.responses import HTMLResponse
        from fastapi.templating import Jinja2Templates
        from urls import url_init
        from form import *

        app=FastAPI()

        templates=Jinja2Templates(directory="html")
        

        async def calc(num1:int =Form(),num2:int=Form()):
            result=num1+num2
            return result


        def calc_get(request:Request):
            form = form_user()
            return templates.TemplateResponse('calc.html', context={'form': form, 'request': request})

        url_init(app)
        
    calc.html:
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>calc</title>
        </head>
        <body>
            <form method="post" action="/calc">
                {{ form.as_p() }}
                <button type="submit">Отправить</button>
            </form>
        </body>
        </html>

