import re
from collections import Counter
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import TextAnalysis


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



@csrf_exempt
def analyze_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text")

            # validation
            if not text:
                return JsonResponse({"error": "Text is required"}, status=400)

            # 🔥 CALL BUSINESS LOGIC
            result = analyze_text_logic(text)

            # save to database
            analysis = TextAnalysis.objects.create(
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
            return JsonResponse({"error": str(e)}, status=500)    

def get_history(request):
    analyses = TextAnalysis.objects.all().values(
        "id", "text", "word_count", "character_count", "sentence_count", "created_at"
    )

    analyses_list = list(analyses)

    if not analyses_list:
        return JsonResponse({"message": "No history found"}, status=404)

    return JsonResponse(analyses_list, safe=False)

def get_single_analysis(request, id):
    try:
        analysis = TextAnalysis.objects.get(id=id)

        data = {
            "id": analysis.id,
            "text": analysis.text,
            "word_count": analysis.word_count,
            "character_count": analysis.character_count,
            "sentence_count": analysis.sentence_count,
            "created_at": analysis.created_at
        }

        return JsonResponse(data)

    except TextAnalysis.DoesNotExist:
        return JsonResponse({"error": "Analysis not found"}, status=404)                