from typing import Dict, Any, Optional
from .base import BaseScraper
import logging
from datetime import datetime
import re

class SantanderScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.bancosantander.es"
        
    async def login(self, credentials: Dict[str, str]):
        try:
            await self.page.goto(f"{self.base_url}/particulares/banca-online/")
            
            # Esperar y rellenar el formulario de login
            await self.page.fill("#username", credentials["username"])
            await self.page.fill("#password", credentials["password"])
            
            # Click en el botón de login
            await self.page.click('button[type="submit"]')
            
            # Esperar a que cargue la página principal
            await self.page.wait_for_selector(".account-summary")
            
        except Exception as e:
            logging.error(f"Error durante el login: {str(e)}")
            raise
            
    async def get_balance(self) -> float:
        try:
            # Navegar a la página de cuentas si es necesario
            balance_text = await self.page.text_content(".account-balance")
            
            # Limpiar el texto y convertir a float
            balance = float(re.sub(r'[^\d.]', '', balance_text))
            return balance
            
        except Exception as e:
            logging.error(f"Error obteniendo el balance: {str(e)}")
            raise
            
    async def get_transactions(self, from_date: Optional[str] = None) -> list:
        transactions = []
        try:
            # Navegar a la página de movimientos
            await self.page.click(".movements-link")
            await self.page.wait_for_selector(".transaction-list")
            
            # Si hay fecha, aplicar el filtro
            if from_date:
                await self._apply_date_filter(from_date)
            
            # Extraer transacciones
            rows = await self.page.query_selector_all(".transaction-row")
            
            for row in rows:
                transaction = {
                    "date": await row.text_content(".transaction-date"),
                    "description": await row.text_content(".transaction-description"),
                    "amount": float(re.sub(r'[^\d.-]', '', 
                                 await row.text_content(".transaction-amount"))),
                    "balance": float(re.sub(r'[^\d.-]', '', 
                                  await row.text_content(".transaction-balance")))
                }
                transactions.append(transaction)
                
            return transactions
            
        except Exception as e:
            logging.error(f"Error obteniendo transacciones: {str(e)}")
            raise
            
    async def _apply_date_filter(self, from_date: str):
        # Implementar la lógica para aplicar el filtro de fecha
        pass