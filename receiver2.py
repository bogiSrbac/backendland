try:
    import pika
    import ast
    import json
    import django
    from django.core.exceptions import ObjectDoesNotExist

except Exception as e:
    print('Some moduls are missing {}'.format(e))


import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backendland.settings")
django.setup()

from hocus.models import *
from hocus.sender import sender
from django.db.models import Count


class Reciever():
    def __init__(self):
        self.credentials = pika.PlainCredentials(username='bogi', password='bogi')
        self.params = pika.ConnectionParameters(host='rabbitmq', heartbeat=600, blocked_connection_timeout=300, credentials=self.credentials)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='attack')

    def callback(ch, method, properties, body):
        pocus_tower = Tower.objects.filter(tower='Pocus').first()
        hocus_tower = Tower.objects.filter(tower='Hocus').first()

        if pocus_tower and hocus_tower:

            pocus_health = pocus_tower.health
            hocus_health = hocus_tower.health
            jsonBody = {}
            msg = {}
            try:
                responseJson = body.decode('utf-8')
                msg = json.loads(responseJson)
                print(msg)
            except:
                print('bad json: ', responseJson)
            # queryset to update Restlin if Hocus attack Pocus
            if 'HocusAttackToPocus' in msg:
                if msg['HocusAttackToPocus'] == 'attack':
                    if pocus_tower.defense <= 0:
                        pocusH = pocus_health - 100
                        pocus_tower.health = pocusH
                        pocus_tower.save(update_fields=['health'])
                    else:
                        pocusD = pocus_tower.defense
                        pocusDUpdate = pocusD - 100
                        pocus_tower.defense = pocusDUpdate
                        pocus_tower.defense = pocus_tower.defense - 100
                        pocus_tower.save(update_fields=['defense'])
                    hocusAttack = hocus_health + 100
                    hocus_tower.health = hocusAttack
                    # hocus_tower.defense
                    hocus_tower.save(update_fields=['health'])
                    data = json.loads(msg['name'])
                    hocusPlayerHealth = Defender.objects.get(nickname=data['name'], tower_id=hocus_tower.pk)
                    hocusPlayerHealth.attacked_points_generated = hocusPlayerHealth.attacked_points_generated + 100
                    hocusPlayerHealth.save(update_fields=['attacked_points_generated'])
                    currentAttackPoints = hocusPlayerHealth.attacked_points_generated
                    jsonBody = {'name': data['name'], 'towerHealth': hocusAttack,
                                'attackPoints': currentAttackPoints}
                    sender(jsonBody)

                # queryset to update Restlin if new defender entered Hocus
                elif len(msg["hocusPlayer"]) > 2 and msg['connect'] == 'yes':
                    hocusH = hocus_health + 1000
                    hocus_tower.health = hocusH
                    hocus_tower.save(update_fields=['health'])
                    pocusH = pocus_health + 1000
                    pocus_tower.health = pocusH
                    pocus_tower.save(update_fields=['health'])

                # queryset to update Restlin if defender disconnected Hocus
                elif len(msg["hocusPlayer"]) > 2 and msg["disconnect"] and hocus_health >= 500:
                    hocusH = hocus_health - 500
                    hocus_tower.health = hocusH
                    hocus_tower.save(update_fields=['health'])
                    print(msg["hocusPlayer"])
                    try:
                        defender = Defender.objects.all()
                        for item in defender:
                            print(item.defendeSocketId)

                    except ObjectDoesNotExist:
                        raise ValueError('Requested query is empty.')


                # queryset to update Restlin if Hocus use shield
                elif msg["shield"] == "shield":
                    hocusDefense = hocus_tower.defense + 150
                    hocus_tower.defense = hocusDefense
                    hocus_tower.save(update_fields=['defense'])
                    data = json.loads(msg['name'])
                    # defense points for player
                    hocusPlayerHealth = Defender.objects.get(nickname=data['name'], tower_id=hocus_tower.pk)
                    hocusPlayerHealth.defense_points_generated = hocusPlayerHealth.defense_points_generated + 150
                    hocusPlayerHealth.save(update_fields=['defense_points_generated'])
                    currentDefendPoints = hocusPlayerHealth.defense_points_generated
                    jsonBody = {'name': data['name'], 'shieldPoints': currentDefendPoints, 'hocus':'hocus'}
                    print(jsonBody, 'this')
                    sender(jsonBody)



            if 'HocusAttackToPocus' in msg:
                if len(msg["hocusPlayer"]) > 2 and len(msg["HocusAttackToPocus"]) > 2:
                    defender = Defender.objects.get(nickname=msg["HocusAttackToPocus"])
                    defender.defendeSocketId = msg["hocusPlayer"]
                    defender.save(update_fields=['defendeSocketId'])

            if 'PocusAttackToHocus' in msg:
                if len(msg["pocusPlayer"]) > 2 and len(msg["PocusAttackToHocus"]) > 2:
                    defender = Defender.objects.get(nickname=msg["PocusAttackToHocus"])
                    defender.defendeSocketId = msg["pocusPlayer"]
                    defender.save(update_fields=['defendeSocketId'])

            # queryset to update Restlin if Pocus attack Hocus
            if 'PocusAttackToHocus' in msg:
                if msg['PocusAttackToHocus'] == "attack":
                    if hocus_tower.defense <= 0:
                        hocusH = hocus_health - 100
                        hocus_tower.health = hocusH
                        hocus_tower.save(update_fields=['health'])
                    else:
                        hocusD = hocus_tower.defense
                        hocusDUpdate = hocusD - 100
                        hocus_tower.defense = hocusDUpdate
                        hocus_tower.save(update_fields=['defense'])
                    pocusAttack = pocus_health + 100
                    pocus_tower.health = pocusAttack
                    # hocus_tower.defense
                    pocus_tower.save(update_fields=['health'])
                    data = json.loads(msg['name'])
                    pocusPlayerHealth = Defender.objects.get(nickname=data['name'], tower_id=pocus_tower.pk)
                    pocusPlayerHealth.attacked_points_generated = pocusPlayerHealth.attacked_points_generated + 100
                    pocusPlayerHealth.save(update_fields=['attacked_points_generated'])
                    currentAttackPoints = pocusPlayerHealth.attacked_points_generated
                    jsonBody = {'name': data['name'], 'towerHealth': pocusAttack,
                                'attackPoints': currentAttackPoints, 'pocus':'pocus'}
                    sender(jsonBody)
                    # queryset to update Restlin if Pocus use shield

                elif msg["shield"] == "shield":
                    pocusDefense = pocus_tower.defense + 150
                    pocus_tower.defense = pocusDefense
                    pocus_tower.save(update_fields=['defense'])
                    data = json.loads(msg['name'])
                    # defense points for player
                    pocusPlayerHealth = Defender.objects.get(nickname=data['name'], tower_id=pocus_tower.pk)
                    pocusPlayerHealth.defense_points_generated = pocusPlayerHealth.defense_points_generated + 150
                    pocusPlayerHealth.save(update_fields=['defense_points_generated'])
                    currentDefendPoints = pocusPlayerHealth.defense_points_generated
                    jsonBody = {'name': data['name'], 'shieldPoints': currentDefendPoints, 'pocus':'pocus'}
                    # print(currentDefendPoints)
                    sender(jsonBody)

            # queryset to update Restlin if new defender entered Pocus
                elif len(msg["pocusPlayer"]) > 2 and msg['connect'] == "yes":
                    hocusH = hocus_health + 1000
                    hocus_tower.health = hocusH
                    hocus_tower.save(update_fields=['health'])
                    pocusH = pocus_health + 1000
                    pocus_tower.health = pocusH
                    pocus_tower.save(update_fields=['health'])

            # # queryset to update Restlin if defender disconnected Pocus
                elif len(msg["pocusPlayer"]) > 2 and msg["disconnect"] and pocus_health >= 500:
                    pocusH = pocus_health - 500
                    pocus_tower.health = pocusH
                    pocus_tower.save(update_fields=['health'])


            # //delete defender from database if disconnect
            if 'disconnect' in msg and 'pocusPlayer' in msg:
                if msg['disconnect'] == 'disconnect' and len(msg['pocusPlayer']) > 1:
                    if Defender.objects.filter(defendeSocketId__isnull=False):
                        try:
                            defender = Defender.objects.filter(defendeSocketId=msg['pocusPlayer']).first()
                            if defender:
                                defender.delete()
                                pocusPlayerCount = Defender.objects.filter(tower_id=pocus_tower.pk).count()
                                pocus_tower.defender_count = pocusPlayerCount - 1
                                pocus_tower.save(update_fields=['defender_count'])

                        except ObjectDoesNotExist:
                            raise ValueError('Requested query is empty.')


            # //delete defender from database if disconnect
            if 'disconnect' in msg and 'hocusPlayer' in msg:
                if msg['disconnect'] == 'disconnect' and len(msg['hocusPlayer']) > 1:
                    if Defender.objects.filter(defendeSocketId__isnull=False):
                        try:
                            defender = Defender.objects.filter(defendeSocketId=msg['hocusPlayer']).first()
                            if defender:
                                defender.delete()
                                hocusPlayerCount = Defender.objects.filter(tower_id=hocus_tower.pk).count()
                                hocus_tower.defender_count = hocusPlayerCount - 1
                                hocus_tower.save(update_fields=['defender_count'])

                        except ObjectDoesNotExist:
                            raise ValueError('Requested query is empty.')


            # update health and defense for both towers
            pocusTowerHealth = Tower.objects.get(tower='Pocus')
            hocusTowrHealth = Tower.objects.get(tower='Hocus')

            pocusPlayerCount = Defender.objects.filter(tower_id=pocusTowerHealth.pk).count()
            pocusTowerHealth.defender_count = pocusPlayerCount
            pocusTowerHealth.save(update_fields=['defender_count'])

            hocusPlayerCount = Defender.objects.filter(tower_id=hocusTowrHealth.pk).count()
            hocusTowrHealth.defender_count = hocusPlayerCount
            hocusTowrHealth.save(update_fields=['defender_count'])

            #update round global_defender_count
            roundCountGlobalDefenders = Round.objects.filter(time_created__isnull=False).order_by('-pk')[0]
            roundCountGlobalDefenders.global_defender_count = pocusPlayerCount + hocusPlayerCount
            roundCountGlobalDefenders.save(update_fields=['global_defender_count'])

            if 'PocusAttackToHocus' in msg:
                if msg['PocusAttackToHocus'] == 'attack':
                    sender(msg)

            if 'HocusAttackToPocus' in msg:
                if msg['HocusAttackToPocus'] == 'attack':
                    sender(msg)



            sender({
                'hocusHealth': hocusTowrHealth.health,
                'hocusDefense': hocusTowrHealth.defense,
                'pocusHealth':pocusTowerHealth.health,
                'pocusDefense':pocusTowerHealth.defense,
                'defenderPocusCount': pocusTowerHealth.defender_count,
                'defenderHocusCount': hocusTowrHealth.defender_count,
            })
            # if some of towers ges under 0 another tower win
            if pocusTowerHealth.health <=0:
                sender({'win':'Hocus tower won this round'})

            elif hocusTowrHealth.health <=0:
                sender({'win':'Pocus tower won this round'})

            if 'PocusAttackToHocus' in msg:
                if msg['PocusAttackToHocus'] == 'pocus' and msg['endGame'] == 'endGame':
                    sender({'winEnd':'Hocus tower won this round because last Pocus defender disconnected'})


            if 'HocusAttackToPocus' in msg:
                if msg['HocusAttackToPocus'] == 'hocus' and msg['endGame'] == 'endGame':
                    sender({'winEnd':'Pocus tower won this round because last Hocus defender disconnected'})












    def startServer(self):
        self.channel.basic_consume(queue='attack', on_message_callback=Reciever.callback, auto_ack=True)
        print('startted consuming')
        self.channel.start_consuming()
        self.channel.close()

if __name__ == "__main__":
    import sys
    import os


    try:
        server = Reciever()
        server.startServer()

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


