from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models
from django.contrib import messages
from . import models
import datetime
from django.urls import reverse_lazy
from django.contrib.auth import logout

def index(request):

    lastquestion = models.question.objects.all().count()

    user = request.user
    if user.is_authenticated:
        try:
            player = models.player.objects.get(user_id=request.user.pk)
        except:
            logout(request)
            return render(request, 'index_page.html')
        if datetime.datetime.now()<datetime.datetime(2021,12,30,21,00,00,701322):
            return render(request, 'wait.html', {'player': player})
        elif datetime.datetime.now()>datetime.datetime(2022,12,9,21,15,00,701322):
            return render(request, 'finish.html', {'player': player})
        elif player.current_question > lastquestion:
            return render(request, 'win.html', {'player': player})
        try:
            question = models.question.objects.get(Q_number=player.current_question)
            return render(request, 'question.html', {'player': player, 'question': question})
        except models.question.DoesNotExist:
            return render(request, 'finish.html', {'player': player})
    return render(request, 'index_page.html')


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        profile = user
        try:
            player = models.player.objects.get(user=profile)
        except:
            player = models.player(user=profile)
            player.timestamp=datetime.datetime.now()
            try:
                player.name = response.get('name')
            except:
                player.name = response.get('given_name') + " " + response.get('family_name')
            player.save()


@login_required
def answer(request):

    lastquestion = models.question.objects.all().count()

    ans = ""
    if request.method == 'POST':
        ans = request.POST.get('option')
        print(ans)
    player = models.player.objects.get(user_id=request.user.pk)
    try:
        question = models.question.objects.get(Q_number=player.current_question)
    except models.question.DoesNotExist:
        if player.current_question > lastquestion:
            return render(request, 'win.html', {'player': player})
        return redirect(reverse_lazy('cit2020:index'))

    if ans == question.answer:
        player.current_question = player.current_question + 1
        player.score = player.score + 4
        player.timestamp = datetime.datetime.now()
        question.correct = question.correct + 1
        question.accuracy = round(question.correct/(float(question.correct + question.wrong)),2)*100
        question.save()
        player.save()

        return redirect(reverse_lazy('cit2020:index'))


    elif ans=='0' or ans==None:
        player.current_question = player.current_question + 1
        player.timestamp = datetime.datetime.now()
        player.save()

        return redirect(reverse_lazy('cit2020:index'))

    else:
        player.current_question = player.current_question + 1
        player.score = player.score - 1
        player.timestamp = datetime.datetime.now()
        question.wrong = question.wrong + 1
        question.accuracy = round(question.correct/(float(question.correct + question.wrong)),2)*100
        question.save()
        player.save()

        return redirect(reverse_lazy('cit2020:index'))

    return render(request, 'question.html', {'player': player, 'question': question})


def lboard(request):
    p = models.player.objects.order_by('-score','timestamp')
    cur_rank = 1

    for pl in p:
        pl.rank = cur_rank
        pl.save()
        cur_rank += 1

    if request.user.is_authenticated:
        try:
            player = models.player.objects.get(user_id=request.user.pk)
            rank = player.rank
            return render(request, 'lboard.html', {'players': p, 'rank':rank})
        except:
            pass
    return render(request, 'lboard.html', {'players': p})

def rules(request):
    return render(request, 'rules.html')