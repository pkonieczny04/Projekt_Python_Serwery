import re
from typing import List, Optional
from abc import ABC, abstractmethod

# Klasa Product reprezentuje produkt z nazwą i ceną
class Product:
    def __init__(self, name: str, price: float):
        # Walidacja nazwy - musi składać się z liter, a następnie cyfr
        if not re.fullmatch(r'^[a-zA-Z]+\d+$', name):
            raise ValueError("Nazwa produktu musi składać się z liter, a następnie cyfr.")
        # Walidacja ceny - cena musi być dodatnia
        if price <= 0:
            raise ValueError("Cena produktu musi być dodatnia.")
        self.name = name  # Nazwa produktu
        self.price = price  # Cena produktu
        
    def __eq__(self, other):
        # Sprawdza, czy dwa produkty są równe (porównanie nazwy i ceny)
        return isinstance(other, Product) and self.name == other.name and self.price == other.price
 
    def __hash__(self):
        # Zwraca wartość hash dla obiektu Product (potrzebne do przechowywania w zbiorach i słownikach)
        return hash((self.name, self.price))

# Klasa wyjątku rzucanego, gdy liczba wyników przekracza dopuszczalny limit
class TooManyProductsFoundError(Exception):
    pass

# Klasa abstrakcyjna Server reprezentująca serwer przechowujący produkty
class Server(ABC):
    # Maksymalna liczba wyników, które mogą być zwrócone
    n_max_returned_entries = 5

    def get_entries(self, n_letters: int) -> List[Product]:
        """
        Zwraca listę produktów, których nazwa zaczyna się od określonej liczby liter,
        a potem kończy cyframi. Filtruje i sortuje produkty, a jeśli liczba wyników
        przekroczy `n_max_returned_entries`, rzuca wyjątek TooManyProductsFoundError.
        """
        all_products = self._get_all_products()  # Pobranie wszystkich produktów
        # Tworzenie wzorca na podstawie liczby początkowych liter
        pattern = rf'^[a-zA-Z]{{{n_letters}}}\d+$'
        # Filtracja produktów według wzorca
        filtered_products = [product for product in all_products if re.fullmatch(pattern, product.name)]
        
        # Jeśli liczba wyników przekroczy dozwolony limit, rzuca wyjątek
        if len(filtered_products) > self.n_max_returned_entries:
            raise TooManyProductsFoundError("Znaleziono zbyt wiele produktów spełniających kryteria.")
        
        # Sortowanie wyników po cenie rosnąco
        return sorted(filtered_products, key=lambda p: p.price)
    
    @abstractmethod
    def _get_all_products(self) -> List[Product]:
        """
        Metoda abstrakcyjna zwracająca wszystkie produkty.
        Musi być zaimplementowana w klasach pochodnych.
        """
        pass

# Klasa ListServer, która implementuje Server i przechowuje produkty w liście
class ListServer(Server):
    def __init__(self, products: List[Product]):
        # Inicjalizacja serwera z listą produktów
        self.products = products

    def _get_all_products(self) -> List[Product]:
        # Zwraca wszystkie produkty przechowywane w liście
        return self.products

# Klasa MapServer, która implementuje Server i przechowuje produkty w słowniku
class MapServer(Server):
    def __init__(self, products: List[Product]):
        # Inicjalizacja serwera ze słownikiem produktów, gdzie kluczem jest nazwa produktu
        self.products = {product.name: product for product in products}

    def _get_all_products(self) -> List[Product]:
        # Zwraca wszystkie produkty jako listę wartości słownika
        return list(self.products.values())

# Klasa Client, która korzysta z serwera do wyszukiwania produktów i obliczania cen
class Client:
    def __init__(self, server: Server):
        # Inicjalizacja klienta z referencją do serwera
        self.server = server
        
    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        """
        Oblicza całkowitą cenę produktów, które spełniają kryterium liczby liter `n_letters`.
        Jeśli liczba wyników przekroczy dozwolony limit, zwraca None.
        """
        if n_letters is None:
            return None
        try:
            # Pobiera produkty spełniające kryterium liczby początkowych liter
            products = self.server.get_entries(n_letters)
            
            # Sprawdzenie, czy lista jest pusta; jeśli tak, zwracamy None
            if not products:
                return None
            
            # Oblicza sumę cen produktów
            total_price = sum(product.price for product in products)
            return total_price
        except TooManyProductsFoundError:
            # Obsługa wyjątku, gdy liczba wyników przekroczy limit
            return None
