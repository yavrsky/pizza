import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.forms.formsets import formset_factory
from django.utils.text import slugify
from django.core.mail import send_mail
from django.http.response import HttpResponse

from .forms import *


ComponentFormSet = formset_factory(ComponentForm, extra=0)

class Constructor(View):
    def get(self, request):
        form_ingredient = IngredientForm()
        ingredients = []
        ing_titles = []
        fs_list = []
        for ing in Ingredient.objects.filter(type='num'):
            ing_len = len(ing.component_set.all())
            num_fields = [{'number':0} for i in range(ing_len)]
            labels = [i.name for i in ing.component_set.all()]
            prices = [i.price for i in ing.component_set.all()]

            fs = ComponentFormSet(initial=num_fields,
                                  prefix=slugify(ing.title))
            fs_list.append(fs)
            ing_titles.append((ing.title))
            ingredients.append(
                list(zip(fs, labels, prices))
            )

        zipper = list(zip(ingredients, ing_titles, fs_list))
        context = {
            'fs':  fs,
            'zipper': zipper,
            'form_ingredient': form_ingredient,
        }
        return render(request, 'pizza/index.html', context)

    def post(self, request):
        form_ingredient = IngredientForm(request.POST)
        num_ingredient = Ingredient.objects.filter(type='num')
        forms = []
        for ing in num_ingredient:
            forms.append(ComponentFormSet(
                                        request.POST,
                                        prefix=slugify(ing.title)
                                        )
                )

        url_order = ''
        total_price = 0
        for ing, form in zip(num_ingredient, forms):
            iterator = 0
            if form.is_valid():
                for comp, f in zip(ing.component_set.all(), form.cleaned_data):
                    print(comp.price, f['number'])
                    url_order += f'{slugify(ing.title)}-{iterator}={comp.price}+{f["number"]}&'
                    iterator += 1
                    total_price += comp.price * float(f['number'])
        url_order += str(total_price)
        utf_encoded = url_order.encode('utf-8')
        base64_encoded = base64.b64encode(utf_encoded)
        utf_decoded = base64_encoded.decode('utf-8')
        return redirect(f'order/{utf_decoded}')
        context = {
            'form': form,
            'total_price': total_price,
        }
        return render(request, 'pizza/index.html', {'form': form})

class OrderPizza(View):
    def get(self, request, url_order):

        utf_decoded = url_encode_decode(url_order)
        if utf_decoded == None:
            return redirect('constructor')
        total_price = utf_decoded.split('&')[-1]
        form = ContactForm()
        context = {
            'form': form,
            'url_order': url_order,
            'total_price': total_price,
        }
        return render(request, 'pizza/order.html', context)


def url_encode_decode(url):
    utf_encoded = url.encode('utf-8')
    base64_decoded = base64.b64decode(utf_encoded)

    try:
        utf_decoded = base64_decoded.decode('utf-8')
    except UnicodeDecodeError as e:
        return

    return utf_decoded

def send(request, url_order, total_price):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            person_name = form.cleaned_data['person_name']
            email = form.cleaned_data['email']
        else:
            for field in form:
                print(field.errors)
            print(form.errors)
            context = {
                'form': form,
                'url_order': url_order,
                'total_price': total_price,
            }
            return render(request, 'pizza/order.html', context)


        utf_decoded = url_encode_decode(url_order)
        splitted = utf_decoded.split('&')[:-1]

        num_ingredient = Ingredient.objects.filter(type='num')

        pizza = {}
        for s, ing in zip(splitted, num_ingredient):
            key, value = s.split('=')
            for i, v in zip(ing.component_set.all(), value):
                pizza[i.name] = value.split('+')

        tr = ''
        for i in pizza:
            tr += f'<tr><td>{i}</td><td>{pizza[str(i)][0]}</td><td>{pizza[str(i)][1]}</td></tr>'
        form_message = (f''' Hello, {person_name}
                    <table><tr><th>Ingredient</th><th>Price</th>
                            <th>Count</th></tr>{tr}
                      </table>
                      Total price: {total_price}''')


        message = Mail(
            from_email='vadim@yavorsky.com',
            to_emails=email,
            subject='Confirmation Pizza Order',
            html_content=form_message)

        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
        except Exception as e:
            print(e.message)
        return redirect('constructor')
