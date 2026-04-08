from rest_framework import serializers

class AnalyzeTextSerializer(serializers.Serializer):
    text = serializers.CharField(
        help_text="Enter the text you want to analyze",
        max_length=10000
    )