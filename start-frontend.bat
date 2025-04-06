@echo off
echo 正在启动前端服务...
cd frontend

echo 清理Next.js缓存和临时文件...
if exist .next (
  rmdir /s /q .next
)

echo 重新创建Next.js文件夹...
mkdir .next

echo 启动前端开发服务器...
set "NODE_OPTIONS=--no-warnings"
npm run dev 