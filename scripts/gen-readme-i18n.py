#!/usr/bin/env python3
"""Generate README.*.md translations for slicer-forge."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCENT = "a78bfa"
INACTIVE = "1e293b"
LANGS = ("es", "fr", "de", "pt-BR", "zh-CN", "ja", "ko", "it", "ar")

LANG_BAR = {
    "en": ("English", "🇺🇸"),
    "es": ("Español", "🇪🇸"),
    "fr": ("Français", "🇫🇷"),
    "de": ("Deutsch", "🇩🇪"),
    "pt-BR": ("Português", "🇧🇷"),
    "zh-CN": ("中文", "🇨🇳"),
    "ja": ("日本語", "🇯🇵"),
    "ko": ("한국어", "🇰🇷"),
    "it": ("Italiano", "🇮🇹"),
    "ar": ("العربية", "🇸🇦"),
}

T: dict[str, dict[str, str]] = {
    "en": {
        "tagline": "**A [3D Slicer](https://www.slicer.org/) extension that batch-imports DICOM through the [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) pipeline.**",
        "intro": "`slicer-forge` adds a **DICOM Forge Batch** module to Slicer. Point it at a folder of DICOM, and it de-identifies each series (removes patient names and IDs from headers), runs quality control, converts to NRRD, and loads the volumes straight into your Slicer scene — driven entirely by the headless, independently tested `dicom-forge` library.",
        "anim_alt": "Animated Slicer Forge batch pipeline — folders through de-id into 3D volumes",
        "deid_alt": "DICOM de-identification — x-ray scan with names redacted from paperwork",
        "two_h": "## The two-repo design",
        "two_table": """| Repo | Role | Tested |
|------|------|--------|
| [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) | Headless pipeline (ingest · de-id · QC · convert) | Unit-tested in CI without Slicer |
| **`slicer-forge`** (this) | Thin Slicer GUI on top of it | Self-test runs inside Slicer |""",
        "two_note": "This mirrors how Slicer itself is built (ITK/VTK do the work; the GUI is a shell on top). All the heavy logic lives in `dicom-forge`, so it is fully testable on its own; this repo stays a small, focused front-end.",
        "mod_h": "## What the module does",
        "mod": """1. **Install dependencies** — one button runs `pip_install('dicom-anvil[convert]')` into Slicer's own Python environment (the engine ships on PyPI as `dicom-anvil`; it still imports as `dicomforge`).
2. **Pick folders** — a DICOM input folder and an output folder.
3. **Choose options** — de-identification level (basic / moderate / strict) and output format (NRRD / NIfTI).
4. **Run** — every series is de-identified → QC'd → converted → loaded into the scene, with a per-series PASS/FAIL summary and warnings. Long runs stay responsive and can be cancelled.

📖 **New to the module?** Follow the step-by-step [usage tutorial](docs/tutorial.md). See the [changelog](CHANGELOG.md) for what has changed.""",
        "inst_h": "## Installation",
        "inst_src_h": "### From source (developer install)",
        "inst_src": """```bash
git clone https://github.com/DaCameraGirl/slicer-forge.git
```

In Slicer: **Edit → Application Settings → Modules → Additional module paths**, add the `slicer-forge/DicomForgeBatch` folder, and restart. The **DICOM Forge Batch** module appears under the *Informatics* category.""",
        "inst_build": "### Build as a loadable extension\n\nThe repo is laid out for the standard Slicer extension build (`CMakeLists.txt` + `slicerMacroBuildScriptedModule`) so it can be built against a Slicer build tree and submitted to the [Slicer Extensions Index](https://github.com/Slicer/ExtensionsIndex).",
        "anat_h": "## Module anatomy",
        "anat": """Slicer scripted modules use a fixed four-class shape — this one lives in [`DicomForgeBatch/DicomForgeBatch.py`](DicomForgeBatch/DicomForgeBatch.py):

- `DicomForgeBatch` — module metadata.
- `DicomForgeBatchWidget` — the GUI panel (built programmatically).
- `DicomForgeBatchLogic` — Qt-free logic wrapping `dicom-forge` (reusable from the Python console).
- `DicomForgeBatchTest` — a self-test that generates synthetic DICOM and runs the whole pipeline inside Slicer.""",
        "test_h": "## Testing",
        "test": """The self-test runs **inside** Slicer (it needs the `slicer` runtime):

> Slicer → **Developer Tools → Self Tests** → run *DicomForgeBatch*, or from the Python console: `slicer.util.selfTest('DicomForgeBatch')`.

CI runs on every push at two levels:

- a **fast lane** lint-checks and byte-compiles the module, and
- a **headless-Slicer lane** that downloads real 3D Slicer and runs the full pipeline end-to-end — de-id → QC → convert → load — across CT and MR, multiple series, both output formats, every de-identification level, and failure paths.

> ⚠️ De-identification is best-effort risk reduction, not a compliance guarantee. See [`dicom-forge`'s SECURITY policy](https://github.com/DaCameraGirl/dicom-forge/blob/main/SECURITY.md).""",
        "lic_h": "## License",
        "lic": "[Apache-2.0](LICENSE) © Angela Hudson",
    },
    "es": {
        "tagline": "**Extensión de [3D Slicer](https://www.slicer.org/) que importa DICOM por lotes mediante [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge).**",
        "intro": "`slicer-forge` añade el módulo **DICOM Forge Batch** a Slicer. Apunta a una carpeta DICOM y desidentifica cada serie (elimina nombres e IDs), ejecuta QC, convierte a NRRD y carga los volúmenes en la escena.",
        "anim_alt": "Pipeline por lotes animado — carpetas pasan por de-id a volúmenes 3D",
        "deid_alt": "Desidentificación DICOM — escáner y nombres tachados",
        "two_h": "## Diseño de dos repos",
        "two_table": "| Repo | Rol | Pruebas |\n|------|------|--------|\n| [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) | Pipeline headless | CI sin Slicer |\n| **`slicer-forge`** | GUI fina en Slicer | Self-test en Slicer |",
        "two_note": "Igual que Slicer: ITK/VTK hacen el trabajo; la GUI es una capa. La lógica pesada vive en `dicom-forge`.",
        "mod_h": "## Qué hace el módulo",
        "mod": "1. **Instalar dependencias** — `pip_install('dicom-anvil[convert]')`.\n2. **Elegir carpetas** — entrada DICOM y salida.\n3. **Opciones** — nivel de desidentificación y formato.\n4. **Ejecutar** — de-id → QC → convertir → cargar, con resumen PASS/FAIL.\n\n📖 [Tutorial](docs/tutorial.md) · [Changelog](CHANGELOG.md)",
        "inst_h": "## Instalación",
        "inst_src_h": "### Desde fuente",
        "inst_src": "```bash\ngit clone https://github.com/DaCameraGirl/slicer-forge.git\n```\n\nEn Slicer: **Edit → Application Settings → Modules → Additional module paths**, añade `slicer-forge/DicomForgeBatch` y reinicia.",
        "inst_build": "### Compilar como extensión\n\nLayout estándar Slicer (`CMakeLists.txt`) para el [Extensions Index](https://github.com/Slicer/ExtensionsIndex).",
        "anat_h": "## Anatomía del módulo",
        "anat": "Cuatro clases en [`DicomForgeBatch/DicomForgeBatch.py`](DicomForgeBatch/DicomForgeBatch.py): metadata, widget GUI, lógica sin Qt, self-test.",
        "test_h": "## Pruebas",
        "test": "Self-test **dentro** de Slicer: *DicomForgeBatch*. CI: lint rápido + Slicer headless con pipeline completo.\n\n> ⚠️ Desidentificación = reducción de riesgo, no garantía legal.",
        "lic_h": "## Licencia",
        "lic": "[Apache-2.0](LICENSE) © Angela Hudson",
    },
}

_OVERRIDES: dict[str, dict[str, str]] = {
    "fr": {
        "tagline": "**Extension [3D Slicer](https://www.slicer.org/) d'import DICOM par lots via [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge).**",
        "intro": "Ajoute **DICOM Forge Batch** a Slicer : de-identification (noms/IDs retires), QC, conversion NRRD, chargement des volumes.",
        "two_h": "## Architecture deux depots",
        "mod_h": "## Fonctions du module",
        "inst_h": "## Installation",
        "test_h": "## Tests",
        "lic_h": "## Licence",
    },
    "de": {
        "tagline": "**[3D Slicer](https://www.slicer.org/) Extension fur DICOM-Stapelimport uber [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge).**",
        "intro": "Fugt **DICOM Forge Batch** hinzu: De-Identifizierung, QC, NRRD-Konvertierung, Laden in die Szene.",
        "two_h": "## Zwei-Repo-Design",
        "mod_h": "## Modulfunktionen",
        "inst_h": "## Installation",
        "test_h": "## Tests",
        "lic_h": "## Lizenz",
    },
    "pt-BR": {
        "tagline": "**Extensao do [3D Slicer](https://www.slicer.org/) para importacao em lote via [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge).**",
        "intro": "Adiciona **DICOM Forge Batch**: desidentifica, QC, converte para NRRD e carrega volumes na cena.",
    },
    "zh-CN": {
        "tagline": "**通过 [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) 批量导入 DICOM 的 [3D Slicer](https://www.slicer.org/) 扩展。**",
        "intro": "添加 **DICOM Forge Batch** 模块：去标识化、QC、转 NRRD 并加载体数据。",
    },
    "ja": {
        "tagline": "**[`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) 経由で DICOM を一括取り込みする [3D Slicer](https://www.slicer.org/) 拡張。**",
        "intro": "**DICOM Forge Batch** を追加：匿名化、QC、NRRD 変換、シーンへ読み込み。",
    },
    "ko": {
        "tagline": "**[`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge) 파이프라인으로 DICOM 일괄 가져오기 [3D Slicer](https://www.slicer.org/) 확장.**",
        "intro": "**DICOM Forge Batch** 모듈: 비식별화, QC, NRRD 변환, 장면 로드.",
    },
    "it": {
        "tagline": "**Estensione [3D Slicer](https://www.slicer.org/) per import DICOM in batch via [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge).**",
        "intro": "Aggiunge **DICOM Forge Batch**: de-identificazione, QC, conversione NRRD, caricamento volumi.",
    },
    "ar": {
        "tagline": "**امتداد [3D Slicer](https://www.slicer.org/) لاستيراد DICOM دفعات عبر [`dicom-forge`](https://github.com/DaCameraGirl/dicom-forge).**",
        "intro": "يضيف **DICOM Forge Batch**: إزالة الهوية وQC وتحويل NRRD وتحميل الحجوم.",
    },
}

for _code, _patch in _OVERRIDES.items():
    T[_code] = {**T["en"], **_patch}


def lang_bar(active: str) -> str:
    keys = list(LANG_BAR.keys())
    rows = []
    for row_start in (0, 5):
        parts = []
        for k in keys[row_start : row_start + 5]:
            label, flag = LANG_BAR[k]
            href = "README.md" if k == "en" else f"README.{k}.md"
            color = ACCENT if k == active else INACTIVE
            parts.append(
                f'  <a href="{href}"><img src="https://img.shields.io/badge/{flag}_{label.replace(" ", "_")}-{color}?style=for-the-badge" alt="{label}"/></a>'
            )
        rows.append("<p align=\"center\">\n" + "\n  ".join(parts) + "\n</p>")
    return "\n".join(rows)


def render(lang: str) -> str:
    t = T.get(lang, T["en"])
    active = "en" if lang == "en" else lang
    return f"""<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Slicer Forge" width="100%"/>
</p>

# slicer-forge

{lang_bar(active)}

<p align="center">
  <img src="docs/assets/slicer-batch.svg" alt="{t['anim_alt']}" width="520"/>
</p>

<p align="center">
  <img src="docs/assets/deid-scanner.svg" alt="{t['deid_alt']}" width="420"/>
</p>

<p align="center">
  <a href="https://github.com/DaCameraGirl/slicer-forge/actions/workflows/ci.yml"><img src="https://github.com/DaCameraGirl/slicer-forge/actions/workflows/ci.yml/badge.svg" alt="Lint"/></a>
  <img src="https://img.shields.io/badge/license-Apache--2.0-green.svg" alt="License"/>
  <img src="https://img.shields.io/badge/3D%20Slicer-extension-{ACCENT}.svg" alt="Slicer extension"/>
</p>

{t['tagline']}

{t['intro']}

<p align="center">
  <img src="DicomForgeBatch/Resources/Icons/DicomForgeBatch.png" width="96" alt="DICOM Forge Batch icon">
</p>

{t['two_h']}

{t['two_table']}

{t['two_note']}

{t['mod_h']}

{t['mod']}

{t['inst_h']}

{t['inst_src_h']}

{t['inst_src']}

{t['inst_build']}

{t['anat_h']}

{t['anat']}

{t['test_h']}

{t['test']}

{t['lic_h']}

{t['lic']}
"""


def main() -> None:
    (ROOT / "README.md").write_text(render("en"), encoding="utf-8")
    for lang in LANGS:
        (ROOT / f"README.{lang}.md").write_text(render(lang), encoding="utf-8")
    print(f"Wrote README.md + {len(LANGS)} translations")


if __name__ == "__main__":
    main()