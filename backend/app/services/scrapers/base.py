from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Browser, Page
import logging

class BaseScraper(ABC):
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
    async def init_browser(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        
    async def close(self):
        if self.browser:
            await self.browser.close()
            
    @abstractmethod
    async def login(self, credentials: Dict[str, str]):
        pass
        
    @abstractmethod
    async def get_balance(self) -> float:
        pass
        
    @abstractmethod
    async def get_transactions(self, from_date: Optional[str] = None) -> list:
        pass