cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(SlicerForge)

# ----------------------------------------------------------------------------
# Extension metadata (consumed by the Slicer Extensions Index / Extension Manager)
# ----------------------------------------------------------------------------
set(EXTENSION_HOMEPAGE "https://github.com/DaCameraGirl/slicer-forge")
set(EXTENSION_CATEGORY "Informatics")
set(EXTENSION_CONTRIBUTORS "Angela Hudson (DaCameraGirl)")
set(EXTENSION_DESCRIPTION "Batch ingest, de-identify, quality-control, and import DICOM into 3D Slicer, powered by the dicom-forge pipeline.")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/DaCameraGirl/slicer-forge/main/DicomForgeBatch/Resources/Icons/DicomForgeBatch.png")
set(EXTENSION_SCREENSHOTURLS "")
set(EXTENSION_DEPENDS "NA")

# ----------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

add_subdirectory(DicomForgeBatch)

include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
