#使用python
# /Users/tulixuan/.local/pipx/venvs/crawl4ai/bin/python

import asyncio, time
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def multi_page_commits():
    # Fix the JavaScript code - using template literals for cleaner code
    run_config = CrawlerRunConfig(
        js_code = [
            """
            (async () => {
                // Login form handling
                const mobileInput = document.getElementById('MainContent_txtMobile');
                if (mobileInput) {
                    mobileInput.value = '17702706599';
                }

                const passwordInput = document.getElementById('MainContent_txtPassword');
                if (passwordInput) {
                    passwordInput.value = 'tlx19980413';
                }

                // Wait for values to be set
                await new Promise(resolve => setTimeout(resolve, 1000));

                // Click login button
                const loginButton = document.querySelector('#MainContent_btnLogin');
                if (loginButton) {
                    loginButton.click();
                }

                // Wait for navigation
                return await new Promise(resolve => setTimeout(() => resolve(true), 5000));
            })();
            """
        ],
        session_id= 42,
        js_only=False
    )

    # Login step
    async with AsyncWebCrawler(verbose=True, headless=True) as crawler:  # Set headless=False to debug


        # Crawling pages
        base_url = "https://passports.gasgoo.com/FastLogin?ReturnUrl=https%3a%2f%2fi.gasgoo.com%2fsupplier%2fSearch.aspx%3fcid%3d1039%26con%3d45%26page%3d{}"
        start_page = 1
        end_page = 10
        
        for page in range(start_page, end_page + 1):
            login_result = await crawler.arun(
            url=base_url.format(page),
            config=run_config,
            simulate_user=True,
            override_navigator=True
            )
            time.sleep(4) # Wait for the login process to complete
            if login_result.success:
            # print(login_result.markdown)
                print("Login attempt completed successfully.")
            else:
                print("Login attempt failed.")
            # return
            # for page in range(start_page, end_page + 1):
                
            config = CrawlerRunConfig(
                css_selector=".bodyCondLeft",
                wait_for="css:.bodyCondLeft",
                    session_id= 42,
                    js_only=True,
                )
            new_url = base_url.format(page)

            # async with AsyncWebCrawler(verbose=True, headless=True) as crawler:
            result = await crawler.arun(
                url=new_url,
                config=config,
                bypass_cache=True,
                simulate_user=True,
                override_navigator=True
            )
            # print(result)
            if result.success:
                print(f"Page {page} crawled successfully. Printing markdown results...")
                print(result.markdown)
                print("finished crawling")
            else:
                print(f"Failed to crawl page {page}. Error: {result.error}")
                continue         
   
async def main():
    await multi_page_commits()

if __name__ == "__main__":
    asyncio.run(main())