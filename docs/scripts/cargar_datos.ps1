Write-Host "Cargando datos de prueba en el sistema TROLI..." -ForegroundColor Green
Get-Content .\scripts\cargar_datos_prueba.py | python manage.py shell
Write-Host "Proceso completado!" -ForegroundColor Green
Read-Host "Presiona Enter para continuar"
