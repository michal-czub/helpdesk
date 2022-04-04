from rest_framework import serializers
from team.models import Team

class MemberField(serializers.Field):
	def to_representation(self, members):
		return ({
			"id": member.id,
			"name": member.name,
			} for member in members.all())

	def to_internal_value(self, data):
		return data

class TeamSerializer(serializers.ModelSerializer):
	members = MemberField()

	def create(self, validated_data):
		members = validated_data.pop("members")
		team = Team.objects.create(**validated_data)
		team.members.set(members)
		return team

	class Meta:
		model = Team
		fields = (
			"id",
			"url",
			"name",
			"members",
		)
