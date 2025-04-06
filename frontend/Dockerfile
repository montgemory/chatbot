FROM node:18-alpine AS base

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY package.json package-lock.json ./
RUN npm ci

# 构建应用
COPY . .
RUN npm run build

# 生产环境
FROM node:18-alpine AS production
WORKDIR /app

COPY --from=base /app/package.json .
COPY --from=base /app/package-lock.json .
COPY --from=base /app/next.config.js ./
COPY --from=base /app/public ./public
COPY --from=base /app/.next ./.next
COPY --from=base /app/node_modules ./node_modules

# 设置环境变量
ENV NODE_ENV=production
ENV PORT=3007

# 暴露端口
EXPOSE 3007

# 启动应用
CMD ["npm", "start"] 