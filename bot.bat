@echo off
:menu
echo Choisissez une option :
echo 1 - Démarré
echo 2 - Arrêter
echo 3 - Quitter
set /p choice=Choix :

if "%choice%"=="1" (
    start "Nom de la fenêtre" python main.py
    echo Le script Python est en cours d'exécution en arrière-plan.
    goto menu
)

if "%choice%"=="2" (
    taskkill /IM python.exe /F
    echo Le script Python a été arrêté.
    goto menu
)

if "%choice%"=="3" (
    exit
)

echo Choix non valide. Réessayez.
goto menu
