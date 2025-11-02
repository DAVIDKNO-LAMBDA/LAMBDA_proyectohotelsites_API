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


def safe_div(a, b):
    """Evita divisiones por cero o valores NaN."""
    try:
        return a / b if b not in [0, None, np.nan] and not pd.isna(b) else 0
    except Exception:
        return 0


def calculate_metrics(property_: str, concept: str, period: str):
    d = load_data()
    ventas = d["ventas"]
    forecast = d["forecast"]
    habitaciones = d["habitaciones"]
    huespedes = d["huespedes"]
    expensas = d["expensas"]
    indicadoresppto = d["indicadoresppto"]
    propiedades = d["propiedades"]
    presupuesto = d["presupuesto"]

    try:
        # === % Ocupación ===
        hab_ocupadas = habitaciones.query('Subconcepto == "Habitaciones ocupadas"')["Valor"].sum() if "Subconcepto" in habitaciones.columns else 0
        hab_totales = habitaciones.query('General == "Habitaciones totales"')["Valor"].sum() if "General" in habitaciones.columns else 0
        ocup = safe_div(hab_ocupadas, hab_totales)

        # === % Ocupación Presupuestada ===
        ocup_ppto = 0
        if not indicadoresppto.empty and "Titulo" in indicadoresppto.columns and "Valor" in indicadoresppto.columns:
            val = indicadoresppto.query('Titulo == "% Ocupación"')["Valor"]
            if not val.empty:
                ocup_ppto = float(val.mean())

        cumplimiento_ocup = safe_div(ocup, ocup_ppto)

        # === ADR ===
        ventas_alo = ventas.query('Titulo == "ALOJAMIENTO"')["Valor"].sum() if "Titulo" in ventas.columns else 0
        adr = safe_div(ventas_alo, hab_ocupadas)

        # === RevPAR ===
        revpar = safe_div(ventas_alo, hab_totales)

        # === Forecast ===
        revpar_fc = forecast["Revpar"].mean() if "Revpar" in forecast.columns else 0
        adr_fc = forecast["Tarifa_promedio"].mean() if "Tarifa_promedio" in forecast.columns else 0
        ocup_fc = forecast["Porc_ocupacion"].mean() if "Porc_ocupacion" in forecast.columns else 0
        forecast_ventas = forecast["Totaltarifa_ocupadas"].sum() if "Totaltarifa_ocupadas" in forecast.columns else 0

        # === Tarifa Promedio (Per) ===
        huesp = huespedes.query('Subconcepto == "Huespedes"')["Valor"].sum() if "Subconcepto" in huespedes.columns else 0
        tarifa_per = safe_div(ventas_alo, huesp)

        # === Presupuesto ===
        ppto_total = presupuesto["Valor"].sum() if "Valor" in presupuesto.columns else 0
        max_fecha_ventas = ventas["Fecha"].max() if "Fecha" in ventas else None
        ppto_hoy = 0
        if max_fecha_ventas is not None and "Fecha" in presupuesto.columns:
            presupuesto["Fecha"] = pd.to_datetime(presupuesto["Fecha"], errors="coerce")
            ppto_hoy = presupuesto.query("Fecha <= @max_fecha_ventas")["Valor"].sum()

        # === Cumplimiento ventas ===
        cumplimiento_ventas = safe_div(ventas["Valor"].sum(), ppto_total)

        # === Gastos y Costos ===
        gastos = expensas["SaldoMes"].sum() if "SaldoMes" in expensas.columns else 0

        # === Utilidad y GOP ===
        utilidad = ventas["Valor"].sum() - gastos if "Valor" in ventas.columns else 0
        gop = safe_div(utilidad, ventas["Valor"].sum())

        # === FARA ===
        fara_factor = 0
        if not propiedades.empty:
            try:
                propiedades.columns = propiedades.columns[0].split(",")  # Corrige Propiedad,Fara sin separador
                fara_factor = float(propiedades["Fara"].iloc[0])
            except Exception:
                fara_factor = 0

        fara = ventas["Valor"].sum() * fara_factor if "Valor" in ventas.columns else 0

        # === Construir respuesta ===
        metrics = {
            "%ocupacion": round(ocup * 100, 2),
            "%ocupacion_ppto": round(ocup_ppto * 100, 2),
            "%cumplimiento_ocup": round(cumplimiento_ocup * 100, 2),
            "adr": round(adr, 2),
            "revpar": round(revpar, 2),
            "revpar_forecast": round(revpar_fc, 2),
            "adr_forecast": round(adr_fc, 2),
            "%ocup_forecast": round(ocup_fc * 100, 2),
            "tarifa_per": round(tarifa_per, 2),
            "forecast_ventas": round(forecast_ventas, 2),
            "ppto_hoy": round(ppto_hoy, 2),
            "ppto_total": round(ppto_total, 2),
            "%cumplimiento_ventas": round(cumplimiento_ventas * 100, 2),
            "gastos_costos": round(gastos, 2),
            "utilidad": round(utilidad, 2),
            "%gop": round(gop * 100, 2),
            "fara": round(fara, 2),
        }

        # 🔒 Limpieza final: reemplazar NaN/inf por 0
        for k, v in metrics.items():
            if pd.isna(v) or v in [np.inf, -np.inf]:
                metrics[k] = 0

        return metrics

    except Exception as e:
        print(f"❌ Error en cálculo de métricas: {e}")
        return {}
