# limpieza_windows.ps1 - revisa y limpia espacio en Windows, y lo anota en limpieza_log.txt
# Uso (en PowerShell, desde tu carpeta personal):
#   powershell -ExecutionPolicy Bypass -File .\limpieza_windows.ps1            solo revisa (no borra nada)
#   powershell -ExecutionPolicy Bypass -File .\limpieza_windows.ps1 limpiar    borra temporales y papelera
#   notepad $HOME\limpieza_log.txt                                             ver el historial

param([string]$Modo = "revisar")

$Log = Join-Path $HOME "limpieza_log.txt"
function Libre { "{0:N1} GB" -f ((Get-PSDrive C).Free / 1GB) }
function Anota([string]$texto) { Write-Output $texto; Add-Content -Path $Log -Value $texto -Encoding UTF8 }

Anota ("=== {0} · modo: {1} ===" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), $Modo)
Anota ("Espacio libre en C: " + (Libre))

Anota "Lo más grande en tu carpeta personal:"
Get-ChildItem $HOME -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
    $bytes = (Get-ChildItem $_.FullName -Recurse -File -Force -ErrorAction SilentlyContinue |
              Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{ Carpeta = $_.Name; Bytes = [double]$bytes }
} | Sort-Object Bytes -Descending | Select-Object -First 8 | ForEach-Object {
    Anota ("  {0,8:N1} GB  {1}" -f ($_.Bytes / 1GB), $_.Carpeta)
}

$descargas = Join-Path $HOME "Downloads"
$viejas = @(Get-ChildItem $descargas -File -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-90) }).Count
Anota "Descargas de hace más de 90 días: $viejas archivos"

if ($Modo -eq "limpiar") {
    Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "$env:LOCALAPPDATA\Microsoft\Windows\INetCache\*" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue   # solo funciona como administrador
    Clear-RecycleBin -Force -ErrorAction SilentlyContinue
    if (Get-Command npm -ErrorAction SilentlyContinue) { npm cache clean --force *> $null }
    if (Get-Command pip -ErrorAction SilentlyContinue) { pip cache purge *> $null }
    Anota ("Limpiado: temporales, caché de Windows, papelera, npm y pip. Espacio libre ahora: " + (Libre))
}
Add-Content -Path $Log -Value "" -Encoding UTF8
