import asyncio
from typing import Any

from playwright.async_api import Page, TimeoutError

from harambe import SDK, Schemas


@SDK.scraper(domain="https://camisvr.co.la.ca.us", stage="listing")
async def scrape(sdk: SDK, url: str, *args: Any, **kwargs: Any) -> None:
    page: Page = sdk.page
    await page.wait_for_selector("li.PagedList-skipToLast a")
    await page.click("li.PagedList-skipToLast a")
    await page.wait_for_selector("li.active a")
    total = await page.locator("li.active a").inner_text()
    for i in range(1, 2):
        await sdk.enqueue(
            f"https://camisvr.co.la.ca.us/LACoBids/BidLookUp/OpenBidList?page={i}&TextSearch=%7C%7C%7C&FieldSort=BidTitle&DirectionSort=Asc"
        )


@SDK.scraper(
    domain="https://camisvr.co.la.ca.us",
    stage="detail",
)
async def detail_scrape(
    sdk: SDK, url: str, context: Any, *args: Any, **kwargs: Any
) -> None:
    page: Page = sdk.page
    await page.wait_for_selector("div.table-responsive")
    rows = await page.query_selector_all(
        "div.table-responsive tbody tr td:first-child a"
    )
    def xpath_by_header(head: str) -> str:
        base_xpath = "//td[strong[contains(.,'{}')]]/following-sibling::td[1]"
        return base_xpath.format(head)
    async def get_text_from_selector(
        selector: str
    ) -> str:
        try:
            await page.wait_for_selector(selector, timeout=1000)
            text = await page.locator(selector).inner_text()
            return text.strip()
        except TimeoutError:
            return None

    for i in range(len(rows)):
        await page.wait_for_selector("div.table-responsive")
        rows = await page.query_selector_all(
            "div.table-responsive tbody tr td:first-child a"
        )
        await rows[i].click()
        await page.wait_for_selector(
            "//td[strong[text()='Solicitation Number: ']]/following-sibling::td"
        )
        notice_id = await page.locator(
            "//td[strong[text()='Solicitation Number: ']]/following-sibling::td"
        ).inner_text()
        notice_title = await page.locator(
            "//td[strong[text()='Title: ']]/following-sibling::td"
        ).inner_text()
        desc = await get_text_from_selector(
            "//td[strong[text()='Description:']]/following-sibling::td"
        )
        buyer_name = await get_text_from_selector(
            "//td[strong[text()='Contact Name: ']]/following-sibling::td[1]"
        )
        buyer_email = await get_text_from_selector(
            "//td[strong[text()='Contact Email: ']]/following-sibling::td[1]"
        )
        buyer_phone = await get_text_from_selector(
            "//td[strong[text()='Contact Phone:']]/following-sibling::td[1]"
        )
        close_date = await get_text_from_selector(
            "//td[strong[text()='Close Date:']]/following-sibling::td[1]"
        )
        issue_dat = await get_text_from_selector(
            "//td[strong[text()='Open Day: ']]/following-sibling::td[1]"
        )
        typ = await get_text_from_selector(
            "//td[strong[text()='Bid Type:']]/following-sibling::td[1]"
        )
        files = []
        try:
            await page.click("#BidAttachPanel")
        except TimeoutError:
            pass
        try:
            await page.click("#BidAmendPanel", timeout=2000)
            while True:
                await page.wait_for_selector("#collapseBidAmend table tbody tr")
                rows = await page.query_selector_all(
                    "#collapseBidAmend table tbody tr "
                )
                for row in rows:
                    title = await row.query_selector("td:first-child")
                    title = await title.inner_text()
                    link = await row.query_selector("td:last-child button")
                    if link:
                        # meta=await sdk.capture_download(link)
                        files.append({"title": title.strip(), "url": ''})
                try:
                    chk = await page.locator(
                        "(//*[@id='collapseBidAmend']//a[@aria-label='Next'])[2]/.."
                    ).get_attribute("class")
                    if "disabled" in chk:
                        break
                    next = await page.query_selector(
                        "(//*[@id='collapseBidAmend']//a[@aria-label='Next'])[2]"
                    )
                    await next.click(timeout=2000)
                    await page.wait_for_timeout(1000)
                except TimeoutError:
                    break
        except TimeoutError:
            pass
        try:
            while True:
                await page.wait_for_selector(
                    "#collapseBidAttach table tbody tr", timeout=3000
                )
                rows = await page.query_selector_all(
                    "#collapseBidAttach table tbody tr"
                )
                for row in rows:
                    title = await row.query_selector("td:first-child")
                    title = await title.inner_text()
                    link = await row.query_selector("td:last-child button")
                    if link:
                        # meta=await sdk.capture_download(link)
                        files.append({"title": title.strip(), "url": ''})
                try:
                    chk = await page.locator(
                        "(//*[@id='collapseBidAttach']//a[@aria-label='Next'])[2]/.."
                    ).get_attribute("class")
                    if "disabled" in chk:
                        break
                    next = await page.query_selector(
                        "(//*[@id='collapseBidAttach']//a[@aria-label='Next'])[2]"
                    )
                    await next.click(timeout=2000)
                    await page.wait_for_timeout(1000)
                except TimeoutError:
                    break
        except TimeoutError:
            pass
        item_description = await page.locator(xpath_by_header("Commodity:")).inner_text()
        items = [
            {
                "code_type": None,
                "code": None,
                "code_description": item_description,
                "description": None,
            }
        ]
        await sdk.save_data(
            {
                "id": notice_id,
                "title": notice_title,
                "description": desc,
                "location": None,
            }
        )
        await page.go_back()


if __name__ == "__main__":
    asyncio.run(
        SDK.run(
            scrape,
            "https://camisvr.co.la.ca.us/LACoBids/BidLookUp/OpenBidList",
            Schemas.government_contracts
        )
    )
    asyncio.run(SDK.run_from_file(detail_scrape, Schemas.government_contracts, headless=False))
