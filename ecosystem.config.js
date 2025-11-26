module.exports = {
    apps: [{
        name: 'fastapi-todo-app',
        script: 'ToDoApp2/fastapienv/bin/uvicorn',
        args: 'ToDoApp2.main:app --host 0.0.0.0 --port 8000',
        cwd: '/Users/admin/Desktop/FastApi-main copy',
        instances: 1,
        autorestart: true,
        watch: false,
        max_memory_restart: '500M',
        env: {
            NODE_ENV: 'production',
            PYTHONUNBUFFERED: '1'
        },
        error_file: 'logs/pm2-error.log',
        out_file: 'logs/pm2-out.log',
        log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
        merge_logs: true,
        // Auto-restart on crash
        min_uptime: '10s',
        max_restarts: 10,
        // Restart at specific time daily (optional)
        cron_restart: '0 3 * * *'  // Restart at 3 AM daily
    }]
}
