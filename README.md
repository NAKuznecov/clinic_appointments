🛠️ Быстрый запуск проекта
1. Клонируйте репозиторий:

 ` https://github.com/NAKuznecov/clinic_appointments.git `
2. Скопируйте файл окружения:

 ` cd clinic_appointment && cp .env.example .env `
3. Соберите и запустите контейнеры:

 ` docker compose up -d --build `
4. Проверьте работоспособность:

 ` curl http://localhost:8000/healthz `
