from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import pickle
import os
from nltk.stem import PorterStemmer
import logging

from .forms import MessageForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import Message, Profile

logger = logging.getLogger(__name__)

models_path = os.path.join(os.getcwd(), 'chat/models')
tv = pickle.load(open(os.path.join(models_path, 'CountVectorizer.pkl'), 'rb'))
model = pickle.load(open(os.path.join(models_path, 'spam_classifier.pkl'), 'rb'))

@login_required
def profile(request):
    senders = User.objects.exclude(id=request.user.id)
    selected_sender = None
    messages_list = []
    chat_users = set()

    # Get users who have chatted with the current user
    sent_messages = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_messages = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    chat_users.update(sent_messages, received_messages)
    chat_users = User.objects.filter(id__in=chat_users)

    # Get other users not in the chat list
    other_users = User.objects.exclude(id__in=chat_users).exclude(id=request.user.id)

    if 'sender_id' in request.GET:
        selected_sender = get_object_or_404(User, id=request.GET['sender_id'])
        messages_list = Message.objects.filter(
            (Q(sender=selected_sender) & Q(receiver=request.user)) |
            (Q(sender=request.user) & Q(receiver=selected_sender))
        ).order_by('created_at')

        # Mark messages as read when displayed to the receiver
        for message in messages_list:
            if message.receiver == request.user and not message.is_read:
                message.is_read = True
                message.save()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if selected_sender:
                message.receiver = selected_sender
            message.sender = request.user
            message.save()

            # Spam detection logic
            content = form.cleaned_data['content']
            stemmed_message = ' '.join([PorterStemmer().stem(word) for word in content.split()])
            transformed_message = tv.transform([stemmed_message]).toarray()
            transformed_message = transformed_message[0].reshape((1, -1))
            is_spam = model.predict(transformed_message)
            if is_spam:
                message.is_spam = True
                message.save()

                # Count total spam messages from this sender to this receiver
                total_spam_count = Message.objects.filter(
                    sender=message.sender,
                    receiver=message.receiver,
                    is_spam=True
                ).count()

                if total_spam_count > 5:
                    logger.debug(f'Spam count exceeded for {message.sender.username}. Sending alerts.')

                    try:
                        send_mail(
                            'Spam Alert',
                            f'You have received multiple spam messages from {message.sender.username}.',
                            'djangopro53@gmail.com',
                            [message.receiver.email],
                            fail_silently=False,
                        )
                        logger.debug(f'Spam alert sent to {message.receiver.email}')
                    except Exception as e:
                        logger.error(f'Failed to send spam alert to {message.receiver.email}: {e}')

                    try:
                        send_mail(
                            'Spam Warning',
                            'You have sent multiple spam messages. Please refrain from sending such messages.',
                            'djangopro53@gmail.com',
                            [message.sender.email],
                            fail_silently=False,
                        )
                        logger.debug(f'Spam warning sent to {message.sender.email}')
                    except Exception as e:
                        logger.error(f'Failed to send spam warning to {message.sender.email}: {e}')

            messages.success(request, "Message sent successfully!")
            return redirect(f'{request.path}?sender_id={selected_sender.id}')
    else:
        form = MessageForm()

    context = {
        'chat_users': chat_users,
        'other_users': other_users,
        'selected_sender': selected_sender,
        'messages_list': messages_list,
        'form': form,
    }
    return render(request, 'profile.html', context)

@login_required
@require_POST
def mark_message_read(request):
    message_id = request.POST.get('message_id')
    if message_id:
        message = get_object_or_404(Message, pk=message_id)
        if message.receiver == request.user:
            message.is_read = True
            message.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def index(request):
    if request.user.is_authenticated:
        return redirect('chat:profile')
    else:
        return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat:index')
        else:
            # Collect error messages
            errors = form.errors.as_json()
    else:
        form = CustomUserCreationForm()
        errors = None
    return render(request, 'signup.html', {'form': form, 'errors': errors})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat:index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('chat:login')


def user_detail(request, sender_id):
    sender = get_object_or_404(User, pk=sender_id)
    return render(request, 'user_profile_details.html', {'sender': sender})
