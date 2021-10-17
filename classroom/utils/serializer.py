from rest_framework import serializers


class ValidateUniqueTogetherMixin:
    def unique_together_validate(self, queryset, err_message):
        request = self.context['request']
        error = False

        if request.method in ('PUT', 'PATCH'):
            pk = request.parser_context['kwargs']['pk']
            instance = queryset.first()
            if instance:
                error = str(instance.pk) != str(pk)
        else:
            error = queryset.exists()

        if error:
            raise serializers.ValidationError(
                detail=err_message,
                code='unique_together'
            )
