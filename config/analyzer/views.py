import re
from collections import Counter
from django.http import JsonResponse
from .models import TextAnalysis
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import AnalyzeTextSerializer
from drf_yasg.utils import swagger_auto_schema


def analyze_text_logic(text):
    # count words
    words = text.split()
    word_count = len(words)

    # count characters
    character_count = len(text)

    # count sentences (simple version)
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])

    # most frequent words
    words_lower = [word.lower() for word in words]
    word_freq = Counter(words_lower)
    most_common = [word for word, count in word_freq.most_common(3)]

    return {
        "word_count": word_count,
        "character_count": character_count,
        "sentence_count": sentence_count,
        "most_frequent_words": most_common
    }


@swagger_auto_schema(
    method='post',
    request_body=AnalyzeTextSerializer,
    operation_description="Analyze input text and return word, character, and sentence counts."
)
@api_view(['POST'])
def analyze_text(request):
    try:
        serializer = AnalyzeTextSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        text = serializer.validated_data["text"]

        if text.strip() == "":
            return JsonResponse({"error": "Text cannot be empty"}, status=400)

        # business logic
        result = analyze_text_logic(text)

        # save
        analysis = TextAnalysis.objects.create(
            user=request.user if request.user.is_authenticated else None,
            text=text,
            word_count=result["word_count"],
            character_count=result["character_count"],
            sentence_count=result["sentence_count"]
        )

        return JsonResponse({
            "id": analysis.id,
            "text": text,
            **result
        }, status=201)

    except Exception as e:
        return JsonResponse({
            "error": "Internal server error",
            "details": str(e)
        }, status=500)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_history(request):
    analyses = TextAnalysis.objects.filter(user=request.user).values(
        "id", "text", "word_count", "character_count", "sentence_count", "created_at"
    )

    analyses_list = list(analyses)

    if not analyses_list:
        return JsonResponse({
            "message": "No history found",
            "data": []
        }, status=200)

    return JsonResponse({
        "count": len(analyses_list),
        "data": analyses_list
    }, status=200)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_single_analysis(request, id):
    try:
        analysis = TextAnalysis.objects.get(id=id, user=request.user)

        return JsonResponse({
            "data": {
                "id": analysis.id,
                "text": analysis.text,
                "word_count": analysis.word_count,
                "character_count": analysis.character_count,
                "sentence_count": analysis.sentence_count,
                "created_at": analysis.created_at
            }
        }, status=200)

    except TextAnalysis.DoesNotExist:
        return JsonResponse({
            "error": "Analysis not found"
        }, status=404)
