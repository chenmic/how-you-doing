import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Message


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def write(request):
    info = request.query_params
    if info and all(param in info.keys() for param in ['to', 'subject', 'message']):
        msg = Message(sender=request.user,
                      receiver=info['to'],
                      subject=info['subject'],
                      message=info['message'],
                      creation_date=datetime.now())
        msg.save()
        return JsonResponse({"data": "Message sent."})
    else:
        return HttpResponseBadRequest('Write must include `to`, `subject`, and `message`.')


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user).order_by('-creation_date')
    messages = list(received_messages.values())
    return HttpResponse(json.dumps(messages, cls=DjangoJSONEncoder), content_type='application/json')


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def unread(request):
    unread_messages = Message.objects.filter(receiver=request.user, is_read=False).order_by('-creation_date')
    messages = list(unread_messages.values())
    return HttpResponse(json.dumps(messages, cls=DjangoJSONEncoder), content_type='application/json')


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def sent(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-creation_date')
    messages = list(sent_messages.values())
    return HttpResponse(json.dumps(messages, cls=DjangoJSONEncoder), content_type='application/json')


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def read(request):
    unread_messages = Message.objects.filter(receiver=request.user, is_read=False).order_by('creation_date')
    oldest_unread_message = unread_messages.values()[0]
    message = Message.objects.get(pk=oldest_unread_message['id'])
    message.is_read = True
    message.save()
    return HttpResponse(json.dumps(oldest_unread_message, cls=DjangoJSONEncoder), content_type='application/json')


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete(request):
    info = request.query_params
    if info and 'id' in info:
        message = get_object_or_404(Message, pk=info['id'])
        if request.user == message.sender or request.user == message.receiver:
            message.delete()
            return JsonResponse({"data": f"Message {info['id']} deleted."})
        else:
            return HttpResponseForbidden('Only sender or receiver allowed to delete their message.')
    else:
        return HttpResponseBadRequest('Delete must include `id`.')

