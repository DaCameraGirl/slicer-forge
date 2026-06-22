<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Slicer Forge" width="100%"/>
</p>

# slicer-forge

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸_English-1e293b?style=for-the-badge" alt="English"/></a>
    <a href="README.es.md"><img src="https://img.shields.io/badge/🇪🇸_Español-a78bfa?style=for-the-badge" alt="Español"/></a>
    <a href="README.fr.md"><img src="https://img.shields.io/badge/🇫🇷_Français-1e293b?style=for-the-badge" alt="Français"/></a>
    <a href="README.de.md"><img src="https://img.shields.io/badge/🇩🇪_Deutsch-1e293b?style=for-the-badge" alt="Deutsch"/></a>
    <a href="README.pt-BR.md"><img src="https://img.shields.io/badge/🇧🇷_Português-1e293b?style=for-the-badge" alt="Português"/></a>
</p>
<p align="center">
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/🇨🇳_中文-1e293b?style=for-the-badge" alt="中文"/></a>
    <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵_日本語-1e293b?style=for-the-badge" alt="日本語"/></a>
    <a href="README.ko.md"><img src="https://img.shields.io/badge/🇰🇷_한국어-1e293b?style=for-the-badge" alt="한국어"/></a>
    <a href="README.it.md"><img src="https://img.shields.io/badge/🇮🇹_Italiano-1e293b?style=for-the-badge" alt="Italiano"/></a>
    <a href="README.ar.md"><img src="https://img.shields.io/badge/🇸🇦_العربية-1e293b?style=for-the-badge" alt="العربية"/></a>
</p>

<p align="center">
  <img src="docs/assets/slicer-batch.svg" alt="Pipeline por lotes animado — carpetas pasan por de-id a volúmenes 3D" width="520"/>
</p>

<p align="center">
  <img src="docs/assets/deid-scanner.svg" alt="Desidentificación DICOM — escáner y nombres tachados" width="420"/>
</p>

<p align="center">
  <a href="https://github.com/DaCameraGirl/slicer-forge/actions/workflows/ci.yml"><img src="https://github.com/DaCameraGirl/slicer-forge/actions/workflows/ci.yml/badge.svg" alt="Lint"/></a>
  <img src="https://img.shields.io/badge/license-Apache--2.0-green.svg" alt="License"/>
  <img src="https://img.shields.io/badge/3D%20Slicer-extension-a78bfa.svg" alt="Slicer extension"/>
</p>

**Extensión de [3D Slicer](https://www.slicer.org/) que importa DICOM por lotes mediante [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge).**

`slicer-forge` añade el módulo **DICOM Forge Batch** a Slicer. Apunta a una carpeta DICOM y desidentifica cada serie (elimina nombres e IDs), ejecuta QC, convierte a NRRD y carga los volúmenes en la escena.

<p align="center">
  <img src="DicomForgeBatch/Resources/Icons/DicomForgeBatch.png" width="96" alt="DICOM Forge Batch icon">
</p>

## Diseño de dos repos

| Repo | Rol | Pruebas |
|------|------|--------|
| [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) | Pipeline headless | CI sin Slicer |
| **`slicer-forge`** | GUI fina en Slicer | Self-test en Slicer |

Igual que Slicer: ITK/VTK hacen el trabajo; la GUI es una capa. La lógica pesada vive en `dicom-forge`.

## Qué hace el módulo

1. **Instalar dependencias** — `pip_install('dicom-anvil[convert]')`.
2. **Elegir carpetas** — entrada DICOM y salida.
3. **Opciones** — nivel de desidentificación y formato.
4. **Ejecutar** — de-id → QC → convertir → cargar, con resumen PASS/FAIL.

📖 [Tutorial](docs/tutorial.md) · [Changelog](CHANGELOG.md)

## Instalación

### Desde fuente

```bash
git clone https://github.com/DaCameraGirl/slicer-forge.git
```

En Slicer: **Edit → Application Settings → Modules → Additional module paths**, añade `slicer-forge/DicomForgeBatch` y reinicia.

### Compilar como extensión

Layout estándar Slicer (`CMakeLists.txt`) para el [Extensions Index](https://github.com/Slicer/ExtensionsIndex).

## Anatomía del módulo

Cuatro clases en [`DicomForgeBatch/DicomForgeBatch.py`](DicomForgeBatch/DicomForgeBatch.py): metadata, widget GUI, lógica sin Qt, self-test.

## Pruebas

Self-test **dentro** de Slicer: *DicomForgeBatch*. CI: lint rápido + Slicer headless con pipeline completo.

> ⚠️ Desidentificación = reducción de riesgo, no garantía legal.

## Licencia

[Apache-2.0](LICENSE) © Angela Hudson
