import uvicorn
import os
import logging
from dotenv import load_dotenv

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

if __name__ == "__main__":
    try:
        # 指定端口，默认为 3004
        port = int(os.getenv("PORT", 3004))
        
        logger.info(f"启动服务器，监听端口 {port}")
        
        # 启动 FastAPI 应用
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            reload=True,  # 开发模式启用热重载
            log_level="info"
        )
    except Exception as e:
        logger.error(f"启动服务器失败: {str(e)}")
        raise 