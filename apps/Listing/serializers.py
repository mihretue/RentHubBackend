from rest_framework import serializers
from .models import Listing
from django.contrib.auth import get_user_model
User = get_user_model()

class ListingSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(
        choices=Listing.Category.choices,
        error_messages={
            'invalid_choice': 'Invalid category. Valid choices are: {}.'.format(
                ', '.join([c for c, _ in Listing.Category.choices])
            )
        }
    )
    
    status = serializers.ChoiceField(
        choices=Listing.ListingStatus.choices,
        error_messages={
            'invalid_choice': 'Invalid status. Valid choices are: {}.'.format(
                ', '.join([c for c, _ in Listing.ListingStatus.choices])
            )
        }
    )
 
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')

        # Admin can assign owner explicitly
        if request.user.is_staff and 'owner' in validated_data:
            owner_id = validated_data.pop('owner')
            try:
                owner = User.objects.get(id=owner_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({"owner": "User does not exist."})
            validated_data['owner'] = owner
        # Regular authenticated user -> set as owner
        elif request.user.is_authenticated:
            validated_data['owner'] = request.user
        # Anonymous
        else:
            validated_data['owner'] = None

        return super().create(validated_data)