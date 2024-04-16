# main/views.py
from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image, ImageOps
import base64
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def apply_negative(request):
    
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        format, imgstr = image_data.split(';base64,')  # Assume que a imagem é enviada como base64
        ext = format.split('/')[-1]

        image = Image.open(BytesIO(base64.b64decode(imgstr)))
        image = image.convert('L')  # Convert to grayscale for simplicity
        image = ImageOps.invert(image)  # Apply negative filter

        buffered = BytesIO()
        image.save(buffered, format=ext.upper())
        new_image_src = f"data:image/{ext};base64," + base64.b64encode(buffered.getvalue()).decode()

        return JsonResponse({'new_image_src': new_image_src})
    return JsonResponse({'error': 'Método não permitido'}, status=405)