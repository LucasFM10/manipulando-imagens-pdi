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

        # Processar cada pixel da imagem
        pixels = image.load()  # Carregar todos os pixels da imagem
        width, height = image.size
        for x in range(width):
            for y in range(height):
                r, g, b, alpha = pixels[x, y]
                pixels[x, y] = (255 - r, 255 - g, 255 - b)  # Inverter cada canal

        buffered = BytesIO()
        image.save(buffered, format=ext.upper())
        new_image_src = f"data:image/{ext};base64," + base64.b64encode(buffered.getvalue()).decode()

        return JsonResponse({'new_image_src': new_image_src})
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)


@csrf_exempt
def apply_average(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        image = Image.open(BytesIO(base64.b64decode(imgstr)))
        pixels = image.load()
        width, height = image.size
        print("(((((((((())))))))))")
        # Criando uma nova imagem com bordas replicadas
        padded_image = Image.new('RGBA', (width + 2, height + 2))  # adiciona uma borda de 1 pixel em todos os lados
        padded_pixels = padded_image.load()

        # Preencher a nova imagem com pixels da imagem original
        for x in range(width):
            for y in range(height):
                padded_pixels[x + 1, y + 1] = pixels[x, y]

        # Preencher as bordas com repetição
        # Bordas verticais
        for y in range(height):
            padded_pixels[0, y + 1] = pixels[0, y]  # Coluna esquerda
            padded_pixels[width + 1, y + 1] = pixels[width - 1, y]  # Coluna direita

        # Bordas horizontais
        for x in range(width + 2):  # inclui os cantos
            padded_pixels[x, 0] = padded_pixels[x, 1]  # Linha superior
            padded_pixels[x, height + 1] = padded_pixels[x, height]  # Linha inferior
        print("000")
        # Preencher os cantos
        padded_pixels[0, 0] = padded_pixels[1, 1]  # Canto superior esquerdo
        padded_pixels[width + 1, 0] = padded_pixels[width, 1]  # Canto superior direito
        padded_pixels[0, height + 1] = padded_pixels[1, height]  # Canto inferior esquerdo
        padded_pixels[width + 1, height + 1] = padded_pixels[width, height]  # Canto inferior direito
        print("aaaa")
        # Cria uma imagem nova para o resultado
        result_image = Image.new('RGBA', (width, height))
        result_pixels = result_image.load()

        # Aplicar o filtro de média
        for x in range(1, width-1):  # Evita as bordas
            print("zzzz\n")
            for y in range(1, height-1):  # Evita as bordas
                total_r, total_g, total_b = 0, 0, 0
                for dx in range(-1, 2):  # Loop sobre a janela 3x3
                    for dy in range(-1, 2):
                        r, g, b, alpha = pixels[x + dx, y + dy]
                        total_r += r
                        total_g += g
                        total_b += b
                # Calcula a média
                avg_r = total_r // 9
                avg_g = total_g // 9
                avg_b = total_b // 9
                result_pixels[x-1, y-1] = (avg_r, avg_g, avg_b)  # Salva o pixel médio na nova imagem
        print("rrrr")
        buffered = BytesIO()
        result_image.save(buffered, format=ext.upper())
        new_image_src = f"data:image/{ext};base64," + base64.b64encode(buffered.getvalue()).decode()

        return JsonResponse({'new_image_src': new_image_src})

    return JsonResponse({'error': 'Método não permitido'}, status=405)