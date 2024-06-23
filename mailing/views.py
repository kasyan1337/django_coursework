import random

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Blog
from .forms import ClientForm, MessageForm, MailingForm
from .models import Client, Message, Mailing, CustomUser

User = get_user_model()


def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(is_active=True).count()
    unique_clients = Client.objects.values('email').distinct().count()

    # Get all blog articles and select 3 random ones
    all_articles = list(Blog.objects.all())
    random_articles = random.sample(all_articles, min(len(all_articles), 3))

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'random_articles': random_articles,
        'can_view_users': request.user.has_perm('mailing.view_customuser'),
        'is_manager': is_manager(request.user),
    }

    return render(request, 'mailing/home.html', context)


def is_manager(user):
    return user.groups.filter(name='managers').exists()


@login_required
def user_list(request):
    if request.user.has_perm('mailing.view_customuser'):
        users = CustomUser.objects.all
        return render(request, 'mailing/user_list.html',
                      {'users': users, 'can_view_users': request.user.has_perm('mailing.view_customuser'),
                       'is_manager': is_manager(request.user), })
    else:
        return HttpResponseForbidden("You do not have permission to view this page.")


@login_required
def block_user(request, user_id):
    if request.user.has_perm('mailing.change_customuser'):
        user = get_object_or_404(User, pk=user_id)
        user.is_active = False
        user.save()
        return redirect('mailing:user_list')
    else:
        return HttpResponseForbidden("You do not have permission to perform this action.")


@login_required
def unblock_user(request, user_id):
    if request.user.has_perm('mailing.change_customuser'):
        user = get_object_or_404(User, pk=user_id)
        user.is_active = True
        user.save()
        return redirect('mailing:user_list')
    else:
        return HttpResponseForbidden("You do not have permission to perform this action.")


@login_required
def disable_mailing(request, pk):
    if request.user.is_staff or is_manager(request.user):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_active = False
        mailing.save()
        return redirect('mailing:mailing_list')


def enable_mailing(request, pk):
    if request.user.is_staff or is_manager(request.user):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_active = True
        mailing.save()
        return redirect('mailing:mailing_list')


# CRUD FOR USER

@login_required
def client_list(request):
    if request.user.is_staff:
        clients = Client.objects.all()
    elif is_manager(request.user):
        clients = Client.objects.all()
    else:
        clients = Client.objects.filter(owner=request.user)

    return render(request, 'mailing/client_list.html', {
        'clients': clients,
        'is_manager': is_manager(request.user),
        'can_view_users': request.user.has_perm('mailing.view_customuser')
    })


@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        # Form can be invalid if the data submitted in the form does not pass the validation checks defined in the form.
        # For example, if a required field is missing or
        # if an email field contains an improperly formatted email address
        if form.is_valid():
            client = form.save(commit=False)  # Don't save yet, only create the object, otherwise IntegrityError
            client.owner = request.user  # Set the owner
            client.save()  # Now it can be saved without IntegrityError
            return redirect('mailing:client_list')
    else:
        form = ClientForm()  # Creates blank form for the user to fill in
    return render(request, 'mailing/client_form.html',
                  {'form': form, 'can_view_users': request.user.has_perm('mailing.view_customuser'),
                   'is_manager': is_manager(request.user)})


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)  # better use get_object_or_404 if no such client exists
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('mailing:client_list')
    else:
        form = ClientForm(instance=client)

    return render(request, 'mailing/client_form.html', {
        'form': form,
        'can_save': request.user.has_perm('mailing.change_client'),
        'can_view_users': request.user.has_perm('mailing.view_customuser'),
        'is_manager': is_manager(request.user),
    })


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('mailing:client_list')
    return render(request, 'mailing/client_confirm_delete.html',
                  {'client': client, 'can_view_users': request.user.has_perm('mailing.view_customuser'),
                   'is_manager': is_manager(request.user)})


# CRUD FOR MESSAGE

@login_required
def message_list(request):
    if request.user.is_staff:
        messages = Message.objects.all()
    elif is_manager(request.user):
        messages = Message.objects.all()
    else:
        messages = Message.objects.filter(owner=request.user)

    return render(request, 'mailing/message_list.html', {
        'messages': messages,
        'is_manager': is_manager(request.user),
        'can_view_users': request.user.has_perm('mailing.view_customuser'),
    })


@login_required
def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)  # Don't save yet, only create the object, otherwise IntegrityError
            message.owner = request.user  # Set the owner
            message.save()  # Now it can be saved without IntegrityError
            return redirect('mailing:message_list')
    else:
        form = MessageForm()
    return render(request, 'mailing/message_form.html',
                  {'form': form, 'can_view_users': request.user.has_perm('mailing.view_customuser'),
                   'is_manager': is_manager(request.user), })


@login_required
def message_update(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('mailing:message_list')
    else:
        form = MessageForm(instance=message)

    return render(request, 'mailing/message_form.html', {
        'form': form,
        'can_save': request.user.has_perm('mailing.change_message'),
        'can_view_users': request.user.has_perm('mailing.view_customuser'), 'is_manager': is_manager(request.user),
    })


@login_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('mailing:message_list')
    return render(request, 'mailing/message_confirm_delete.html',
                  {'message': message, 'can_view_users': request.user.has_perm('mailing.view_customuser'),
                   'is_manager': is_manager(request.user)})


# CRUD FOR MAILING

@login_required
def mailing_list(request):
    if request.user.is_staff or is_manager(request.user):
        mailings = Mailing.objects.all()
    else:
        mailings = Mailing.objects.filter(owner=request.user, is_active=True)

    return render(request, 'mailing/mailing_list.html',
                  {'mailings': mailings, 'is_manager': is_manager(request.user),
                   'can_view_users': request.user.has_perm('mailing.view_customuser')})


@login_required
def mailing_create(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)  # the form.save(commit=False) line is used to create a Mailing object
            # from the form's data without saving it to the database yet.
            # This is done because we need to add the owner field manually, which is not included in the form.
            mailing.owner = request.user  # Here I set the owner
            mailing.save()  # Here I can finally save it to the database
            form.save_m2m()  # The form.save_m2m() line is used to save the many-to-many relationships.
            # In Django, when you have a form with a ManyToManyField, the many-to-many data can't be saved directly
            # from the form because it requires the instance to be saved first.
            # So, form.save_m2m() is called after the instance is saved to handle the saving of the many-to-many data.
            return redirect('mailing:mailing_list')
    else:
        form = MailingForm()
    return render(request, 'mailing/mailing_form.html',
                  {'form': form, 'can_view_users': request.user.has_perm('mailing.view_customuser'),
                   'is_manager': is_manager(request.user), })


@login_required
def mailing_update(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == 'POST':
        form = MailingForm(request.POST, instance=mailing)  # populate the form with the data of the existing mailing
        if form.is_valid():
            form.save()
            return redirect('mailing:mailing_list')
    else:
        form = MailingForm(instance=mailing)
    return render(request, 'mailing/mailing_form.html',
                  {'form': form, 'can_view_users': request.user.has_perm('mailing.view_customuser'),
                   'is_manager': is_manager(request.user)})


@login_required
def mailing_delete(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == 'POST':
        mailing.delete()
        return redirect('mailing:mailing_list')
    return render(request, 'mailing/mailing_confirm_delete.html',
                  {'mailing': mailing, 'can_view_users': request.user.has_perm('mailing.view_customuser'),
                   'is_manager': is_manager(request.user)})
