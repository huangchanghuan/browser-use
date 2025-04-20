import logging
import os
import ssl

from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser
from browser_use import BrowserConfig
from httpx import Client, AsyncClient

import asyncio
from dotenv import load_dotenv

load_dotenv()

# 配置日志
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# logger = logging.getLogger(__name__)
print(os.getenv("OPENAI_API_KEY"))  # Should print your key
# 禁用 SSL 验证（不推荐用于生产环境）
os.environ['REQUESTS_CA_BUNDLE'] = ""
ssl._create_default_https_context = ssl._create_unverified_context
llm = ChatOpenAI(
    base_url="https://api.siliconflow.cn/v1/",
    model="Qwen/Qwen2.5-72B-Instruct-128K",
    api_key="sk-jgzpphkqtbjpdwkuqiaclvuussojnchgrdarirnwubmlfpkl",
    # base_url="https://api.hunyuan.cloud.tencent.com/v1/",
    # model="hunyuan-pro",
    # api_key="sk-VMGNgGpim4ztGDiQtx9Gzm6S92PcJeaabchVrqcmc2DLIb59",
    # base_url="https://ide.tools.cmic.site/app/tiangong/openai-service/8080/v1/",
    # model="deepseek-v3",
    # api_key="sk-lrhdwxwgnkrmqviiuzoqifucbpdddevpnucrvfehabiaxxmj",
    http_client=Client(verify=False, proxy="http://localhost:8888"),
    http_async_client=AsyncClient(verify=False, proxy="http://localhost:8888"),
    streaming=True  # 启用流式响应
)

async def main():   
    # logger.info("初始化Agent和LLM...")
    config = BrowserConfig(
        # chrome_instance_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        cdp_url="http://localhost:9222"
    )
    browser = Browser(config=config)                 
    agent = Agent(
        task="打开网址https://www.zhihu.com/question/waiting，抓取前面2个问题，并且进入问题详情页面，获取问题和问题详情，最后整理成一个markdown表格输出给我",
        llm=llm,
        browser=browser,
        use_vision=False

    )
    # logger.info("开始执行任务")
    await agent.run()
    # logger.info("任务执行完成")

if __name__ == "__main__":
    asyncio.run(main())