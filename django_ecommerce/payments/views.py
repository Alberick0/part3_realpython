import socket
import datetime

import stripe
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

import django_ecommerce.settings as settings
from .forms import SigninForm, CardForm, UserForm
from .models import User, UnPaidUsers

stripe.api_key = settings.STRIPE_SECRET


def soon():
    soon = datetime.date.today() + datetime.timedelta(days=30)
    return {'month': soon.month, 'year': soon.year}


def sign_in(request):
    user = None

    if request.method == 'POST':
        form = SigninForm(request.POST)

        if form.is_valid():
            results = User.objects.filter(email=form.cleaned_data['email'])

            if len(results) == 1:
                if results[0].check_password(form.cleaned_data['password']):
                    request.session['user'] = results[0].pk

                    return HttpResponseRedirect('/')

                else:
                    form.addError('Incorrect email or password')

            else:
                form.addError('Incorrect email address or password')

    else:
        form = SigninForm()

    return render_to_response('sign_in.html', {'form': form, 'user': user},
                              context_instance=RequestContext(request))


def sign_out(request):
    try:
        del request.session['user']
    except KeyError:
        pass

    return HttpResponseRedirect('/')


def register(request):
    user = None

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            #  update based on your billing method (subscription vs one time)
            cd = form.cleaned_data

            customer = Customer.create(
                email=form.cleaned_data['email'],
                description=form.cleaned_data['name'],
                card=form.cleaned_data['stripe_token'],
                plan='gold',
            )

            # customer = stripe.Charge.create(
            # description = form.cleaned_data['email'],
            # card = form.cleaned_data['stripe_token'],
            # amount="5000",
            # currency="usd"
            # )

            # The part above creates the new user

            try:
                with transaction.atomic():
                    user = User.create(
                        cd['name'],
                        cd['email'],
                        cd['password'],
                        cd['last_4_digits'],
                        stripe_id=''
                    )

                    if customer:
                        user.stripe_id = customer.id
                        user.save()
                    else:
                        UnPaidUsers(email=cd['email']).save()

            except IntegrityError:
                import traceback

                form.addError(cd['email'] + 'is already a member' +
                              traceback.format_exc())
                user = None
            else:
                request.session['user'] = user.pk
                return HttpResponseRedirect('/')

    else:
        form = UserForm()

    return render_to_response(
        'register.html',
        {
            'form': form,
            'months': list(range(1, 12)),
            'publishable': settings.STRIPE_PUBLISHABLE,
            'soon': soon(),
            'user': user,
            'years': list(range(2011, 2036)),
        },
        context_instance=RequestContext(request)
    )


def edit(request):
    uid = request.session.get('user')

    if uid is None:
        return HttpResponseRedirect('/')

    user = User.objects.get(pk=uid)

    if request.method == 'POST':
        form = CardForm(request.POST)

        if form.is_valid():
            customer = stripe.Customer.retrieve(user.stripe_id)
            customer.card = form.cleaned_data['stripe_token']
            customer.save()
            user.last_4_digits = form.cleaned_data['stripe_token']
            user.stripe_id = customer.id
            user.save()

            return HttpResponseRedirect('/')
    else:
        form = CardForm()

    return render_to_response(
        'edit.html', {'form': form,
                      'publishable': settings.STRIPE_PUBLISHABLE,
                      'soon': soon(), 'months': range(1, 12),
                      'years': range(2011, 2036)},
        context_instance=RequestContext(request)
    )


class Customer(object):
    @classmethod
    def create(cls, billing_method='subscription', **kwargs):
        try:
            if billing_method == 'subscription':
                return stripe.Customer.create(**kwargs)
            elif billing_method == 'one_time':
                return stripe.Charge.create(**kwargs)
        except socket.error:
            return None
