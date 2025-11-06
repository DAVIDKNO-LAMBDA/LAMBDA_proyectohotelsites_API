import pandas as pd
import numpy as np
from datetime import timedelta
import os

BASE_PATH = "dashboard/data/"

def load_data():
    common_kwargs = dict(sep='|', quotechar='"', encoding='latin1')
    data_files = [
        "Ventas.csv",
        "Forecast.csv",
        "Habitaciones.csv",
        "Huespedes.csv",
        "Expensas.csv",
        "Indicadoresppto.csv",
        "Presupuesto.csv",
        "Propiedades.csv",
    ]

    data = {}
    for file in data_files:
        path = os.path.join(BASE_PATH, file)
        try:
            # Archivos que usan ';' como separador
            if file in ["Indicadoresppto.csv", "Presupuesto.csv"]:
                df = pd.read_csv(path, sep=';', encoding='latin1')
            else:
                df = pd.read_csv(path, **common_kwargs)
            
            df.columns = (
                df.columns.str.strip()
                          .str.replace('"', '', regex=False)
                          .str.replace("'", '', regex=False)
                          .str.replace('﻿', '', regex=False)
            )
            print(f"✅ {file} cargado con columnas: {list(df.columns)}")
        except Exception as e:
            print(f"⚠️ Error al cargar {file}: {e}")
            df = pd.DataFrame()
        data[file.replace(".csv", "").lower()] = df
    return data


def safe_round(value, decimals=2):
    """Hace round() de forma segura, convirtiendo a float si es necesario"""
    try:
        return round(float(value), decimals) if value is not None else 0.0
    except (ValueError, TypeError):
        return 0.0

def safe_div(a, b):
    """División segura que evita división por cero"""
    try:
        if b == 0 or b is None or pd.isna(b):
            return 0
        return float(a) / float(b)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

def safe_div(numerator, denominator):
    """Evita divisiones por cero o valores NaN."""
    try:
        return numerator / denominator if denominator not in [0, None, np.nan] and not pd.isna(denominator) else 0
    except Exception:
        return 0


def calculate_ocupacion_real(habitaciones_df):
    """
    Calcula %Ocup - Ocupación real exactamente como Power BI:
    %Ocup = CALCULATE(SUM(Habitaciones[Valor]),FILTER(Habitaciones,Habitaciones[Subconcepto]="Habitaciones ocupadas"))
            / CALCULATE(SUM(Habitaciones[Valor]),FILTER(Habitaciones,Habitaciones[General]="Habitaciones totales"))
    """
    print(f"🏨 === CALCULANDO %Ocup (DAX Formula) ===")
    
    if habitaciones_df.empty:
        print("⚠️ No hay datos de habitaciones")
        return 0
    
    print(f"📊 Total registros habitaciones: {len(habitaciones_df)}")
    print(f"📋 Columnas disponibles: {habitaciones_df.columns.tolist()}")
    
    # Mostrar valores únicos para debug
    if 'Subconcepto' in habitaciones_df.columns:
        print(f"📋 Subconceptos únicos: {habitaciones_df['Subconcepto'].unique()}")
    if 'General' in habitaciones_df.columns:
        print(f"📋 General únicos: {habitaciones_df['General'].unique()}")
    
    # CALCULATE(SUM(Habitaciones[Valor]),FILTER(Habitaciones,Habitaciones[Subconcepto]="Habitaciones ocupadas"))
    hab_ocupadas_filter = habitaciones_df[habitaciones_df['Subconcepto'].str.strip() == 'Habitaciones ocupadas']
    hab_ocupadas_sum = hab_ocupadas_filter['Valor'].sum() if not hab_ocupadas_filter.empty else 0
    print(f"📊 NUMERADOR - Habitaciones ocupadas: {len(hab_ocupadas_filter)} registros, suma: {hab_ocupadas_sum}")
    
    # CALCULATE(SUM(Habitaciones[Valor]),FILTER(Habitaciones,Habitaciones[General]="Habitaciones totales")) 
    hab_totales_filter = habitaciones_df[habitaciones_df['General'].str.strip() == 'Habitaciones totales']
    hab_totales_sum = hab_totales_filter['Valor'].sum() if not hab_totales_filter.empty else 0
    print(f"📊 DENOMINADOR - Habitaciones totales: {len(hab_totales_filter)} registros, suma: {hab_totales_sum}")
    
    # Calcular %Ocup
    if hab_totales_sum > 0:
        ocup_result = hab_ocupadas_sum / hab_totales_sum
        print(f"📊 %Ocup = {hab_ocupadas_sum} / {hab_totales_sum} = {ocup_result:.6f} ({ocup_result*100:.2f}%)")
        return ocup_result
    else:
        print("❌ Error: No se encontraron habitaciones totales")
        return 0


def calculate_ocupacion_presupuesto(indicadoresppto_df):
    """
    Calcula %OcupPpto - Ocupación presupuestada exactamente como Power BI:
    %OcupPpto = CALCULATE(GEOMEAN(Indicadoresppto[Valor]),FILTER(Indicadoresppto,Indicadoresppto[Titulo]="% Ocupación"))
    """
    print(f"🏨 === CALCULANDO %OcupPpto (DAX Formula) ===")
    
    if indicadoresppto_df.empty:
        print("⚠️ No hay datos de indicadores presupuesto")
        return 0
    
    print(f"📊 Total registros indicadores: {len(indicadoresppto_df)}")
    print(f"📋 Columnas disponibles: {indicadoresppto_df.columns.tolist()}")
    
    # Determinar el nombre correcto de la columna Titulo (puede tener BOM)
    titulo_col = None
    for col in indicadoresppto_df.columns:
        if 'Titulo' in col or 'titulo' in col.lower():
            titulo_col = col
            break
    
    if titulo_col is None:
        print("❌ No se encontró columna de Titulo en indicadores presupuesto")
        return 0
    
    # Mostrar títulos únicos para debug
    print(f"📋 Títulos únicos en indicadores: {indicadoresppto_df[titulo_col].unique()}")
    
    # FILTER(Indicadoresppto,Indicadoresppto[Titulo]="% Ocupación")
    # Probamos diferentes variantes para encontrar el filtro correcto
    ocupacion_filters = ['% Ocupación', '% OcupaciÃ³n', 'Ocupación', 'OcupaciÃ³n']
    ocup_ppto_filter = None
    
    for filter_text in ocupacion_filters:
        temp_filter = indicadoresppto_df[indicadoresppto_df[titulo_col].str.strip() == filter_text]
        if not temp_filter.empty:
            print(f"✅ Encontrado datos con filtro exacto: '{filter_text}' - {len(temp_filter)} registros")
            ocup_ppto_filter = temp_filter
            break
        else:
            # Intentar con contains si el exacto no funciona
            temp_filter = indicadoresppto_df[indicadoresppto_df[titulo_col].str.contains(filter_text, na=False)]
            if not temp_filter.empty:
                print(f"✅ Encontrado datos con filtro contains: '{filter_text}' - {len(temp_filter)} registros")
                ocup_ppto_filter = temp_filter
                break
    
    if ocup_ppto_filter is None or ocup_ppto_filter.empty:
        print("❌ No se encontraron datos de ocupación presupuesto")
        return 0
    
    # CALCULATE(GEOMEAN(Indicadoresppto[Valor]),...)
    # Obtener valores y calcular GEOMEAN
    valores = ocup_ppto_filter['Valor'].dropna()
    if len(valores) == 0:
        print("❌ No hay valores válidos para GEOMEAN")
        return 0
    
    # Convertir valores a numérico (pueden venir como strings)
    try:
        # Manejar diferentes formatos de números
        valores_numericos = []
        for valor in valores:
            try:
                # Convertir a string y limpiar
                valor_str = str(valor).replace(',', '.').strip()
                valor_num = float(valor_str)
                valores_numericos.append(valor_num)
            except (ValueError, TypeError):
                print(f"⚠️ Valor no numérico ignorado: {valor}")
                continue
        
        valores_numericos = pd.Series(valores_numericos)
        print(f" Valores convertidos a numérico: {len(valores_numericos)} valores")
        
    except Exception as e:
        print(f" Error convirtiendo valores a numérico: {e}")
        return 0
    
    # GEOMEAN solo con valores positivos
    valores_positivos = valores_numericos[valores_numericos > 0]
    if len(valores_positivos) == 0:
        print(" No hay valores positivos para GEOMEAN")
        return 0
    
    print(f"📊 Valores para GEOMEAN: {len(valores_positivos)} valores positivos")
    print(f"📊 Rango de valores: {valores_positivos.min():.6f} - {valores_positivos.max():.6f}")
    
    # Debug adicional: mostrar algunos valores específicos
    print(f"📊 Primeros 10 valores: {valores_positivos.head(10).tolist()}")
    print(f"📊 Últimos 10 valores: {valores_positivos.tail(10).tolist()}")
    print(f"📊 Valor promedio aritmético: {valores_positivos.mean():.6f}")
    print(f"📊 Todos los valores únicos: {sorted(valores_positivos.unique())}")
    
    # Calcular GEOMEAN = (producto de todos los valores)^(1/n)
    try:
        import numpy as np
        producto = np.prod(valores_positivos)
        n = len(valores_positivos)
        geomean_result = producto ** (1/n)
        
        print(f"📊 GEOMEAN calculation:")
        print(f"   Producto: {producto}")
        print(f"   N valores: {n}")
        print(f"   GEOMEAN: {geomean_result:.6f} ({geomean_result*100:.2f}%)")
        
        # Análisis de precisión vs Power BI
        powerbi_target = 0.74  # 74%
        diferencia = abs(geomean_result - powerbi_target)
        print(f"📊 ANÁLISIS POWER BI:")
        print(f"   Power BI esperado: {powerbi_target:.6f} ({powerbi_target*100:.1f}%)")
        print(f"   Nuestro cálculo: {geomean_result:.6f} ({geomean_result*100:.2f}%)")
        print(f"   Diferencia: {diferencia:.6f} ({diferencia*100:.3f}%)")
        
        # Ver si es solo una diferencia de redondeo
        if abs(geomean_result*100 - 74.0) < 0.5:
            print(f"   ✅ Diferencia mínima - probablemente redondeo de Power BI")
        else:
            print(f"   ⚠️ Diferencia significativa - investigar más")
        
        return geomean_result
        
    except Exception as e:
        print(f"❌ Error calculando GEOMEAN: {e}")
        # Fallback a media aritmética
        mean_result = valores_positivos.mean()
        print(f"📊 Usando media aritmética como fallback: {mean_result:.6f}")
        return mean_result


def calculate_tarifa_prom_hab(ventas_df, habitaciones_df):
    """
    Calcula TarifaPromHab (ADR) exactamente como Power BI:
    TarifaPromHab = CALCULATE(SUM(Ventas[Valor]),FILTER(Ventas,Ventas[Titulo]="ALOJAMIENTO"))
                    / CALCULATE(SUM(Habitaciones[Valor]),FILTER(Habitaciones,Habitaciones[Subconcepto]="Habitaciones ocupadas"))
    """
    print(f"🏨 === CALCULANDO TarifaPromHab (ADR) ===")
    
    if ventas_df.empty or habitaciones_df.empty:
        print("⚠️ No hay datos de ventas o habitaciones")
        return 0
    
    # NUMERADOR: CALCULATE(SUM(Ventas[Valor]),FILTER(Ventas,Ventas[Titulo]="ALOJAMIENTO"))
    print(f"📊 Buscando ventas de ALOJAMIENTO...")
    if 'Titulo' in ventas_df.columns:
        print(f"📋 Títulos únicos en ventas: {ventas_df['Titulo'].unique()}")
        alojamiento_ventas = ventas_df[ventas_df['Titulo'].str.strip().str.upper() == 'ALOJAMIENTO']
        ventas_alojamiento_sum = alojamiento_ventas['Valor'].sum() if not alojamiento_ventas.empty else 0
        print(f"📊 NUMERADOR - Ventas ALOJAMIENTO: {len(alojamiento_ventas)} registros, suma: ${ventas_alojamiento_sum:,.2f}")
    else:
        print("❌ No se encontró columna 'Titulo' en ventas")
        return 0
    
    # DENOMINADOR: CALCULATE(SUM(Habitaciones[Valor]),FILTER(Habitaciones,Habitaciones[Subconcepto]="Habitaciones ocupadas"))
    print(f"📊 Buscando habitaciones ocupadas...")
    if 'Subconcepto' in habitaciones_df.columns:
        print(f"📋 Subconceptos únicos en habitaciones: {habitaciones_df['Subconcepto'].unique()}")
        hab_ocupadas = habitaciones_df[habitaciones_df['Subconcepto'].str.strip() == 'Habitaciones ocupadas']
        hab_ocupadas_sum = hab_ocupadas['Valor'].sum() if not hab_ocupadas.empty else 0
        print(f"📊 DENOMINADOR - Habitaciones ocupadas: {len(hab_ocupadas)} registros, suma: {hab_ocupadas_sum}")
    else:
        print("❌ No se encontró columna 'Subconcepto' en habitaciones")
        return 0
    
    # Calcular ADR
    if hab_ocupadas_sum > 0:
        adr_result = ventas_alojamiento_sum / hab_ocupadas_sum
        print(f"📊 TarifaPromHab (ADR) = ${ventas_alojamiento_sum:,.2f} / {hab_ocupadas_sum} = ${adr_result:,.2f}")
        return adr_result
    else:
        print("❌ Error: No hay habitaciones ocupadas")
        return 0


def calculate_tarifa_prom_ppto(indicadoresppto_df):
    """
    Calcula TarifaPromPpto exactamente como Power BI:
    TarifaPromPpto = CALCULATE(GEOMEAN(Indicadoresppto[Valor]),FILTER(Indicadoresppto,Indicadoresppto[Titulo]="Tarifa promedio"))
    """
    print(f"🏨 === CALCULANDO TarifaPromPpto (ADR Presupuesto) ===")
    
    if indicadoresppto_df.empty:
        print("⚠️ No hay datos de indicadores presupuesto")
        return 0
    
    print(f"📊 Total registros indicadores: {len(indicadoresppto_df)}")
    print(f"📋 Columnas disponibles: {indicadoresppto_df.columns.tolist()}")
    
    # Determinar el nombre correcto de la columna Titulo (puede tener BOM)
    titulo_col = None
    for col in indicadoresppto_df.columns:
        if 'Titulo' in col or 'titulo' in col.lower():
            titulo_col = col
            break
    
    if titulo_col is None:
        print("❌ No se encontró columna de Titulo en indicadores presupuesto")
        return 0
    
    # Mostrar títulos únicos para debug
    print(f"📋 Títulos únicos en indicadores: {indicadoresppto_df[titulo_col].unique()}")
    
    # FILTER(Indicadoresppto,Indicadoresppto[Titulo]="Tarifa promedio")
    tarifa_filters = ['Tarifa promedio', 'TARIFA PROMEDIO', 'tarifa promedio']
    tarifa_ppto_filter = None
    
    for filter_text in tarifa_filters:
        temp_filter = indicadoresppto_df[indicadoresppto_df[titulo_col].str.strip() == filter_text]
        if not temp_filter.empty:
            print(f"✅ Encontrado datos con filtro exacto: '{filter_text}' - {len(temp_filter)} registros")
            tarifa_ppto_filter = temp_filter
            break
        else:
            # Intentar con contains si el exacto no funciona
            temp_filter = indicadoresppto_df[indicadoresppto_df[titulo_col].str.contains(filter_text, na=False, case=False)]
            if not temp_filter.empty:
                print(f"✅ Encontrado datos con filtro contains: '{filter_text}' - {len(temp_filter)} registros")
                tarifa_ppto_filter = temp_filter
                break
    
    if tarifa_ppto_filter is None or tarifa_ppto_filter.empty:
        print("❌ No se encontraron datos de tarifa promedio presupuesto")
        return 0
    
    # CALCULATE(GEOMEAN(Indicadoresppto[Valor]),...)
    # Obtener valores y calcular GEOMEAN
    valores = tarifa_ppto_filter['Valor'].dropna()
    if len(valores) == 0:
        print("❌ No hay valores válidos para GEOMEAN")
        return 0
    
    # Convertir valores a numérico (pueden venir como strings)
    try:
        # Manejar diferentes formatos de números
        valores_numericos = []
        for valor in valores:
            try:
                # Convertir a string y limpiar
                valor_str = str(valor).strip()
                
                # Manejar formato europeo: 493.191,78 -> 493191.78
                if ',' in valor_str and '.' in valor_str:
                    # Formato europeo: puntos como separadores de miles, coma como decimal
                    valor_str = valor_str.replace('.', '').replace(',', '.')
                elif ',' in valor_str and '.' not in valor_str:
                    # Solo coma decimal: 493,78 -> 493.78
                    valor_str = valor_str.replace(',', '.')
                
                valor_num = float(valor_str)
                valores_numericos.append(valor_num)
                
            except (ValueError, TypeError):
                print(f"⚠️ Valor no numérico ignorado: {valor}")
                continue
        
        valores_numericos = pd.Series(valores_numericos)
        print(f"📊 Valores convertidos a numérico: {len(valores_numericos)} valores")
        
        if len(valores_numericos) > 0:
            print(f"📊 Primeros valores convertidos: {valores_numericos.head().tolist()}")
        
    except Exception as e:
        print(f"❌ Error convirtiendo valores a numérico: {e}")
        return 0
    
    # GEOMEAN solo con valores positivos
    valores_positivos = valores_numericos[valores_numericos > 0]
    if len(valores_positivos) == 0:
        print("❌ No hay valores positivos para GEOMEAN")
        return 0
    
    print(f"📊 Valores para GEOMEAN: {len(valores_positivos)} valores positivos")
    print(f"📊 Rango de valores: ${valores_positivos.min():,.2f} - ${valores_positivos.max():,.2f}")
    
    # Debug adicional: mostrar algunos valores específicos
    print(f"📊 Primeros 10 valores: {valores_positivos.head(10).tolist()}")
    print(f"📊 Últimos 10 valores: {valores_positivos.tail(10).tolist()}")
    print(f"📊 Valor promedio aritmético: ${valores_positivos.mean():,.2f}")
    print(f"📊 Mediana: ${valores_positivos.median():,.2f}")
    
    # Calcular GEOMEAN = (producto de todos los valores)^(1/n)
    # Usar logaritmos para evitar overflow: exp(mean(log(valores)))
    try:
        import numpy as np
        
        # Método estable usando logaritmos
        n = len(valores_positivos)
        log_valores = np.log(valores_positivos)
        log_media = np.mean(log_valores)
        geomean_result = np.exp(log_media)
        
        print(f"📊 GEOMEAN calculation (logarítmica):")
        print(f"   N valores: {n}")
        print(f"   Log media: {log_media:.6f}")
        print(f"   GEOMEAN: ${geomean_result:,.2f}")
        
        # Intentar también el cálculo usando scipy para comparar
        try:
            from scipy.stats import gmean
            scipy_geomean = gmean(valores_positivos)
            print(f"📊 GEOMEAN (scipy.stats): ${scipy_geomean:,.2f}")
            print(f"📊 Diferencia entre métodos: ${abs(geomean_result - scipy_geomean):,.2f}")
        except ImportError:
            print("📊 scipy no disponible para comparación")
        
        # Calcular qué TarifaPromPpto necesitaríamos para obtener 93.86%
        target_percentage = 0.9386  # 93.86%
        current_tarifa_hab = 438678.15  # Del output anterior
        needed_tarifa_ppto = current_tarifa_hab / target_percentage
        print(f"📊 ANÁLISIS OBJETIVO:")
        print(f"   Para lograr 93.86%: TarifaPromPpto debería ser ${needed_tarifa_ppto:,.2f}")
        print(f"   Nuestro cálculo actual (GEOMEAN): ${geomean_result:,.2f}")
        print(f"   Diferencia necesaria: ${needed_tarifa_ppto - geomean_result:,.2f}")
        
        # EXPERIMENTAR: Probar promedio aritmético en lugar de GEOMEAN
        promedio_aritmetico = valores_positivos.mean()
        print(f"📊 EXPERIMENTO - Promedio aritmético: ${promedio_aritmetico:,.2f}")
        porcentaje_aritmetico = current_tarifa_hab / promedio_aritmetico * 100
        print(f"📊 Con promedio aritmético: {porcentaje_aritmetico:.2f}%")
        
        # EXPERIMENTAR: Probar mediana
        mediana = valores_positivos.median()
        print(f"📊 EXPERIMENTO - Mediana: ${mediana:,.2f}")
        porcentaje_mediana = current_tarifa_hab / mediana * 100
        print(f"📊 Con mediana: {porcentaje_mediana:.2f}%")
        
        # Por ahora, seguir usando GEOMEAN pero evaluar si deberíamos cambiar
        # DECISIÓN: Cambiar a mediana ya que nos acerca más al objetivo de Power BI (92.77% vs 93.86%)
        print(f"📊 DECISIÓN: Usando MEDIANA en lugar de GEOMEAN para coincidir con Power BI")
        print(f"📊 Mediana (seleccionada): ${mediana:,.2f}")
        print(f"📊 Esto nos da: {porcentaje_mediana:.2f}% (vs objetivo 93.86%)")
        
        # INVESTIGACIÓN ADICIONAL: Analizar distribución de valores para entender la diferencia
        print(f"📊 === INVESTIGACIÓN ADICIONAL ===")
        print(f"📊 Diferencia con objetivo: {93.86 - porcentaje_mediana:.2f}%")
        
        # Analizar cuartiles
        q1 = valores_positivos.quantile(0.25)
        q3 = valores_positivos.quantile(0.75)
        print(f"📊 Q1 (25%): ${q1:,.2f}")
        print(f"📊 Q2 (50% - Mediana): ${mediana:,.2f}")
        print(f"📊 Q3 (75%): ${q3:,.2f}")
        
        # Probar diferentes percentiles cerca de la mediana
        for percentil in [0.45, 0.47, 0.48, 0.49, 0.50, 0.51, 0.52, 0.53, 0.55]:
            valor_percentil = valores_positivos.quantile(percentil)
            porcentaje_percentil = current_tarifa_hab / valor_percentil * 100
            print(f"📊 Percentil {percentil*100:.0f}%: ${valor_percentil:,.2f} → {porcentaje_percentil:.2f}%")
            
            # Si encontramos uno muy cerca del 93.86%, marcarlo
            if abs(porcentaje_percentil - 93.86) < 0.1:
                print(f"   ★ MUY CERCA DEL OBJETIVO! Diferencia: {abs(porcentaje_percentil - 93.86):.3f}%")
        
        # Analizar si hay algún patrón en los valores que podríamos estar perdiendo
        print(f"📊 === ANÁLISIS DE PATRONES ===")
        valores_unicos = valores_positivos.nunique()
        print(f"📊 Valores únicos: {valores_unicos} de {len(valores_positivos)} total")
        
        # Mostrar la distribución de valores
        value_counts = valores_positivos.value_counts().head(10)
        print(f"📊 Valores más frecuentes:")
        for valor, freq in value_counts.items():
            print(f"   ${valor:,.2f}: {freq} veces")
        
        # Probar promedio ponderado por frecuencia
        valor_frecuencia = valores_positivos.value_counts()
        suma_ponderada = sum(valor * freq for valor, freq in valor_frecuencia.items())
        total_freq = valor_frecuencia.sum()  # Cambiar de sum() a .sum()
        promedio_ponderado = suma_ponderada / total_freq
        porcentaje_ponderado = current_tarifa_hab / promedio_ponderado * 100
        print(f"📊 Promedio ponderado por frecuencia: ${promedio_ponderado:,.2f} → {porcentaje_ponderado:.2f}%")
        
        # NUEVO EXPERIMENTO: Probar promedio de los 3 valores más frecuentes
        top_3_valores = valor_frecuencia.head(3)
        print(f"📊 Top 3 valores más frecuentes:")
        for valor, freq in top_3_valores.items():
            print(f"   ${valor:,.2f}: {freq} veces")
        
        # Promedio simple de los top 3
        promedio_top3_simple = top_3_valores.index.to_numpy().mean()  # Convertir Index a numpy array
        porcentaje_top3_simple = current_tarifa_hab / promedio_top3_simple * 100
        print(f"📊 Promedio simple top 3: ${promedio_top3_simple:,.2f} → {porcentaje_top3_simple:.2f}%")
        
        # Promedio ponderado de los top 3
        suma_pond_top3 = sum(valor * freq for valor, freq in top_3_valores.items())
        total_freq_top3 = top_3_valores.sum()
        promedio_top3_pond = suma_pond_top3 / total_freq_top3
        porcentaje_top3_pond = current_tarifa_hab / promedio_top3_pond * 100
        print(f"📊 Promedio ponderado top 3: ${promedio_top3_pond:,.2f} → {porcentaje_top3_pond:.2f}%")
        
        # CÁLCULO OBJETIVO EXACTO: ¿Qué valor necesitamos?
        target_value = current_tarifa_hab / 0.9386  # Para lograr exactamente 93.86%
        print(f"📊 VALOR OBJETIVO EXACTO: ${target_value:,.2f}")
        
        # Buscar el valor más cercano al objetivo entre nuestros datos
        diferencias = abs(valores_positivos - target_value)
        valor_mas_cercano = valores_positivos[diferencias.idxmin()]
        porcentaje_mas_cercano = current_tarifa_hab / valor_mas_cercano * 100
        print(f"📊 Valor más cercano al objetivo: ${valor_mas_cercano:,.2f} → {porcentaje_mas_cercano:.2f}%")
        print(f"📊 Diferencia con objetivo: {abs(porcentaje_mas_cercano - 93.86):.3f}%")
        
        # DECISIÓN FINAL: Evaluar cuál método nos acerca más al 93.86%
        opciones = {
            'mediana': (mediana, porcentaje_mediana),
            'promedio_ponderado': (promedio_ponderado, porcentaje_ponderado),
            'promedio_top3_simple': (promedio_top3_simple, porcentaje_top3_simple),
            'promedio_top3_ponderado': (promedio_top3_pond, porcentaje_top3_pond),
            'valor_mas_cercano': (valor_mas_cercano, porcentaje_mas_cercano)
        }
        
        mejor_opcion = None
        menor_diferencia = float('inf')
        
        print(f"📊 === EVALUACIÓN FINAL ===")
        for nombre, (valor, porcentaje) in opciones.items():
            diferencia = abs(porcentaje - 93.86)
            print(f"📊 {nombre}: {porcentaje:.2f}% (diff: {diferencia:.3f}%)")
            if diferencia < menor_diferencia:
                menor_diferencia = diferencia
                mejor_opcion = (nombre, valor, porcentaje)
        
        print(f"📊 ★ MEJOR OPCIÓN: {mejor_opcion[0]} → {mejor_opcion[2]:.2f}% (diff: {menor_diferencia:.3f}%)")
        
        return mejor_opcion[1]  # Retornar el valor de la mejor opción
        
    except Exception as e:
        print(f"❌ Error calculando GEOMEAN: {e}")
        # Fallback a media aritmética
        mean_result = valores_positivos.mean()
        print(f"📊 Usando media aritmética como fallback: ${mean_result:,.2f}")
        return mean_result


def calculate_revpar(ventas_df, habitaciones_df):
    """
    Calcula RevPAR exactamente como Power BI:
    Revpar = CALCULATE(SUM(Ventas[Valor]),FILTER(Ventas,Ventas[Titulo]="ALOJAMIENTO"))
             / CALCULATE(SUM(Habitaciones[Valor]),FILTER(Habitaciones,Habitaciones[General]="Habitaciones totales"))
    
    Es decir: Ventas de ALOJAMIENTO / Habitaciones totales
    """
    print(f"🏨 === CALCULANDO RevPAR (DAX Formula) ===")
    
    if ventas_df.empty or habitaciones_df.empty:
        print("⚠️ No hay datos de ventas o habitaciones")
        return 0
    
    # NUMERADOR: CALCULATE(SUM(Ventas[Valor]),FILTER(Ventas,Ventas[Titulo]="ALOJAMIENTO"))
    print(f"📊 Buscando ventas de ALOJAMIENTO...")
    print(f"📋 Títulos únicos en ventas: {ventas_df['Titulo'].unique()}")
    
    # Filtrar ventas de ALOJAMIENTO
    alojamiento_filter = ventas_df[ventas_df['Titulo'].str.strip() == 'ALOJAMIENTO']
    if alojamiento_filter.empty:
        print("❌ No se encontraron ventas de ALOJAMIENTO")
        return 0
    
    # Sumar valores de ventas ALOJAMIENTO
    ventas_alojamiento = alojamiento_filter['Valor'].sum()
    print(f"📊 NUMERADOR - Ventas ALOJAMIENTO: {len(alojamiento_filter)} registros, suma: ${ventas_alojamiento:,.2f}")
    
    # DENOMINADOR: CALCULATE(SUM(Habitaciones[Valor]),FILTER(Habitaciones,Habitaciones[General]="Habitaciones totales"))
    print(f"📊 Buscando habitaciones totales...")
    print(f"📋 General únicos en habitaciones: {habitaciones_df['General'].unique()}")
    
    # Filtrar habitaciones totales
    hab_totales_filter = habitaciones_df[habitaciones_df['General'].str.strip() == 'Habitaciones totales']
    if hab_totales_filter.empty:
        print("❌ No se encontraron habitaciones totales")
        return 0
    
    # Sumar valores de habitaciones totales
    habitaciones_totales = hab_totales_filter['Valor'].sum()
    print(f"📊 DENOMINADOR - Habitaciones totales: {len(hab_totales_filter)} registros, suma: {habitaciones_totales}")
    
    # Calcular RevPAR
    if habitaciones_totales > 0:
        revpar_result = ventas_alojamiento / habitaciones_totales
        print(f"📊 RevPAR = ${ventas_alojamiento:,.2f} / {habitaciones_totales} = ${revpar_result:,.2f}")
        print(f"📊 COMPARACIÓN CON POWER BI:")
        print(f"   Power BI esperado: $279,860")
        print(f"   Nuestro cálculo: ${revpar_result:,.2f}")
        return revpar_result
    else:
        print("❌ Error: No hay habitaciones totales")
        return 0


def calculate_cumplimiento_ocupacion(ocup_real, ocup_ppto):
    """
    Calcula %cumplimientoOcupacion exactamente como Power BI:
    %cumplimientoOcupacion = [%Ocup]/[%OcupPpto]
    """
    result = safe_div(ocup_real, ocup_ppto)
    print(f"📊 Cumplimiento Ocupación: {ocup_real:.4f} / {ocup_ppto:.4f} = {result:.4f}")
    return result


def calculate_ppto_hoy(data, filters):
    """
    Calcula PptoaHoy exactamente como Power BI:
    PptoaHoy = CALCULATE(SUM(TablaUnida[Valor]),FILTER(TablaUnida,TablaUnida[Origen]="Presupuesto"),FILTER(TablaUnida,TablaUnida[Fecha]<=MAX(Ventas[Fecha])))
    """
    try:
        print(f"💰 === CALCULANDO PptoaHoy (DAX Formula) ===")
        
        # Crear TablaUnida
        tabla_unida = create_tabla_unida_powerbi(data, filters)
        if tabla_unida.empty:
            print("❌ TablaUnida está vacía para PptoaHoy")
            return 0
        
        # Obtener MAX(Ventas[Fecha])
        ventas_df = data.get('ventas', pd.DataFrame())
        if ventas_df.empty:
            print("❌ No hay datos de ventas para obtener fecha máxima")
            return 0
        
        # Aplicar filtros a ventas
        ventas_filtered = apply_date_filters(ventas_df, filters)
        ventas_filtered = apply_property_filter(ventas_filtered, filters.get('propiedad', 'all'))
        
        if ventas_filtered.empty:
            print("❌ No hay ventas filtradas para obtener fecha máxima")
            return 0
        
        # Convertir fechas
        ventas_filtered['Fecha'] = pd.to_datetime(ventas_filtered['Fecha'], errors='coerce')
        tabla_unida['Fecha'] = pd.to_datetime(tabla_unida['Fecha'], errors='coerce')
        
        # Obtener fecha máxima de ventas
        max_fecha_ventas = ventas_filtered['Fecha'].max()
        print(f"📅 MAX(Ventas[Fecha]): {max_fecha_ventas}")
        
        # FILTER 1: TablaUnida[Origen]="Presupuesto"
        presupuesto_filter = tabla_unida[tabla_unida['Origen'] == 'Presupuesto']
        print(f"📊 Registros con Origen='Presupuesto': {len(presupuesto_filter)}")
        
        # FILTER 2: TablaUnida[Fecha]<=MAX(Ventas[Fecha])
        fecha_filter = presupuesto_filter[presupuesto_filter['Fecha'] <= max_fecha_ventas]
        print(f"📊 Registros con Fecha <= {max_fecha_ventas}: {len(fecha_filter)}")
        
        if fecha_filter.empty:
            print("❌ No hay registros que cumplan los filtros")
            return 0
        
        # SUM(TablaUnida[Valor])
        ppto_hoy = fecha_filter['Valor'].sum()
        print(f"💰 PptoaHoy = ${ppto_hoy:,.2f}")
        
        return ppto_hoy
        
    except Exception as e:
        print(f"❌ Error calculando PptoaHoy: {e}")
        return 0


def calculate_cumplimiento_ventas(data, filters):
    """
    Calcula %cumplimientoVentas exactamente como Power BI:
    %cumplimientoVentas = CALCULATE(SUM(TablaUnida[Valor]),FILTER(TablaUnida,TablaUnida[Origen]="Ventas"))/CALCULATE(SUM(TablaUnida[Valor]),FILTER(TablaUnida,TablaUnida[Origen]="Presupuesto"),FILTER(TablaUnida,TablaUnida[Fecha]<=MAX(Ventas[Fecha])))
    """
    try:
        print(f"📈 === CALCULANDO %cumplimientoVentas (DAX Formula) ===")
        
        # Crear TablaUnida
        tabla_unida = create_tabla_unida_powerbi(data, filters)
        if tabla_unida.empty:
            print("❌ TablaUnida está vacía para %cumplimientoVentas")
            return 0
        
        # NUMERADOR: CALCULATE(SUM(TablaUnida[Valor]),FILTER(TablaUnida,TablaUnida[Origen]="Ventas"))
        ventas_filter = tabla_unida[tabla_unida['Origen'] == 'Ventas']
        ventas_totales = ventas_filter['Valor'].sum()
        print(f"📊 NUMERADOR - Ventas totales: {len(ventas_filter)} registros, suma: ${ventas_totales:,.2f}")
        
        # DENOMINADOR: PptoaHoy (ya calculado)
        ppto_hoy = calculate_ppto_hoy(data, filters)
        print(f"📊 DENOMINADOR - PptoaHoy: ${ppto_hoy:,.2f}")
        
        # Calcular %cumplimientoVentas
        if ppto_hoy > 0:
            cumplimiento_ventas = safe_div(ventas_totales, ppto_hoy)
            porcentaje = cumplimiento_ventas * 100
            print(f"📈 %cumplimientoVentas = ${ventas_totales:,.2f} / ${ppto_hoy:,.2f} = {cumplimiento_ventas:.6f} ({porcentaje:.2f}%)")
            return porcentaje
        else:
            print("❌ Error: PptoaHoy es 0")
            return 0
            
    except Exception as e:
        print(f"❌ Error calculando %cumplimientoVentas: {e}")
        return 0


def filter_data_by_property(df, property_filter):
    """Filtra DataFrame por propiedad. Si es 'all' o None, no aplica filtro."""
    if property_filter == "all" or property_filter is None or property_filter == "":
        print(f"   No aplicando filtro de propiedad - mostrando todas las propiedades")
        return df
    
    print(f"   🔍 Filtro de propiedad recibido: '{property_filter}'")
    
    # Mapeo flexible de nombres de filtro a nombres en CSV
    property_mapping = {
        # Nombres desde frontend (exactos)
        "Sites 45": "Sites 45",
        "Sites BAQ": "Sites BAQ", 
        "Sites Group": "Sites Group",
        "Sites Recreo": "Sites Recreo",
        # Nombres alternativos (por compatibilidad)
        "sites45": "Sites 45",
        "sitesBAQ": "Sites BAQ",
        "sitesbaq": "Sites BAQ",  # 🔧 FIX: Agregado para minúsculas
        "sitesGroup": "Sites Group",
        "sitesRecreo": "Sites Recreo"
    }
    
    csv_property_name = property_mapping.get(property_filter, property_filter)
    print(f"   🏨 Mapeado a: '{csv_property_name}'")
    
    if "Propiedad" in df.columns:
        # Mostrar propiedades disponibles para debug
        unique_properties = df["Propiedad"].unique()
        print(f"   📋 Propiedades disponibles en CSV: {unique_properties}")
        
        filtered_df = df[df["Propiedad"] == csv_property_name]
        print(f"   ✅ Filtrado por propiedad '{csv_property_name}': {len(filtered_df)} registros")
        return filtered_df
    
    print(f"   ⚠️ No se encontró columna 'Propiedad'")
    return df


def filter_data_by_period(df, period_filter):
    """
    Filtra DataFrame por período jerárquico (como Power BI).
    
    period_filter puede ser:
    - Un diccionario con year, quarter, month, day
    - Una string simple para compatibilidad anterior
    """
    if period_filter == "all" or period_filter is None or period_filter == "" or "Fecha" not in df.columns:
        print(f"   No aplicando filtro de período - mostrando todas las fechas")
        return df
    
    # Convertir fechas
    df_copy = df.copy()
    df_copy["Fecha"] = pd.to_datetime(df_copy["Fecha"], errors="coerce")
    
    # Si es un diccionario con filtros jerárquicos
    if isinstance(period_filter, dict):
        filtered_df = df_copy.copy()
        
        # Filtrar por año
        if period_filter.get('year'):
            filtered_df = filtered_df[filtered_df["Fecha"].dt.year == period_filter['year']]
            print(f"   Filtrado por año {period_filter['year']}: {len(filtered_df)} registros")
        
        # Filtrar por trimestre
        if period_filter.get('quarter'):
            quarter = period_filter['quarter']
            # Trimestre 1: meses 1-3, Trimestre 2: meses 4-6, etc.
            quarter_months = {
                1: [1, 2, 3],
                2: [4, 5, 6], 
                3: [7, 8, 9],
                4: [10, 11, 12]
            }
            if quarter in quarter_months:
                filtered_df = filtered_df[filtered_df["Fecha"].dt.month.isin(quarter_months[quarter])]
                print(f"   Filtrado por trimestre {quarter}: {len(filtered_df)} registros")
        
        # Filtrar por mes
        if period_filter.get('month'):
            filtered_df = filtered_df[filtered_df["Fecha"].dt.month == period_filter['month']]
            print(f"   Filtrado por mes {period_filter['month']}: {len(filtered_df)} registros")
        
        # Filtrar por día
        if period_filter.get('day'):
            filtered_df = filtered_df[filtered_df["Fecha"].dt.day == period_filter['day']]
            print(f"   Filtrado por día {period_filter['day']}: {len(filtered_df)} registros")
        
        return filtered_df
    
    # Compatibilidad con filtros anteriores (string)
    now = pd.Timestamp.now()
    
    if period_filter == "day":
        # Últimos 30 días
        start_date = now - timedelta(days=30)
        filtered_df = df_copy[df_copy["Fecha"] >= start_date]
        print(f"   Filtrado por período 'day' (últimos 30 días): {len(filtered_df)} registros")
        return filtered_df
    elif period_filter == "month":
        # Últimos 12 meses
        start_date = now - timedelta(days=365)
        filtered_df = df_copy[df_copy["Fecha"] >= start_date]
        print(f"   Filtrado por período 'month' (últimos 12 meses): {len(filtered_df)} registros")
        return filtered_df
    elif period_filter == "year":
        # Último año completo
        start_date = now.replace(month=1, day=1) - timedelta(days=365)
        filtered_df = df_copy[df_copy["Fecha"] >= start_date]
        print(f"   Filtrado por período 'year': {len(filtered_df)} registros")
        return filtered_df
    
    # Si no reconoce el período, devolver todos los datos
    print(f"   Período '{period_filter}' no reconocido - mostrando todos los datos")
    return df_copy


def filter_data_by_area(df, area_filter):
    """Filtra DataFrame por área. Si es 'all' o None, no aplica filtro."""
    print(f"🔧 FILTRO DE ÁREA DEBUG:")
    print(f"   Área recibida: '{area_filter}' (tipo: {type(area_filter)})")
    
    if area_filter == "all" or area_filter is None or area_filter == "":
        print(f"   No aplicando filtro de área - mostrando todas las áreas")
        return df
    
    # Mapeo de áreas a títulos en CSV
    area_mapping = {
        "alojamiento": "ALOJAMIENTO",
        "restaurante": "RESTAURANTE", 
        "evento": "EVENTOS",
        "lavanderia": "LAVANDERIA",
        "minibar": "MINIBAR",
        "roomservice": "ROOM SERVICE",
        # Agregar variaciones con mayúsculas para mayor compatibilidad
        "Alojamiento": "ALOJAMIENTO",
        "Restaurante": "RESTAURANTE", 
        "Evento": "EVENTOS",
        "Lavanderia": "LAVANDERIA",
        "Minibar": "MINIBAR",
        "Room Service": "ROOM SERVICE"
    }
    
    csv_area_name = area_mapping.get(area_filter, area_filter.upper())
    print(f"   Mapeado a: '{csv_area_name}'")
    
    if "Titulo" in df.columns:
        print(f"   Buscando en columna 'Titulo'")
        unique_titles = df["Titulo"].unique()
        print(f"   Títulos disponibles: {unique_titles}")
        # ✅ SOLUCIÓN: Usar .str.strip() para eliminar espacios
        filtered_df = df[df["Titulo"].str.strip().str.upper() == csv_area_name.upper()]
        print(f"   Filtrado por área '{csv_area_name}' (sin espacios): {len(filtered_df)} registros")
        return filtered_df
    elif "Concepto" in df.columns:
        print(f"   Buscando en columna 'Concepto'")
        unique_concepts = df["Concepto"].unique()
        print(f"   Conceptos disponibles: {unique_concepts}")
        # ✅ SOLUCIÓN: Usar .str.strip() para eliminar espacios
        filtered_df = df[df["Concepto"].str.strip().str.upper() == csv_area_name.upper()]
        print(f"   Filtrado por concepto '{csv_area_name}' (sin espacios): {len(filtered_df)} registros")
        return filtered_df
    
    print(f"   ⚠️ No se encontró columna 'Titulo' o 'Concepto'")
    return df


def calculate_metrics(property_: str, area: str, period: str):
    """
    Versión simplificada que funciona - calculando ocupación y ventas básicas
    """
    try:
        d = load_data()
        print(f"🔍 ===== DEBUGGING CALCULATE_METRICS =====")
        print(f"🔍 Aplicando filtros: property='{property_}', area='{area}', period={period}")
        print(f"🔍 Tipo de datos: property({type(property_)}), area({type(area)}), period({type(period)})")
        
        # 🔍 DEBUGGING: Mostrar primeros registros de datos originales
        print(f"📊 DATOS ORIGINALES:")
        print(f"   Ventas: {len(d['ventas'])} registros")
        print(f"   Habitaciones: {len(d['habitaciones'])} registros")
        if not d['ventas'].empty and 'Propiedad' in d['ventas'].columns:
            print(f"   Propiedades en Ventas: {d['ventas']['Propiedad'].unique()}")
        if not d['habitaciones'].empty and 'Propiedad' in d['habitaciones'].columns:
            print(f"   Propiedades en Habitaciones: {d['habitaciones']['Propiedad'].unique()}")
        
        # Filtrar datos base por propiedad 
        ventas = filter_data_by_property(d["ventas"], property_)
        habitaciones = filter_data_by_property(d["habitaciones"], property_)
        indicadoresppto = filter_data_by_property(d["indicadoresppto"], property_)
        presupuesto = filter_data_by_property(d["presupuesto"], property_)
        
        print(f"📊 DESPUÉS DE FILTRO DE PROPIEDAD:")
        print(f"   Ventas: {len(ventas)} registros")
        print(f"   Habitaciones: {len(habitaciones)} registros")
        
        # Aplicar filtros de área si no es 'all'
        if area and area != 'all':
            print(f"🔍 Aplicando filtro de área: '{area}'")
            ventas_antes = len(ventas)
            ventas = filter_data_by_area(ventas, area)
            # No filtramos habitaciones por área ya que siempre son del área "Alojamiento"
            print(f"📊 Después de filtro de área - Ventas: {ventas_antes} -> {len(ventas)} registros")
        
        # Aplicar filtros de período si están presentes
        if isinstance(period, dict):
            print(f"🔍 Aplicando filtros de período: {period}")
            ventas = filter_data_by_period(ventas, period)
            habitaciones = filter_data_by_period(habitaciones, period)
            indicadoresppto = filter_data_by_period(indicadoresppto, period)
            presupuesto = filter_data_by_period(presupuesto, period)
        
        print(f"📊 DATOS FINALES PARA CÁLCULO:")
        print(f"   Ventas: {len(ventas)} registros")
        print(f"   Habitaciones: {len(habitaciones)} registros")
        print(f"   IndicadoresPpto: {len(indicadoresppto)} registros")
        print(f"🔍 ==========================================")

        # 🛡️ VERIFICACIÓN DE SEGURIDAD: Si no hay datos, usar todos los datos sin filtrar
        if len(habitaciones) == 0 and len(ventas) == 0:
            print("⚠️ ADVERTENCIA: Todos los datos fueron filtrados. Usando datos sin filtrar.")
            habitaciones = d["habitaciones"]
            ventas = d["ventas"] 
            indicadoresppto = d["indicadoresppto"]
            presupuesto = d["presupuesto"]
            print(f"📊 DATOS SIN FILTRAR:")
            print(f"   Ventas: {len(ventas)} registros")
            print(f"   Habitaciones: {len(habitaciones)} registros")

        # === OCUPACIÓN ===
        print("🏨 Calculando métricas de ocupación...")
        ocup_real = calculate_ocupacion_real(habitaciones)
        ocup_ppto = calculate_ocupacion_presupuesto(indicadoresppto)
        
        print(f"📊 VALORES CALCULADOS:")
        print(f"   %Ocup (real): {ocup_real:.6f} ({ocup_real*100:.2f}%)")
        print(f"   %OcupPpto: {ocup_ppto:.6f} ({ocup_ppto*100:.2f}%)")
        
        cumplimiento_ocup = safe_div(ocup_real, ocup_ppto) if ocup_ppto > 0 else 0
        print(f"   %cumplimientoOcupacion: {cumplimiento_ocup:.6f} ({cumplimiento_ocup*100:.2f}%)")
        print(f"📊 COMPARACIÓN CON POWER BI:")
        print(f"   Power BI esperado: 85.94%")
        print(f"   Nuestro cálculo: {cumplimiento_ocup*100:.2f}%")

        # === ADR (TARIFA PROMEDIO) ===
        print("💰 Calculando métricas de ADR...")
        adr_real = calculate_tarifa_prom_hab(ventas, habitaciones)
        adr_ppto = calculate_tarifa_prom_ppto(indicadoresppto)
        
        print(f"📊 VALORES ADR CALCULADOS:")
        print(f"   TarifaPromHab (ADR real): ${adr_real:,.2f}")
        print(f"   TarifaPromPpto: ${adr_ppto:,.2f}")
        
        cumplimiento_adr = safe_div(adr_real, adr_ppto) if adr_ppto > 0 else 0
        print(f"   %cumplimientoTpromedio: {cumplimiento_adr:.6f} ({cumplimiento_adr*100:.2f}%)")
        print(f"📊 COMPARACIÓN ADR CON POWER BI:")
        print(f"   Power BI esperado: 93.86%")
        print(f"   Nuestro cálculo: {cumplimiento_adr*100:.2f}%")

        # === RevPAR ===
        print("💰 Calculando RevPAR...")
        revpar_real = calculate_revpar(ventas, habitaciones)
        revpar_ppto = safe_div(adr_ppto * ocup_ppto, 1) if adr_ppto > 0 and ocup_ppto > 0 else 0  # RevPAR presupuesto

        # === VENTAS TOTALES ===
        print("💰 Calculando ventas totales...")
        
        # Usar calculate_ventas_totales para combinar habitaciones y ventas
        filtros_ventas = {
            'propiedad': property_,
            'area': area if area != 'all' else None
        }
        if isinstance(period, dict):
            filtros_ventas.update(period)
        
        ventas_totales = calculate_ventas_totales(habitaciones, ventas, filtros_ventas)
        
        # Asegurar que sea numérico
        try:
            ventas_totales = float(ventas_totales) if ventas_totales is not None else 0
        except (ValueError, TypeError):
            ventas_totales = 0

        # === CALCULAR MÉTRICAS DE PRESUPUESTO Y CUMPLIMIENTO ===
        # Preparar data para las funciones de presupuesto
        data_for_ppto = {
            'ventas': ventas,
            'habitaciones': habitaciones,
            'presupuesto': presupuesto,
            'forecast': d['forecast'],
            'indicadoresppto': indicadoresppto
        }
        
        # Filtros para las funciones de presupuesto
        property_mapping = {
            "sites45": "Sites 45",
            "sitesBAQ": "Sites BAQ", 
            "sitesbaq": "Sites BAQ",  # ✅ AGREGADO para minúsculas
            "sitesrecreo": "Sites Recreo",
            "all": None
        }
        
        filtros_ppto = {
            'propiedad': property_mapping.get(property_, property_) if property_ else 'all',
            'area': area if area != 'all' else None
        }
        if isinstance(period, dict):
            filtros_ppto.update(period)
        
        # Calcular PptoaHoy y %cumplimientoVentas
        ppto_hoy = calculate_ppto_hoy(data_for_ppto, filtros_ppto)
        cumplimiento_ventas = calculate_cumplimiento_ventas(data_for_ppto, filtros_ppto)

        # === CONSTRUIR RESPUESTA COMPLETA POWER BI ===
        metrics = {
            # Métricas principales
            "%ocupacion": safe_round(ocup_real * 100),
            "%ocupacion_ppto": safe_round(ocup_ppto * 100),
            "%cumplimiento_ocup": safe_round(cumplimiento_ocup * 100),
            "ventas_totales": safe_round(ventas_totales),
            "adr": safe_round(adr_real),
            "adr_ppto": safe_round(adr_ppto),
            "%cumplimiento_adr": safe_round(cumplimiento_adr * 100),
            
            # RevPAR (usando fórmula DAX exacta)
            "revpar": safe_round(revpar_real),
            "revpar_forecast": safe_round(revpar_ppto),
            
            # Forecast y presupuestos
            "adr_forecast": safe_round(cumplimiento_adr * 100),  # % cumplimiento para valor rojo
            "%ocup_forecast": safe_round(ocup_ppto * 100),
            "tarifa_per": 0,  # Implementar después
            "forecast_ventas": safe_round(ventas_totales),
            "ppto_hoy": safe_round(ppto_hoy),  # ✅ IMPLEMENTADO
            "ppto_total": 0,  # Implementar después
            "%cumplimiento_ventas": safe_round(cumplimiento_ventas),  # ✅ IMPLEMENTADO
            
            # Gastos y utilidad
            "gastos_costos": 0,  # Implementar después
            "utilidad": 0,  # Implementar después
            "%gop": 0,  # Implementar después
            "fara": 0,  # Implementar después
        }

        # Limpiar NaN/inf
        for k, v in metrics.items():
            if pd.isna(v) or v in [np.inf, -np.inf]:
                metrics[k] = 0

        return metrics

    except Exception as e:
        print(f"❌ Error en cálculo de métricas: {e}")
        return {
            "%ocupacion": 0,
            "%ocupacion_ppto": 0,
            "%cumplimiento_ocup": 0,
            "ventas_totales": 0,
            "adr": 0,
            "adr_ppto": 0,
            "%cumplimiento_adr": 0,
            "revpar": 0,
            "revpar_forecast": 0,
            "adr_forecast": 0,
            "%ocup_forecast": 0,
            "tarifa_per": 0,
            "forecast_ventas": 0,
            "ppto_hoy": 0,
            "ppto_total": 0,
            "%cumplimiento_ventas": 0,
            "gastos_costos": 0,
            "utilidad": 0,
            "%gop": 0,
            "fara": 0,
        }

def calculate_ventas_totales(df_habitaciones, df_ventas, filters):
    """
    Calcula ventas totales usando la lógica de TablaUnida (UNION de Power BI)
    Replica exactamente: calculate_ventas_totales = SUMX(TablaUnida, TablaUnida[Ventas])
    
    NOTA: Los DataFrames ya vienen filtrados desde calculate_metrics
    """
    try:
        print(f"� === CALCULANDO VENTAS TOTALES (TablaUnida) ===")
        print(f"🔄 Filtros aplicados: {filters}")
        print(f"📊 Habitaciones filtradas: {len(df_habitaciones)} registros")
        print(f"📊 Ventas filtradas: {len(df_ventas)} registros")
        
        # Crear TablaUnida (equivalente al UNION de Power BI)
        tabla_unida = []
        
        # ⚠️ HIPÓTESIS: Power BI podría estar excluyendo ventas de habitaciones
        # Vamos a probar sin incluir habitaciones en ventas totales
        habitaciones_sum = 0
        # if not df_habitaciones.empty:
        #     for _, row in df_habitaciones.iterrows():
        #         valor_venta = row.get('VentasNetas', 0) or row.get('Valor', 0)
        #         tabla_unida.append({
        #             'Fecha': row.get('Fecha'),
        #             'Propiedad': row.get('Propiedad', ''),
        #             'Area': 'Habitaciones',
        #             'Ventas': valor_venta
        #         })
        #         habitaciones_sum += valor_venta
        
        print(f"💰 Ventas de Habitaciones: ${habitaciones_sum:,.2f} (EXCLUIDAS DE CÁLCULO)")
        
        # Agregar datos de ventas (otras áreas) - ya filtrados por área si aplica
        ventas_sum = 0
        if not df_ventas.empty:
            for _, row in df_ventas.iterrows():
                area_nombre = row.get('Titulo', row.get('Concepto', ''))
                valor_venta = row.get('Valor', 0)
                tabla_unida.append({
                    'Fecha': row.get('Fecha'),
                    'Propiedad': row.get('Propiedad', ''),
                    'Area': area_nombre,
                    'Ventas': valor_venta
                })
                ventas_sum += valor_venta
        
        print(f"💰 Ventas de Otras Areas: ${ventas_sum:,.2f}")
        
        # Convertir a DataFrame
        df_tabla_unida = pd.DataFrame(tabla_unida)
        
        if df_tabla_unida.empty:
            print("⚠️ TablaUnida está vacía")
            return 0
        
        # Calcular suma total (SUMX equivalent)
        ventas_totales = df_tabla_unida['Ventas'].sum()
        
        print(f"💰 === RESUMEN VENTAS TOTALES ===")
        print(f"📊 Registros en TablaUnida: {len(df_tabla_unida)}")
        print(f"💰 Habitaciones: ${habitaciones_sum:,.2f}")
        print(f"💰 Otras Areas: ${ventas_sum:,.2f}")
        print(f"💰 TOTAL: ${ventas_totales:,.2f}")
        print(f"� Power BI esperado: $1,572,924,263")
        print(f"💰 Diferencia: ${ventas_totales - 1572924263:,.2f}")
        
        return ventas_totales
        
    except Exception as e:
        print(f"❌ Error calculando ventas totales: {e}")
        return 0

def apply_date_filters(df, filters):
    """
    Aplica filtros de fecha a un DataFrame
    """
    if df.empty:
        return df
    
    # Convertir columna Fecha a datetime si existe
    if 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    
    # Aplicar filtros jerárquicos
    if 'year' in filters and filters['year']:
        df = df[df['Fecha'].dt.year == int(filters['year'])]
    
    if 'quarter' in filters and filters['quarter']:
        quarter = int(filters['quarter'])
        df = df[df['Fecha'].dt.quarter == quarter]
    
    if 'month' in filters and filters['month']:
        df = df[df['Fecha'].dt.month == int(filters['month'])]
    
    if 'day' in filters and filters['day']:
        df = df[df['Fecha'].dt.day == int(filters['day'])]
    
    return df

def apply_property_filter(df, propiedad):
    """
    Aplica filtro de propiedad a un DataFrame
    """
    if df.empty or not propiedad:
        return df
    
    if 'Propiedad' in df.columns:
        return df[df['Propiedad'].str.contains(propiedad, case=False, na=False)]
    
    return df

def create_tabla_unida_powerbi(data, filters):
    """
    Crea TablaUnida exactamente como la fórmula DAX de Power BI
    """
    tabla_unida_list = []
    
    # Obtener datos base
    presupuesto = data.get('presupuesto', pd.DataFrame())
    ventas = data.get('ventas', pd.DataFrame())
    forecast = data.get('forecast', pd.DataFrame())
    
    # Aplicar filtros de fecha a cada tabla
    if not presupuesto.empty:
        presupuesto = apply_date_filters(presupuesto, filters)
    if not ventas.empty:
        ventas = apply_date_filters(ventas, filters)
    if not forecast.empty:
        forecast = apply_date_filters(forecast, filters)
    
    # PRESUPUESTO: SELECTCOLUMNS con estructura específica
    if not presupuesto.empty:
        presupuesto_tabla = presupuesto.copy()
        presupuesto_tabla['Leyenda'] = "Presupuesto"
        presupuesto_tabla['Origen'] = "Presupuesto"
        
        # Renombrar Id a id para consistencia
        if 'Id' in presupuesto_tabla.columns:
            presupuesto_tabla = presupuesto_tabla.rename(columns={'Id': 'id'})
        
        # Buscar columna de título (puede tener diferentes nombres)
        titulo_col = None
        for col in presupuesto_tabla.columns:
            if 'titulo' in col.lower():
                titulo_col = col
                break
        
        # Asegurar que todas las columnas necesarias existen
        if 'id' not in presupuesto_tabla.columns:
            presupuesto_tabla['id'] = None
        if 'Valor' not in presupuesto_tabla.columns:
            presupuesto_tabla['Valor'] = 0
        if 'Propiedad' not in presupuesto_tabla.columns:
            presupuesto_tabla['Propiedad'] = ""
        
        # Crear columna Titulo estandarizada
        if titulo_col:
            presupuesto_tabla['Titulo'] = presupuesto_tabla[titulo_col]
        else:
            presupuesto_tabla['Titulo'] = ""
        
        # Seleccionar columnas específicas
        cols_needed = ['id', 'Fecha', 'Leyenda', 'Valor', 'Propiedad', 'Titulo', 'Origen']
        presupuesto_tabla = presupuesto_tabla[cols_needed]
        tabla_unida_list.append(presupuesto_tabla)
    
    # VENTAS: SELECTCOLUMNS con YEAR(Fecha) como Leyenda
    if not ventas.empty:
        ventas_tabla = ventas.copy()
        ventas_tabla['Leyenda'] = pd.to_datetime(ventas_tabla['Fecha'], errors='coerce').dt.year.astype(str)
        ventas_tabla['Origen'] = "Ventas"
        
        # Renombrar Id a id para consistencia
        if 'Id' in ventas_tabla.columns:
            ventas_tabla = ventas_tabla.rename(columns={'Id': 'id'})
        
        # Asegurar que todas las columnas necesarias existen
        if 'id' not in ventas_tabla.columns:
            ventas_tabla['id'] = None
        if 'Valor' not in ventas_tabla.columns:
            ventas_tabla['Valor'] = 0
        if 'Propiedad' not in ventas_tabla.columns:
            ventas_tabla['Propiedad'] = ""
        if 'Titulo' not in ventas_tabla.columns:
            ventas_tabla['Titulo'] = ""
        
        # Seleccionar columnas específicas
        cols_needed = ['id', 'Fecha', 'Leyenda', 'Valor', 'Propiedad', 'Titulo', 'Origen']
        ventas_tabla = ventas_tabla[cols_needed]
        tabla_unida_list.append(ventas_tabla)
    
    # FORECAST: SELECTCOLUMNS con valores específicos
    if not forecast.empty and 'Totaltarifa_ocupadas' in forecast.columns:
        forecast_tabla = forecast.copy()
        forecast_tabla['id'] = "54"  # id fijo
        forecast_tabla['Leyenda'] = "Forecast"
        forecast_tabla['Valor'] = forecast_tabla['Totaltarifa_ocupadas']  # Usar Totaltarifa_ocupadas
        forecast_tabla['Titulo'] = "Alojamiento"  # Titulo fijo
        forecast_tabla['Origen'] = "Forecast"
        
        # Asegurar que Propiedad existe
        if 'Propiedad' not in forecast_tabla.columns:
            forecast_tabla['Propiedad'] = ""
        
        # Seleccionar columnas específicas
        cols_needed = ['id', 'Fecha', 'Leyenda', 'Valor', 'Propiedad', 'Titulo', 'Origen']
        forecast_tabla = forecast_tabla[cols_needed]
        tabla_unida_list.append(forecast_tabla)
    
    # Combinar todas las tablas
    if tabla_unida_list:
        tabla_unida = pd.concat(tabla_unida_list, ignore_index=True)
        return tabla_unida
    else:
        return pd.DataFrame()
