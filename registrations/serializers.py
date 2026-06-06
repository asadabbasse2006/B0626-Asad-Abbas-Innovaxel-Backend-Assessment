from .models import Registration
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ('registered_at',)

    def validate(self, attrs):
        event = attrs.get('event')
        username = attrs.get('username')

        if not username:
            raise serializers.ValidationError('Username is required')

        if Registration.objects.filter(event=event, username=username,status='ACTIVE').exists():
            raise serializers.ValidationError('Username is already registered')

        if event.available_seats <= 0:
            raise serializers.ValidationError('No seats available for this event')

        return attrs

    def create(self, validated_data):

        event = validated_data['event']
        event.available_seats -= 1
        event.save()

        return super().create(validated_data)
