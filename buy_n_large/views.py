from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Computador, Usuario
from django.views.decorators.csrf import csrf_exempt
import json
from .chatbot import obtener_respuesta_ia #se importa la logica del chatbot


def computer_list(request):
    computers = Computador.objects.all()
    data = [{"id": c.id, "marca": c.marca, "cpu": c.cpu, "ram": c.ram, "gb": c.gb, "precio": str(c.precio), "stock": c.stock, "gpu": c.gpu} for c in computers]
    return JsonResponse(data, safe=False)

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            pregunta = data.get("mensaje")
            
            if not pregunta:
                return JsonResponse({"error": "Falta el mensaje en la solicitud"}, status=400)

                # Llamamos a la función que obtiene la respuesta de la IA
            respuesta = obtener_respuesta_ia(pregunta)
            
            return JsonResponse({"respuesta":respuesta})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON Invalido"}, status=400)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def user_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            email = data.get('email')
            password = data.get('password')

            if not all([nombre, email, password]):
                return JsonResponse({'error': 'Campos requeridos faltantes'}, status=400)

            usuario = Usuario.objects.create(nombre=nombre, email=email, password=password)
            return JsonResponse({'id': usuario.id, 'nombre': usuario.nombre, 'email': usuario.email}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)

def user_detail(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    data = {"id": usuario.id, "nombre": usuario.nombre, "email": usuario.email, "is_admin": usuario.is_admin}
    return JsonResponse(data)

@csrf_exempt
def computer_create(request):
    if request.method =='POST':
        try:
            data=json.loads(request.body)
            marca=data.get('marca')
            cpu=data.get('cpu')
            ram=data.get('ram')
            gb =data.get('gb')
            precio= data.get('precio')
            stock= data.get('stock')
            gpu= data.get('gpu')

            if not all([marca, cpu, ram, gb, precio, stock]):
                return JsonResponse({'error': 'Campos requeridos faltantes'}, status=400)
            computador = Computador.objects.create(marca=marca,cpu=cpu, ram=ram, gb=gb, precio=precio,stock=stock,gpu=gpu)

            return JsonResponse({'id': computador.id, 'marca': computador.marca, 'cpu': computador.cpu, 'ram': computador.ram, 'gb': computador.gb, 'precio':computador.precio, 
                                'stock':computador.stock, 'gpu': computador.gpu }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
    


def computer_detail(request, computer_id):
    computador=get_object_or_404(Computador,pk=computer_id)
    data={'id': computador.id, 'marca': computador.marca, 'cpu': computador.cpu, 'ram': computador.ram, 'gb': computador.gb, 'precio':computador.precio, 
                                'stock':computador.stock, 'gpu': computador.gpu}
    return JsonResponse(data)


@csrf_exempt
def computer_update(request, computer_id):

    if request.method == "PUT":
        try:
            computador = get_object_or_404(Computador, pk=computer_id)
            data = json.loads(request.body)

            # Actualizar solo los campos proporcionados en la solicitud
            computador.marca = data.get('marca', computador.marca)
            computador.cpu = data.get('cpu', computador.cpu)
            computador.ram = data.get('ram', computador.ram)
            computador.gb = data.get('gb', computador.gb)
            computador.precio = data.get('precio', computador.precio)
            computador.stock = data.get('stock', computador.stock)
            computador.gpu = data.get('gpu', computador.gpu)

            computador.save()

            return JsonResponse({
                'id': computador.id, 'marca': computador.marca, 'cpu': computador.cpu, 'ram': computador.ram,
                'gb': computador.gb, 'precio': computador.precio, 'stock': computador.stock, 'gpu': computador.gpu
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)


