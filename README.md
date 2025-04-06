# Deepseek 聊天机器人应用

这是一个使用Deepseek API的聊天机器人应用，包含前端和后端两部分。

## 技术架构

- 前端：Next.js (端口: 3007)
- 后端：FastAPI (端口: 3004)

## 快速启动

您可以使用以下批处理脚本快速启动应用：

1. 启动所有服务（推荐）:
   ```
   start-all.bat
   ```

2. 分别启动服务:
   ```
   start-backend.bat
   start-frontend.bat
   ```

## 手动启动

### 启动后端

```bash
cd backend
python run.py
```

后端服务将在 http://localhost:3004 上运行。

### 启动前端

```bash
cd frontend
# 完全清理Next.js构建文件（推荐）
if exist .next (rmdir /s /q .next)
mkdir .next
# 禁用警告信息
set NODE_OPTIONS=--no-warnings
# 启动服务
npm run dev
```

前端服务将在 http://localhost:3007 上运行。

## 访问应用

启动服务后，在浏览器中访问 http://localhost:3007 即可使用聊天机器人应用。

## 关于Webpack缓存警告

在首次启动前端时，您可能会看到类似以下的Webpack缓存警告：

```
<w> [webpack.cache.PackFileCacheStrategy] Restoring pack failed: TypeError: Cannot read properties of undefined (reading 'hasStartTime')
```

这是一个已知的Next.js/Webpack问题，不会影响应用的功能。我们通过以下方式处理:

1. 在每次启动前清理整个`.next`目录
2. 使用`NODE_OPTIONS=--no-warnings`抑制警告信息的显示

## 注意事项

- 确保在正确的目录中运行命令
- 前端和后端需要同时运行，应用才能正常工作
- 首次加载可能需要一点时间，请耐心等待 