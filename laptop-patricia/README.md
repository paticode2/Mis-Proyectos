# Laptop de Patricia (Windows)

Última actualización: 26 oct 2026

## El equipo
| | |
|---|---|
| Modelo | HP Pavilion dv7 Notebook PC (serie dv7-6000, 2011–2012) |
| Procesador | AMD A8-3520M con gráficos integrados |
| RAM | 4 GB DDR3 1333 en "Bottom-Slot 2 (under)". **Slot 1 vacío.** Windows usa ~3 GB (el resto es para los gráficos). |
| Disco | Hitachi HTS547575A9E384, 750 GB, **disco mecánico de 5400 RPM** (lo que más la frena) |
| Sistema | Windows 10 (sin actualizaciones de seguridad desde oct 2025; este procesador no admite Windows 11) |

## Limpieza hecha (26 oct 2026)
- Borrado: Photoshop pirata (.rar de 4.7 GB, nunca instalado) con los archivos del crack, instalador de uTorrent e instalador de Google Play Games.
- Quitado del arranque: uTorrent Web (quedaba solo la entrada, sin programa).
- Iniciado escaneo completo de Windows Defender. **Falta ver el resultado.**
- Espacio libre en C: 584 GB. El espacio no es el problema; la lentitud es por la RAM y el disco.

## Pendiente
- [ ] Ver el resultado del escaneo (PowerShell):
      `Get-MpThreatDetection | Select-Object InitialDetectionTime, ActionSuccess, Resources`
- [x] Deshabilitados del arranque **EADM** (EA app) y **MicrosoftEdgeAutoLaunch** (26 oct 2026, por StartupApproved, igual que el Administrador de tareas). Quedan SecurityHealth, SynTPEnh (touchpad) y OneDrive.
- [ ] En Edge (`edge://settings/system`), apagar "Aumento de inicio" y las extensiones en segundo plano.
- [ ] Buscar el número de producto exacto: `Get-CimInstance Win32_ComputerSystem | Select-Object SystemSKUNumber` (o la etiqueta bajo la batería). Con él se busca el "HP Pavilion dv7 maintenance and service guide".

## Computadora nueva
Lista de compra por fases (torre con Windows): `computadora_nueva.md`.

## Qué comprar para que vaya más rápido (~$55)
Solo vale la pena si la torre nueva va a tardar meses. Si llega en semanas, no gastar.

1. **RAM: 1 × 4 GB DDR3 SODIMM 1333 (PC3-10600)**. 1600 también funciona. Va en el Slot 1, que está libre bajo la tapa de abajo. Llega a 8 GB, que es el máximo, y en doble canal, lo que además mejora los gráficos. ~$15
2. **SSD SATA 2.5" de 500 GB** (Crucial MX500, Samsung 870 EVO, WD Blue SA510 o Kingston A400). Reemplaza el disco clonándolo, o va en el segundo espacio para disco si el modelo lo tiene. Después sirve para la torre. ~$40

Comprobar la RAM después de instalarla (deben salir dos líneas de 4 GB):
`Get-CimInstance Win32_PhysicalMemory | Format-Table Capacity, Speed, DeviceLocator`

## Script de limpieza
`limpieza_windows.ps1` revisa el espacio y lo anota en `C:\Users\Patricia\limpieza_log.txt`. En la laptop está en `Descargas`:

```powershell
powershell -ExecutionPolicy Bypass -File $HOME\Downloads\limpieza_windows.ps1            # solo revisa
powershell -ExecutionPolicy Bypass -File $HOME\Downloads\limpieza_windows.ps1 limpiar    # borra temporales y papelera
notepad $HOME\limpieza_log.txt                                                           # ver el historial
```
