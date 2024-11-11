import unittest
from collections import Counter
from exercise import ListServer, Product, Client, MapServer, TooManyProductsFoundError

class ServerTest(unittest.TestCase):
    def test_get_entries_returns_properly_sorted_entries(self):
        """Czy wyniki zwrócone przez serwer przechowujący dane w liście są poprawnie posortowane?"""
        # Tworzymy listę produktów z różnymi cenami
        products = [
            Product("P1", 10),
            Product("P3", 5),
            Product("P2", 15)
        ]
        # Inicjalizujemy serwer z listą produktów
        server = ListServer(products)
        # Pobieramy produkty zaczynające się od jednej litery
        entries = server.get_entries(1)
        # Sprawdzamy, czy produkty są zwrócone w kolejności rosnącej według ceny
        self.assertEqual([products[1], products[0], products[2]], entries)

    def test_get_entries_raises_too_many_products_found_error(self):
        """Czy przekroczenie maksymalnej liczby znalezionych produktów powoduje rzucenie wyjątku?"""
        # Tworzymy listę produktów, gdzie liczba pasujących produktów przekroczy maksymalny limit (5)
        products = [
            Product("P1", 10),
            Product("P2", 20),
            Product("P3", 30),
            Product("P4", 40),
            Product("P5", 50),
            Product("P6", 60)
        ]
        # Inicjalizujemy serwer z listą produktów
        server = ListServer(products)
        # Sprawdzamy, czy zostanie rzucony wyjątek TooManyProductsFoundError przy przekroczeniu limitu wyników
        with self.assertRaises(TooManyProductsFoundError):
            server.get_entries(1)

class ClientTest(unittest.TestCase):
    def test_total_price_with_exception(self):
        """Czy funkcja obliczająca łączną cenę produktów zwraca poprawny wynik w przypadku rzucenia wyjątku?"""
        # Tworzymy listę produktów, gdzie liczba wyników przekroczy limit i wywoła wyjątek
        products = [
            Product("P1", 10),
            Product("P2", 20),
            Product("P3", 30),
            Product("P4", 40),
            Product("P5", 50),
            Product("P6", 60)
        ]
        # Inicjalizujemy serwer i klienta
        server = ListServer(products)
        client = Client(server)
        # Sprawdzamy, czy metoda get_total_price zwraca None, gdy wywołany jest wyjątek
        self.assertIsNone(client.get_total_price(1))

    def test_total_price_with_no_matching_products(self):
        """Czy funkcja obliczająca łączną cenę produktów zwraca None, gdy brak produktów pasujących do kryterium?"""
        # Tworzymy listę produktów, które nie pasują do wzorca wyszukiwania (zaczynają się na mniej niż 3 litery)
        products = [
            Product("Apple1", 10),
            Product("Banana2", 20)
        ]
        # Inicjalizujemy serwer i klienta
        server = ListServer(products)
        client = Client(server)
        # Sprawdzamy, czy metoda get_total_price zwraca None, gdy brak produktów spełniających kryterium
        self.assertIsNone(client.get_total_price(3))

    def test_total_price_for_proper_matching_products(self):
        """Czy funkcja obliczająca łączną cenę produktów zwraca poprawną sumę?"""
        # Tworzymy listę produktów, z których część spełnia kryterium (zaczyna się od "Apple" i ma co najmniej 5 liter)
        products = [
            Product("Apple123", 10),
            Product("Apple124", 20),
            Product("Banana12", 30)
        ]
        # Inicjalizujemy serwer i klienta
        server = ListServer(products)
        client = Client(server)
        # Sprawdzamy, czy metoda get_total_price zwraca poprawną sumę cen produktów, które spełniają kryterium
        self.assertEqual(30, client.get_total_price(5))

# Uruchomienie testów, jeśli skrypt jest wywoływany bezpośrednio
if __name__ == "__main__":
    unittest.main()
