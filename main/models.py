from django.db import models

class Department(models.Model):
    nickname = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Unit(models.Model):
    STATE_ACTIVE = 'A'
    STATE_SUSPENDED = 'S'
    STATE_FINISHED = 'F'

    STATE_CHOICES = [
        (STATE_ACTIVE, 'Active'),
        (STATE_SUSPENDED, 'Suspended'),
        (STATE_FINISHED, 'Finished'),
    ]

    nickname = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='units')
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default=STATE_SUSPENDED)
    voting_limit = models.PositiveSmallIntegerField(default=24)

    def __str__(self) -> str:
        return self.name 

class Nominee(models.Model):
    name = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='nominees')

    def __str__(self) -> str:
        return self.name

class Voter(models.Model):
    qr_id = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='voters')
    voted_at = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(Nominee, related_name='votes')

    def __str__(self) -> str:
        return f'{self.unit.nickname}_{self.qr_id}'
