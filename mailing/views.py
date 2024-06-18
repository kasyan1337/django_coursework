from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ClientForm, MessageForm, MailingForm
from .models import Client, Message, Mailing


def home(request):
    return render(request, 'mailing/home.html')

# CRUD FOR USER

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'mailing/client_list.html',  # needs to be created
                  {'clients': clients})  # context is a dictionary that is passed to the template


@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        # Form can be invalid if the data submitted in the form does not pass the validation checks defined in the form.
        # For example, if a required field is missing or
        # if an email field contains an improperly formatted email address
        if form.is_valid():
            form.save()
            return redirect('mailing:client_list')
    else:
        form = ClientForm()  # Creates blank form for the user to fill in
    return render(request, 'mailing/client_form.html', {'form': form})


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)  # better use get_object_or_404 if no such client exists
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)  # populate the form with the data of the existing clien
        if form.is_valid():
            form.save()
            return redirect('mailing:client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'mailing/client_form.html', {'form': form})  # dictionary,
    # containing the form that is passed to the template


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('mailing:client_list')
    return render(request, 'mailing/client_confirm_delete.html', {'client': client})


# CRUD FOR MESSAGE

@login_required
def message_list(request):
    messages = Message.objects.all()
    return render(request, 'mailing/message_list.html', {'messages': messages})


@login_required
def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mailing:message_list')
    else:
        form = MessageForm()
    return render(request, 'mailing/message_form.html', {'form': form})


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
    return render(request, 'mailing/message_form.html', {'form': form})


@login_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('mailing:message_list')
    return render(request, 'mailing/message_confirm_delete.html', {'message': message})


# CRUD FOR MAILING

@login_required
def mailing_list(request):
    mailings = Mailing.objects.all()
    return render(request, 'mailing/mailing_list.html', {'mailings': mailings})


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
    return render(request, 'mailing/mailing_form.html', {'form': form})


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
    return render(request, 'mailing/mailing_form.html', {'form': form})


@login_required
def mailing_delete(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == 'POST':
        mailing.delete()
        return redirect('mailing:mailing_list')
    return render(request, 'mailing/mailing_confirm_delete.html', {'mailing': mailing})
