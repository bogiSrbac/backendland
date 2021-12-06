from django.db import models


class Tower(models.Model):
    TOWERS = [
        ('Hocus', 'Hocus'),
        ('Pocus', 'Pocus')
    ]
    tower = models.CharField(max_length=150, choices=TOWERS, blank=True, null=True)
    health = models.IntegerField(default=5000)
    defense = models.IntegerField(blank=True, null=True, default=0)
    round = models.IntegerField(blank=True, null=True, default=0)
    defender_count = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.tower)

class Defender(models.Model):
    nickname = models.CharField(max_length=150, blank=True, null=True)
    defendeSocketId = models.CharField(max_length=150, blank=True, null=True)
    attacked_points_generated = models.IntegerField(blank=True, null=True, default=0)
    defense_points_generated = models.IntegerField(blank=True, null=True, default=0)
    tower = models.ForeignKey(Tower, on_delete=models.CASCADE, related_name='tower_defender')

    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ['nickname']

from datetime import datetime

class Round(models.Model):
    time_created = models.DateTimeField(default=datetime.now, blank=True)
    # preispitati
    global_defender_count = models.IntegerField(blank=True, null=True)
    hocus_tower = models.ForeignKey(Tower, on_delete=models.CASCADE, blank=True, null=True, related_name='hocus_tower')
    pocus_tower = models.ForeignKey(Tower, on_delete=models.CASCADE, blank=True, null=True, related_name='pocus_tower')

    def __str__(self):
        return self.time_created.strftime('%d-%m-%Y (%H:%M)')

    def save(self, *args, **kwargs):
        tower = Tower.objects.filter(tower='Hocus')[0]
        towerPocus = Tower.objects.filter(tower='Pocus')[0]
        self.hocus_tower = tower
        self.pocus_tower = towerPocus
        super(Round, self).save(*args, **kwargs)







































