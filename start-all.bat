@echo off
echo 启动聊天机器人应用...

echo 启动后端服务...
start cmd /k "cd %~dp0backend && python run.py"

echo 等待5秒后启动前端服务...
timeout /t 5 /nobreak

echo 清理和准备前端环境...
if exist frontend\.next (
  rmdir /s /q frontend\.next
)
mkdir frontend\.next

echo 启动前端服务...
start cmd /k "cd %~dp0frontend && set NODE_OPTIONS=--no-warnings && npm run dev"

echo 服务已启动！
echo 前端访问地址: http://localhost:3007
echo 后端API地址: http://localhost:3004 