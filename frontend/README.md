# Deepseek 聊天机器人前端

这是一个基于Next.js、React和TypeScript开发的Deepseek聊天机器人前端应用。

## 功能特点

- 基于Deepseek API的聊天机器人
- 流式响应（打字机效果）
- 会话历史记录保存和加载
- 响应式设计，适配不同设备

## 技术栈

- **Next.js** - React框架
- **TypeScript** - 类型安全
- **TailwindCSS** - 样式系统
- **React Hooks** - 状态管理

## 安装和运行

### 前提条件

- Node.js 18.0.0 或更高版本
- npm 或 yarn 包管理器

### 安装步骤

1. 克隆仓库或下载代码

2. 安装依赖
   ```bash
   npm install
   # 或
   yarn install
   ```

3. 配置环境变量
   创建 `.env.local` 文件并设置API地址:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:3004
   ```

4. 启动开发服务器
   ```bash
   npm run dev
   # 或
   yarn dev
   ```

5. 打开浏览器访问 http://localhost:3000

## 生产环境构建

```bash
npm run build
npm run start
# 或
yarn build
yarn start
```

## 后端API

该前端应用需要配合Deepseek聊天机器人后端API一起使用。详细的API文档请参考 `backend/API.md`。

## 项目结构

- `/app` - Next.js 应用页面
- `/components` - React 组件
- `/services` - API服务
- `/styles` - 全局样式
- `/types` - TypeScript 类型定义 