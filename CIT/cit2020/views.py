from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models
from . import models
import datetime
from django.urls import reverse_lazy
from django.contrib.auth import logout

slot1_start=datetime.datetime(2022, 1, 15, 9, 00, 00, 701322)
slot1_end=datetime.datetime(2023, 1, 15, 12, 00, 00, 701322)


slot2_start=datetime.datetime(2022, 1, 16, 9, 00, 00, 701322)
slot2_end=datetime.datetime(2023, 1, 16, 12, 00, 00, 701322)


slot3_start=datetime.datetime(2022, 1, 17, 9, 00, 00, 701322)
slot3_end=datetime.datetime(2023, 1, 17, 12, 00, 00, 701322)


final_start=datetime.datetime(2022, 1, 20, 9, 00, 00, 701322)
final_end=datetime.datetime(2023, 1, 20, 12, 00, 00, 701322)



def index(request):

    lastquestion = models.question.objects.all().count()

    user = request.user
    if user.is_authenticated:
        try:
            player = models.player.objects.get(user_id=request.user.pk)
        except:
            logout(request)
            return render(request, 'index_page.html')
        if player.slot < 1:
            return render(request, 'forms.html')
        elif player.slot == 1 and datetime.datetime.now() < slot1_start:
            return render(request, 'wait.html', {'player': player})
        elif player.slot == 1 and datetime.datetime.now() > slot1_end:
            return render(request, 'finish.html', {'player': player})
        elif player.slot == 2 and datetime.datetime.now() < slot2_start:
            return render(request, 'wait.html', {'player': player})
        elif player.slot == 2 and datetime.datetime.now() > slot2_end:
            return render(request, 'finish.html', {'player': player})
        elif player.slot == 3 and datetime.datetime.now() < slot3_start:
            return render(request, 'wait.html', {'player': player})
        elif player.slot == 3 and datetime.datetime.now() > slot3_end:
            return render(request, 'finish.html', {'player': player})
        elif player.qualified==True and datetime.datetime.now() < final_start:
            return render(request, 'wait.html', {'player': player})
        elif player.qualified==True and datetime.datetime.now() > final_end:
            return render(request, 'finish.html', {'player': player})
        elif player.qualified==False and datetime.datetime.now() > slot3_end:
            return render(request, 'luck.html', {'player': player})
        elif player.current_question > lastquestion:
            return render(request, 'win.html', {'player': player})
        try:
            question = models.question.objects.get(
                Q_number=player.current_question)
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
            player.timestamp = datetime.datetime.now()
            try:
                player.name = response.get('name')
            except:
                player.name = response.get(
                    'given_name') + " " + response.get('family_name')
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
        question = models.question.objects.get(
            Q_number=player.current_question)
    except models.question.DoesNotExist:
        if player.current_question > lastquestion:
            return render(request, 'win.html', {'player': player})
        return redirect(reverse_lazy('cit2020:index'))

    if ans == question.answer:
        player.current_question = player.current_question + 1
        player.score = player.score + 4
        player.timestamp = datetime.datetime.now()
        question.correct = question.correct + 1
        question.accuracy = round(
            question.correct/(float(question.correct + question.wrong)), 2)*100
        question.save()
        player.save()
      
        return redirect(reverse_lazy('cit2020:index'))

    elif ans == '0' or ans == None:
        player.current_question = player.current_question + 1
        player.timestamp = datetime.datetime.now()
        player.save()

        return redirect(reverse_lazy('cit2020:index'))

    else:
        player.current_question = player.current_question + 1
        player.score = player.score - 1
        player.timestamp = datetime.datetime.now()
        question.wrong = question.wrong + 1
        question.accuracy = round(
            question.correct/(float(question.correct + question.wrong)), 2)*100
        question.save()
        player.save()

    return redirect(reverse_lazy('cit2020:index'))


def lboard(request,slot=0):
    if slot==1 :
        if datetime.datetime.now() < slot1_start:
            return render(request, 'lboard.html',{})
        else :
            p = models.player.objects.filter(slot=1).order_by('-score', 'timestamp')
    elif slot==2:
        if datetime.datetime.now() < slot2_start:
            return render(request, 'lboard.html',{})
        else :
            p = models.player.objects.filter(slot=2).order_by('-score', 'timestamp')
    elif slot==3:
        if datetime.datetime.now() < slot3_start:
            return render(request, 'lboard.html',{})
        else :
            p = models.player.objects.filter(slot=3).order_by('-score', 'timestamp')
    elif slot==0 :
        if datetime.datetime.now() < final_start:
            return render(request, 'lboard.html',{})
        else :
            p = models.player.objects.filter(qualified=True).order_by('-score', 'timestamp')
    else :
         return redirect('cit2020:lboard',slot=1)

    cur_rank = 1
    show=False
    if request.user.is_authenticated and (models.player.slot==slot or models.player.qualified==True) :
        show=True
    rank=0
    for pl in p:
        pl.rank = cur_rank
        # pl.save()
        cur_rank += 1
        if show==True :
            rank=pl.rank
    return render(request, 'lboard.html', {'players': p, 'rank': rank})

def rules(request):
    return render(request, 'rules.html')


@login_required
def forms(request):
    slot = ""
    if request.method == 'POST':
        slot = request.POST.get('slot')
        player = models.player.objects.get(user_id=request.user.pk)
        if slot == '1':
            player.slot = player.slot + 1
           
        elif slot == '2':
            player.slot = player.slot + 2
          
        elif slot == '3':
            player.slot = player.slot + 3

        player.save()

    return redirect(reverse_lazy('cit2020:index'))


def qualify(request):
    if request.user.is_superuser:
        q=models.player.objects.filter(score__gte=120)
        for pl in q :
            pl.qualified=True
            pl.slot=4
            pl.save()

        return redirect(reverse_lazy('cit2020:index'))
    else:
        return redirect(reverse_lazy('cit2020:index'))
