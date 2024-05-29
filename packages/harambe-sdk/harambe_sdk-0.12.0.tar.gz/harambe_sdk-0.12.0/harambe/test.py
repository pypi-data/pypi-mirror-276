import asyncio
import re
from typing import Any

from playwright.async_api import Page, TimeoutError

from harambe import SDK
from harambe import Schemas


async def scrape(sdk: SDK, url: str, context: Any, *args: Any, **kwargs: Any) -> None:
    page: Page = sdk.page
    await page.goto(url)
    await page.wait_for_selector("div.page-header h1")
    notice_title = await page.locator("div.page-header h1").inner_text()
    try:
        await page.wait_for_selector(
            "(//div[@class='info'])[1]/following-sibling::div[1]/input", timeout=2000
        )
        notice_id = await page.locator(
            "(//div[@class='info'])[1]/following-sibling::div[1]/input"
        ).get_attribute("value")
    except TimeoutError:
        notice_id = None
    try:
        await page.wait_for_selector("#evp_description", timeout=1000)
        desc = await page.locator("#evp_description").input_value()
        desc = desc.strip()
    except TimeoutError:
        desc = None
    p_items = []
    try:
        await page.wait_for_selector(
            '//input[@aria-label="Commodity Code is a required field."]', timeout=1000
        )
        category = await page.locator(
            '//input[@aria-label="Commodity Code is a required field."]'
        ).get_attribute("value")
        p_items.append(
            {
                "code_type": None,
                "code": None,
                "code_description": category,
                "description": None,
            }
        )
    except TimeoutError:
        p_items = []
    try:
        await page.wait_for_selector(
            "#evp_posteddate_datepicker_description", timeout=1000
        )
        open_date = await page.locator(
            "#evp_posteddate_datepicker_description"
        ).first.input_value()
    except TimeoutError:
        open_date = None
    try:
        await page.wait_for_selector("#statuscode", timeout=1000)
        status = await page.locator("#statuscode").first.inner_text()
    except TimeoutError:
        status = None
    try:
        await page.wait_for_selector("#evp_specinstr", timeout=1000)
        buyer_email = await page.locator("#evp_specinstr").first.get_attribute("value")
        email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
        # Extract phone numbers and emails
        emails = re.findall(email_pattern, buyer_email)
        if emails:
            buyer_email = emails[0]
        else:
            buyer_email = None
    except:
        buyer_email = None
    files = []
    try:
        await page.wait_for_selector("div.notes>div", timeout=2000)
        cards = await page.query_selector_all("div.notes>div")
        for card in cards:
            files_link = await card.query_selector("a")
            files_tite = await card.query_selector("div.text")
            title = await files_tite.inner_text()
            href = await files_link.get_attribute("href")
            if not title.strip():
                title = await files_link.inner_text()
            files.append({"title": title.strip(), "url": "https://evp.nc.gov" + href})
    except TimeoutError:
        files = []

    await sdk.save_data(
        {
            "id": notice_id,
            "title": notice_title,
            "description": desc,
            "location": None,
            "type": None,
            "category": category,
            "posted_date": open_date,
            "due_date": None,
            "buyer_name": None,
            "buyer_contact_name": None,
            "buyer_contact_number": None,
            "buyer_contact_email": buyer_email,
            "status": status,
            "attachments": files,
            "procurement_items": p_items,
        }
    )


if __name__ == "__main__":
    asyncio.run(
        SDK.run(
            scrape,
            "https://evp.nc.gov/solicitations/details/?id=4a9961c8-de16-ef11-9f89-001dd8053ad2",
            Schemas.government_contracts,
        )
    )
