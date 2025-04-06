@echo off
echo 重启聊天机器人应用...

echo 关闭现有进程...
taskkill /f /im node.exe > nul 2>&1
taskkill /f /im python.exe > nul 2>&1
timeout /t 2 /nobreak > nul

echo 清理前端缓存...
if exist frontend\.next (
  rmdir /s /q frontend\.next
  mkdir frontend\.next
)

echo 启动后端服务...
start cmd /k "cd %~dp0backend && python run.py"

echo 等待5秒后启动前端服务...
timeout /t 5 /nobreak

echo 启动前端服务...
start cmd /k "cd %~dp0frontend && set NODE_OPTIONS=--no-warnings && npm run dev"

echo 服务已重启！
echo 前端访问地址: http://localhost:3007
echo 后端API地址: http://localhost:3004 