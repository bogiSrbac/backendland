from django.shortcuts import render, redirect
from .models import *
from receiver2 import Reciever
from .sender import CheckIfDefenderExist, sender
from .forms import CreateDefenderForm
from django.http import JsonResponse, HttpResponseRedirect
try:
    import pika
    import ast
    import json

except Exception as e:
    print('Some moduls are missing {}'.format(e))



def index(request):
    form = CreateDefenderForm(request.POST)
    context = {
        'form':form
    }
    return render(request, 'hocus/hocusIndex.html', context)

def play_game(request, pk):
    if pk=='Hocus':
        return HttpResponseRedirect('http://127.0.0.1:666/')
    elif pk=='Pocus':
        return HttpResponseRedirect('http://127.0.0.1:3000/')
    else:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def createDefenders(request):
    form = CreateDefenderForm(request.POST)
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid():
                # pokrecemo Pika server
                print('saljem')

                nickname = request.POST.get('nickname')
                tower = request.POST.get('tower')
                towerId = Tower.objects.get(pk=int(tower))
                whichTower = towerId.tower

                message = {'tower': f'{tower}', 'name': f'{nickname}'}
                # sender(message)
                sendRPC = CheckIfDefenderExist()
                response = sendRPC.call(message)
                response = response.decode('utf-8')
                response = json.loads(response)
                defenderDataBase = Defender.objects.filter(nickname__isnull=False, nickname=response['name'])
                if defenderDataBase:
                    return JsonResponse({'submit': 'Player whit this nickname already exist. Try another nick!'})
                elif response['name'] == nickname and whichTower == 'Hocus' and response['status'] == 'no':
                    defender = Defender(nickname=response['name'], tower_id=int(tower))
                    defender.save()
                    return JsonResponse({'submit': 'hocus'})
                elif response['name'] == nickname and whichTower == 'Pocus' and response['status'] == 'no':
                    defender = Defender(nickname=response['name'], tower_id=int(tower))
                    defender.save()
                    return JsonResponse({'submit': 'pocus'})
                else:
                    print('da li sam ovde')
                    return JsonResponse({'submit': 'Player whit this nickname already exist. Try another nick!'})
            else:
                return JsonResponse({'error':"form wasn't submitted successfully"})

def sendNick(request, var_X=None):
    if request.method == 'GET':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            tower = Defender.objects.get(nickname=var_X)
            towerName = tower.tower.tower
            towerHealth = tower.tower.health
            defenderAttackPoints = tower.attacked_points_generated
            defenderDefencePointsGenerated = tower.defense_points_generated
            nickName = {
                'tower':towerName,
                'nickName': var_X,
                'towerHealth':towerHealth,
                'defenderAttackPoints': defenderAttackPoints,
                'defenderDefencePointsGenerated':defenderDefencePointsGenerated,
            }
            sender(nickName)
            print(nickName)
            return JsonResponse({})

def createFirstRoundFunc():
    roundCrete = Round.objects.create()
    roundCrete.save()
    return 'success'


# creating first round and bout towers
def createFirstRound(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if Tower.objects.all().count() == 0:
                towerHocus = Tower.objects.create(tower='Hocus', health=5000)
                towerHocus.save()
                towerPocus = Tower.objects.create(tower='Pocus', health=5000)
                towerPocus.save()
                createFirstRoundFunc()
            return JsonResponse({})

def hocusWon(request):
    hocus = Tower.objects.get(tower='Hocus')
    pocus = Tower.objects.get(tower='Pocus')
    pocusCount = Defender.objects.filter(tower__tower='Pocus').count()
    hocusCount = Defender.objects.filter(tower__tower='Hocus').count()
    rounds = Round.objects.filter(time_created__isnull=False).count()
    print(pocusCount, hocusCount, 'hokus')
    if pocusCount == 0 and hocusCount == 1:
        if hocus.round + pocus.round == rounds:
            pass
        else:
            hocus.round = hocus.round + 1
            if hocus.round + pocus.round == rounds:
                newRoundCreate = Round.objects.create()
                newRoundCreate.save()
        hocus.health = 5000
        pocus.health = 5000
        hocus.defense = 0
        pocus.defense = 0
        pocus.save()
        hocus.save()
    elif pocusCount == 0 and hocusCount == 0:
        if hocus.round + pocus.round == rounds:
            pass
        else:
            hocus.round = hocus.round + 1
            if hocus.round + pocus.round == rounds:
                newRoundCreate = Round.objects.create()
                newRoundCreate.save()
        hocus.health = 5000
        pocus.health = 5000
        hocus.defense = 0
        pocus.defense = 0
        pocus.save()
        hocus.save()


    context = {
        'hocus': hocus
    }
    return render(request, 'hocus/hocus_won.html', context)

def pocusWon(request):
    pocus = Tower.objects.get(tower='Pocus')
    hocus = Tower.objects.get(tower='Hocus')
    pocusCount = Defender.objects.filter(tower__tower='Pocus').count()
    hocusCount = Defender.objects.filter(tower__tower='Hocus').count()
    rounds = Round.objects.filter(time_created__isnull=False).count()
    if pocusCount == 1 and hocusCount == 0:
        if hocus.round + pocus.round == rounds:
            pass
        else:
            pocus.round = pocus.round + 1
            if hocus.round + pocus.round == rounds:
                newRoundCreate = Round.objects.create()
                newRoundCreate.save()
        pocus.health = 5000
        hocus.health = 5000
        hocus.defense = 0
        pocus.defense = 0
        hocus.save()
        pocus.save()
    elif pocusCount == 0 and hocusCount == 0:
        if hocus.round + pocus.round == rounds:
            pass
        else:
            pocus.round = pocus.round + 1
            if hocus.round + pocus.round == rounds:
                newRoundCreate = Round.objects.create()
                newRoundCreate.save()
        pocus.health = 5000
        hocus.health = 5000
        hocus.defense = 0
        pocus.defense = 0
        hocus.save()
        pocus.save()


    context = {
            'pocus': pocus
        }
    return render(request, 'hocus/pocus_won.html', context)
