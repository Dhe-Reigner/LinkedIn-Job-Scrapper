from contextlib import suppress, asynccontextmanager
from crawlee.router import Router
from crawlee import Request
from crawlee.playwright_crawler import PlaywrightCrawlingContext
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
import re

router = Router[PlaywrightCrawlingContext]()


# @router.default_handler
# async def default_handler(context: PlaywrightCrawlingContext) -> None:
#     """Default request handler."""
#     context.log.info(f'Processing {context.request.url} ...')
#     title = await context.page.query_selector('title')
#     await context.push_data(
#         {
#             'url': context.request.loaded_url,
#             'title': await title.inner_text() if title else None,
#         }
#     )

#     await context.enqueue_links()

# router = router[PlaywrightCrawlingContext]()

@router.default_handler
async def default_handler(context : PlaywrightCrawlingContext) -> None:
    """Default request handler."""

    # select all the links for the job posting on the page
    hrefs = await context.page.locator('ul.jobs-search__results-list a').evaluate_all("links => links.map(link => link.href)")
    
    # add all the links to the job listings route
    await context.add_requests(
        [Request.from_url(rec, label='job_listing') for rec in hrefs]
    )


@router.handler('job_listing')
async def listing_handler(context : PlaywrightCrawlingContext) -> None:
    """Handler for job listings."""

    await context.page.wait_for_load_state('load')
    
    job_title = await context.page.locator('div.top-card-layout__entity-info h1.top-card-layout__title').text_content()
    
    company_name = await context.page.locator('span.topcard__flavor a').text_content()
    
    time_of_posting = await context.page.locator('div.topcard__flavor-row span.posted-time-ago__text').text_content()
    
    await context.push_data(
        {
            # we are making use of regex to remove special characters for the extracted texts
            
            'title': re.sub(r'[\s\n]+', '', job_title),
            'Company name': re.sub(r'[\s\n]+', '', company_name),
            'Time of posting': re.sub(r'[\s\n]+', '', time_of_posting),
            'url': context.request.loaded_url,
        }
    )