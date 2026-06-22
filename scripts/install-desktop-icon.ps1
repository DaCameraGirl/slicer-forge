# Creates a "Slicer Forge" shortcut on your Desktop (purple 3D Slicer batch icon).
# Run once: powershell -ExecutionPolicy Bypass -File scripts\install-desktop-icon.ps1
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$icoPath = Join-Path $PSScriptRoot "slicer-forge.ico"

$size = 256
$bmp = New-Object System.Drawing.Bitmap $size, $size
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::Transparent)

$radius = 52
$path = New-Object System.Drawing.Drawing2D.GraphicsPath
$path.AddArc(0, 0, $radius, $radius, 180, 90)
$path.AddArc($size - $radius, 0, $radius, $radius, 270, 90)
$path.AddArc($size - $radius, $size - $radius, $radius, $radius, 0, 90)
$path.AddArc(0, $size - $radius, $radius, $radius, 90, 90)
$path.CloseFigure()

$rect = New-Object System.Drawing.Rectangle 0, 0, $size, $size
$purple = [System.Drawing.Color]::FromArgb(167, 139, 250)
$navy = [System.Drawing.Color]::FromArgb(15, 23, 42)
$brush = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rect, $purple, $navy, 45)
$g.FillPath($brush, $path)

$white = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::White)
$pts = @(
    [System.Drawing.Point]::new(128, 56),
    [System.Drawing.Point]::new(188, 168),
    [System.Drawing.Point]::new(68, 168)
)
$g.FillPolygon($white, $pts)
$g.FillPolygon([System.Drawing.Color]::FromArgb(56, 189, 248), @(
    [System.Drawing.Point]::new(128, 96),
    [System.Drawing.Point]::new(160, 152),
    [System.Drawing.Point]::new(96, 152)
))

$font = New-Object System.Drawing.Font("Segoe UI", 24, [System.Drawing.FontStyle]::Bold)
$fmt = New-Object System.Drawing.StringFormat
$fmt.Alignment = [System.Drawing.StringAlignment]::Center
$textRect = New-Object System.Drawing.RectangleF 0, 186, $size, 44
$g.DrawString("SF", $font, $white, $textRect, $fmt)
$g.Dispose()

$dim = $size
$lockRect = New-Object System.Drawing.Rectangle 0, 0, $dim, $dim
$bd = $bmp.LockBits($lockRect, [System.Drawing.Imaging.ImageLockMode]::ReadOnly, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$stride = $bd.Stride
$px = New-Object byte[] ($stride * $dim)
[System.Runtime.InteropServices.Marshal]::Copy($bd.Scan0, $px, 0, $px.Length)
$bmp.UnlockBits($bd)
$andSize = $dim * ($dim / 8)
$dibSize = 40 + ($dim * $dim * 4) + $andSize
$ico = New-Object System.IO.MemoryStream
$bw = New-Object System.IO.BinaryWriter $ico
$bw.Write([UInt16]0); $bw.Write([UInt16]1); $bw.Write([UInt16]1)
$bw.Write([Byte]0); $bw.Write([Byte]0); $bw.Write([Byte]0); $bw.Write([Byte]0)
$bw.Write([UInt16]1); $bw.Write([UInt16]32)
$bw.Write([UInt32]$dibSize); $bw.Write([UInt32]22)
$bw.Write([UInt32]40); $bw.Write([Int32]$dim); $bw.Write([Int32]($dim * 2))
$bw.Write([UInt16]1); $bw.Write([UInt16]32); $bw.Write([UInt32]0)
$bw.Write([UInt32]0); $bw.Write([Int32]0); $bw.Write([Int32]0)
$bw.Write([UInt32]0); $bw.Write([UInt32]0)
for ($y = $dim - 1; $y -ge 0; $y--) { $bw.Write($px, $y * $stride, $stride) }
$bw.Write((New-Object byte[] $andSize))
$bw.Flush()
[System.IO.File]::WriteAllBytes($icoPath, $ico.ToArray())

$ws = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath("Desktop")
$lnkPath = Join-Path $desktop "Slicer Forge.lnk"
$lnk = $ws.CreateShortcut($lnkPath)
$lnk.TargetPath = (Get-Command powershell).Source
$lnk.Arguments = "-ExecutionPolicy Bypass -NoProfile -File `"$($PSScriptRoot)\open-repo.ps1`""
$lnk.WorkingDirectory = $root
$lnk.IconLocation = "$icoPath,0"
$lnk.Description = "Slicer Forge - 3D Slicer DICOM batch import extension"
$lnk.Save()
Write-Host "Desktop shortcut created: $lnkPath" -ForegroundColor Green