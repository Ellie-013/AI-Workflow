import asyncio
import time
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def main():
    async with AsyncWebCrawler(verbose=True, headless=True) as crawler:
        original_url = "https://36kr.com/information/travel/"
        session_id = 11

        # -----------------------------------------------------------------------------------
        # 第一步：点击文章链接触发跳转
        click_js = """
        (async () => {
            const links = document.querySelectorAll('a.article-item-description.ellipsis-2');
            if (links.length > 0) {
                links[0].click(); // 点击第一个链接
            }
        })();
        """
        # TODO: add scrolling to script all 24 hours
        click_result = await crawler.arun(
            url=original_url,
            config=CrawlerRunConfig(
                # js_code=[click_js],
                session_id=session_id,
                # js_only=False,
            #    css_selector=".article-mian-content"
               css_selector="div.article-item-info:has(*:contains('小时'))"
            ),
            simulate_user=True,
            override_navigator=True
        )
        # print(click_result.links["internal"][:100])
        print(len(click_result.links["internal"]))
        filtered_links = [link['href'] for link in click_result.links["internal"] if '/p/' in link['href']]
        print(len(filtered_links))
        print("!!!!!!!!!")
        print(filtered_links)
        
        
        time.sleep(6)  # 等待页面跳转完成（根据实际加载速度调整）
    #   # print(click_result.markdown)
    #     result = await crawler.arun(
    #         url=original_url,
    #         config=CrawlerRunConfig(
    #             session_id=11
    #         #    css_selector=".article-mian-content"
    #         ),
    #         simulate_user=True,
    #         override_navigator=True
    #     )
    #     print(result.markdown)
        # -----------------------------------------------------------------------------------
        # 第二步：获取新页面的当前 URL
        # get_current_url_js = "return window.location.href;"
        # current_url_config = CrawlerRunConfig(
        #     js_code=[get_current_url_js],
        #     session_id=session_id,
        #     js_only=True
        # )

        # url_result = await crawler.arun(
        #     url=original_url,  # 这里可能是旧 URL，但会沿用当前会话
        #     config=current_url_config
        # )
        
        # if not url_result or not url_result.success:
        #     print("无法获取新页面 URL，停止操作")
        #     return
        
        # new_url = url_result  # 移除可能的换行符/空格
        
        # print(f"新页面 URL：{new_url}")

        # # -----------------------------------------------------------------------------------
        # # 第三步：在新页面中执行 JS 提取 og:url
        # extract_js = """
        # (() => {
        #     const ogUrl = document.querySelector('meta[name="og:url"]');
        #     if (ogUrl) {
        #         return ogUrl.getAttribute('content');
        #     } else {
        #         return "未找到 og:url";
        #     }
        # })();
        # """
        
        # extract_config = CrawlerRunConfig(
        #     js_code=[extract_js],
        #     session_id=session_id,
        #     js_only=True
        # )

        # extract_result = await crawler.arun(
        #     url=new_url,  # 使用新获取的 URL
        #     config=extract_config,
        #     simulate_user=True,
        #     override_navigator=True
        # )
        
        # if extract_result.success:
        #     extracted_url = extract_result.result
        #     print(f"提取到的 og:url：{extracted_url}")
        # else:
        #     print(f"提取失败：{extract_result.error}")

asyncio.run(main())
