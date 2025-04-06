@echo off
echo 激活虚拟环境...
call venv\Scripts\activate

echo 启动服务器...
start cmd /k "python run.py"

echo 等待服务器启动...
timeout /t 5

echo 运行 API 测试...
python test_api.py

echo 运行流式响应测试...
python test_stream.py

echo 测试完成！
echo 服务器仍在运行中，可以在浏览器访问 http://localhost:3004/docs 测试 API
echo 请手动关闭服务器窗口以结束测试
pause 