from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import (
    resumen_nulos, columnas_mayor_nulos, candidatas_fecha, resumen_numericas,
    acumulado_columna, tipo_dato_pastel, total_datos_no_nulos
)
import pandas as pd
import json
import os

# Variable global para almacenar el DataFrame actual
current_df = None

def dashboard(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def upload_csv(request):
    global current_df
    
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        try:
            # Leer el CSV (igual que en tu Colab)
            current_df = pd.read_csv(csv_file)
            
            # Información básica
            info_basica = {
                'filas': len(current_df),
                'columnas': len(current_df.columns),
                'nombre_archivo': csv_file.name
            }
            
            return JsonResponse({
                'success': True, 
                'message': 'CSV cargado correctamente',
                'info': info_basica
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'No se recibió archivo'})

def api_nulos(request):
    """API que devuelve el análisis de valores nulos (tu código de Colab)"""
    global current_df
    
    if current_df is None:
        return JsonResponse({'error': 'No hay datos cargados'})
    
    try:
        # Tu código exacto de Colab:
        resumen = resumen_nulos(current_df)
        cols_problematicas = columnas_mayor_nulos(resumen)

        # Convertir a formato para gráficos web
        data = {
            'labels': resumen.index.tolist(),
            'valores_nulos': resumen['nulos'].tolist(),
            'porcentaje_nulos': resumen['pct_nulos'].tolist(),
            'columnas_problematicas': cols_problematicas
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)})

def api_numericas(request):
    global current_df
    if current_df is None:
        return JsonResponse({'error': 'No hay datos cargados'})
    try:
        resumen = resumen_numericas(current_df)
        data = resumen.reset_index().to_dict(orient='records')
        return JsonResponse({'resumen_numericas': data})
    except Exception as e:
        return JsonResponse({'error': str(e)})

def api_fechas(request):
    global current_df
    if current_df is None:
        return JsonResponse({'error': 'No hay datos cargados'})
    try:
        fechas = candidatas_fecha(current_df)
        return JsonResponse({'candidatas_fecha': fechas})
    except Exception as e:
        return JsonResponse({'error': str(e)})

def api_acumulado(request):
    global current_df
    if current_df is None:
        return JsonResponse({'error': 'No hay datos cargados'})
    try:
        acumulado = acumulado_columna(current_df)
        return JsonResponse({'acumulado': acumulado})
    except Exception as e:
        return JsonResponse({'error': str(e)})

def api_tipo_dato(request):
    global current_df
    if current_df is None:
        return JsonResponse({'error': 'No hay datos cargados'})
    try:
        tipo_dato = tipo_dato_pastel(current_df)
        return JsonResponse(tipo_dato)
    except Exception as e:
        return JsonResponse({'error': str(e)})

def api_no_nulos(request):
    global current_df
    if current_df is None:
        return JsonResponse({'error': 'No hay datos cargados'})
    try:
        data = total_datos_no_nulos(current_df)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)})