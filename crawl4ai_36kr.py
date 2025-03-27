import asyncio
import time
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig,BrowserConfig


async def main():
    async with AsyncWebCrawler(verbose=True, headless=True) as crawler:
        original_url = "https://36kr.com/information/travel/"
        session_id = 11

        # -----------------------------------------------------------------------------------
        # 第一步：点击文章链接触发跳转
        # click_js = """
        # (async () => {
        #     const links = document.querySelectorAll('a.article-item-description.ellipsis-2');
        #     if (links.length > 0) {
        #         links[0].click(); // 点击第一个链接
        #     }
        # })();
        # """
        # TODO: add scrolling to script all 24 hours
        # 第一步：获取所有文章链接，且限定条件为24小时内的文章
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
        #检验filter是否生效
        # print(len(filtered_links))
        # print("!!!!!!!!!")
        # print(filtered_links)
    
        time.sleep(6)  # 等待页面跳转完成（根据实际加载速度调整）

        # -----------------------------------------------------------------------------------
        # 第二步：打印新页面的文章
        for page in range(0, len(filtered_links)):
            new_url = filtered_links[page]
            text_result = await crawler.arun(
            url=new_url,
            config=CrawlerRunConfig(
            css_selector=".article-mian-content",
            ),
            simulate_user=True,
            override_navigator=True
        )
            
            # print('第', page+1, '篇文章：')
            # print(text_result.markdown)
            # print('-----------------------------')
            md_res = text_result.markdown 
            # md_red_1 = print(md_res.raw_markdown)
            # md_red_2 = print(md_res.markdown_with_citations)
            # md_red_3 = print(md_res.references_markdown)
            with open('output.txt', 'a', encoding='utf-8') as f:
                print(f'第 {page+1} 篇文章：', file=f)
                print(md_res, file=f)
                print('-----------------------------', file=f)

asyncio.run(main())
