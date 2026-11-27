# SOUL: Operational Regulations

1. **АВТОЗАПУСК ЧЕРЕЗ API**: Всегда запускать воркеры через GitHub REST API (POST /repos/demkine776-sketch/mark-agent-core/actions/workflows/agent_worker.yml/dispatches).
2. **АВТОСОЗДАНИЕ ИНФРАСТРУКТУРЫ**: Скрипты обязаны проверять наличие бакетов/таблиц и создавать их через Supabase API.
3. **САМОЛЕЧЕНИЕ**:
   - Проверка статуса воркера через API: раз в 60 сек, макс 10 проверок.
   - При failure: анализ лога, исправление, перезапуск (макс 3 попытки).
   - При ошибке 429: переключение каскада (Gemini -> Groq -> OpenRouter).
