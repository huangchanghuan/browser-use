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
)

async def main():   
    # logger.info("初始化Agent和LLM...")
    config = BrowserConfig(
        # chrome_instance_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        cdp_url="http://localhost:9222"
    )
    browser = Browser(config=config)                 
    agent = Agent(
        task="打开网址元宝https://yuanbao.tencent.com/chat/naQivTmsDa ，打开网页后，不要有其他操作，直接找到输入框，输入问题：今天天气怎样? 等待15秒，得到回复，把回复输出给我结果",
        llm=llm,
        browser=browser,
        use_vision=False

    )
    # logger.info("开始执行任务")
    await agent.run()
    # logger.info("任务执行完成")

if __name__ == "__main__":
    asyncio.run(main())