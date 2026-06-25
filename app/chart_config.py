"""Shared chart configuration."""

from __future__ import annotations


# Fecha maxima visible en graficos basados en tiempo.
# Cambiala manualmente cuando quieras truncar la serie mensual.
#
# Ejemplos validos:
# CHARTS_MAX_DATE = "2026-05-31"
# CHARTS_MAX_DATE = "2026-04-30"
# CHARTS_MAX_DATE = None  # desactiva el truncamiento
CHARTS_MAX_DATE: str | None = "2026-06-21"
