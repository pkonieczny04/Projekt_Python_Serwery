import unittest
from exercise import ListServer, Product, Client, MapServer, TooManyProductsFoundError

# Zbiór serwerów, które będziemy testować.
server_types = (ListServer, MapServer)

class ServerTest(unittest.TestCase):
    def test_get_entries_returns_properly_sorted_entries(self):
        """Czy serwer zwraca wyniki poprawnie posortowane według ceny?"""
        products = [
            Product("P1", 10),
            Product("P3", 5),
            Product("P2", 15)
        ]
        
        # Testujemy zarówno dla ListServer, jak i MapServer
        for server_type in server_types:
            with self.subTest(server=server_type):
                server = server_type(products)
                entries = server.get_entries(1)  # Dopasowanie dla nazw zaczynających się na jedną literę
                self.assertEqual([products[1], products[0], products[2]], entries)

    def test_get_entries_raises_too_many_products_found_error(self):
        """Czy przekroczenie maksymalnej liczby znalezionych produktów powoduje rzucenie wyjątku?"""
        products = [
            Product("P1", 10),
            Product("P2", 20),
            Product("P3", 30),
            Product("P4", 40),
            Product("P5", 50),
            Product("P6", 60)
        ]
        
        # Testujemy zarówno dla ListServer, jak i MapServer
        for server_type in server_types:
            with self.subTest(server=server_type):
                server = server_type(products)
                with self.assertRaises(TooManyProductsFoundError):
                    server.get_entries(1)

class ClientTest(unittest.TestCase):
    
    def test_total_price_with_exception(self):
        """Czy funkcja obliczająca łączną cenę produktów zwraca poprawny wynik w przypadku rzucenia wyjątku?"""
        products = [
            Product("P1", 10),
            Product("P2", 20),
            Product("P3", 30),
            Product("P4", 40),
            Product("P5", 50),
            Product("P6", 60)
        ]
        
        # Testujemy zarówno dla ListServer, jak i MapServer
        for server_type in server_types:
            with self.subTest(server=server_type):
                server = server_type(products)
                client = Client(server)
                self.assertIsNone(client.get_total_price(1))

    def test_total_price_with_no_matching_products(self):
        """Czy funkcja obliczająca łączną cenę produktów zwraca None, gdy brak produktów pasujących do kryterium?"""
        products = [
            Product("Apple1", 10),
            Product("Banana2", 20)
        ]
        
        # Testujemy zarówno dla ListServer, jak i MapServer
        for server_type in server_types:
            with self.subTest(server=server_type):
                server = server_type(products)
                client = Client(server)
                self.assertIsNone(client.get_total_price(3))  # Nie ma produktów zaczynających się trzema literami

    def test_total_price_for_proper_matching_products(self):
        """Czy funkcja obliczająca łączną cenę produktów zwraca poprawną sumę?"""
        products = [
            Product("Apple123", 10),
            Product("Apple124", 20),
            Product("Banana12", 30)
        ]
        
        # Testujemy zarówno dla ListServer, jak i MapServer
        for server_type in server_types:
            with self.subTest(server=server_type):
                server = server_type(products)
                client = Client(server)
                self.assertEqual(30, client.get_total_price(5))  # Suma cen dla produktów zaczynających się od 5 liter "Apple"

if __name__ == "__main__":
    unittest.main()
