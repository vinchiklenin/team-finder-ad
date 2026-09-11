from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden,  HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

def meeting(request):
    return HttpResponse('Привет, это главная страница')