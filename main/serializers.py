from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Department, Nominee, Unit, Voter

class DepartmentSerilaizer(ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'nickname']


class UnitSerilaizer(ModelSerializer):
    class Meta:
        model = Unit
        fields = ['name', 'nickname', 'department', 'state', 'voting_limit']

class UpdateUnitStateSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = ['state']


class NomineeSerilaizer(ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Nominee
        fields = ['id', 'name', 'unit', 'votes_count']

class NomineeVoteSerializer(ModelSerializer):
    class Meta:
        model = Nominee
        fields = ['name']

class VoteForNomineeSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Nominee
        fields = ['id']

class VoterSerilaizer(ModelSerializer):
    votes = NomineeVoteSerializer(many=True)

    class Meta:
        model = Voter
        fields = ['id', 'qr_id', 'voted_at', 'unit', 'votes']

class CreateVoterSerializer(ModelSerializer):
    votes = VoteForNomineeSerializer(many=True)

    class Meta:
        model = Voter
        fields = '__all__'

    def validate_unit(self, unit):
        state = unit.state

        if state == 'F':
            raise serializers.ValidationError(
                f'The voting operation for this unit has finished'
                )
        
        if state == 'S':
            raise serializers.ValidationError(
                f'The voting operation for this unit is temperory suspended'
                )
        
        return unit

    def validate(self, data):
        unit_nickname = data['unit'].nickname
        nominees_ids = [vote.get('id') for vote in data['votes']]

        unit = Unit.objects.get(pk=unit_nickname)
        voting_limit = unit.voting_limit
        
        if len(nominees_ids) != voting_limit:
            raise serializers.ValidationError(
                f'You must vote for {voting_limit} nominees exactly'
                )

        for nominee_id in nominees_ids:
            if not Nominee.objects \
                .filter(unit=unit_nickname) \
                .filter(id=nominee_id).exists():
                raise serializers.ValidationError(
                    'You cannot vote for nominees from another unit'
                    )
        return data

    def create(self, validated_data):
        votes = validated_data.pop('votes', [])
        nominees_ids = [vote.get('id') for vote in votes]
        voter = Voter.objects.create(**validated_data)
        voter.votes.set(nominees_ids)
        return voter

    
