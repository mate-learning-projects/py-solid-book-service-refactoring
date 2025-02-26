import json
import xml.etree.ElementTree as Et
from abc import ABC, abstractmethod


# Interface for serialization
class Serializer(ABC):
    @abstractmethod
    def serialize(self, title: str, content: str) -> str:
        pass


# Implementation of JSON serialization
class JsonSerializer(Serializer):
    def serialize(self, title: str, content: str) -> str:
        return json.dumps({"title": title, "content": content})


# Implementation of XML serialization
class XmlSerializer(Serializer):
    def serialize(self, title: str, content: str) -> str:
        root = Et.Element("book")
        title_elem = Et.SubElement(root, "title")
        title_elem.text = title
        content_elem = Et.SubElement(root, "content")
        content_elem.text = content
        return Et.tostring(root, encoding="unicode")


# Factory for creating Serializer
class SerializerFactory:
    _serializers = {
        "json": JsonSerializer,
        "xml": XmlSerializer,
    }

    @staticmethod
    def create_serializer(serialize_type: str) -> Serializer:
        serializer_class = SerializerFactory._serializers.get(serialize_type)
        if serializer_class is None:
            raise ValueError(f"Unknown serialize type: {serialize_type}")
        return serializer_class()


# Interface for output
class Printer(ABC):
    @abstractmethod
    def print(self, title: str, content: str) -> None:
        pass


# Simple console output (for display)
class ConsolePrinter(Printer):
    def print(self, title: str, content: str) -> None:
        print(content)


# Reverse console output (for display)
class ReverseConsolePrinter(Printer):
    def print(self, title: str, content: str) -> None:
        print(content[::-1])


# Console output with title (for print)
class PrintConsolePrinter(Printer):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book: {title}...")
        print(content)


# Reverse console output with title (for print)
class PrintReverseConsolePrinter(Printer):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book in reverse: {title}...")
        print(content[::-1])


# Factory for creating Printer
class PrinterFactory:
    _display_printers = {
        "console": ConsolePrinter,
        "reverse": ReverseConsolePrinter,
    }
    _print_printers = {
        "console": PrintConsolePrinter,
        "reverse": PrintReverseConsolePrinter,
    }

    @staticmethod
    def create_display_printer(method_type: str) -> Printer:
        printer_class = PrinterFactory._display_printers.get(method_type)
        if printer_class is None:
            raise ValueError(f"Unknown display type: {method_type}")
        return printer_class()

    @staticmethod
    def create_print_printer(method_type: str) -> Printer:
        printer_class = PrinterFactory._print_printers.get(method_type)
        if printer_class is None:
            raise ValueError(f"Unknown print type: {method_type}")
        return printer_class()


# Class Book — only data
class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content


# Function main with factories
def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    printer_factory = PrinterFactory()
    serializer_factory = SerializerFactory()
    for cmd, method_type in commands:
        if cmd == "display":
            printer = printer_factory.create_display_printer(method_type)
            printer.print(book.title, book.content)
        elif cmd == "print":
            printer = printer_factory.create_print_printer(method_type)
            printer.print(book.title, book.content)
        elif cmd == "serialize":
            serializer = serializer_factory.create_serializer(method_type)
            return serializer.serialize(book.title, book.content)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(
        main(
            sample_book,
            [
                ("display", "reverse"),
                ("print", "console"),
                ("serialize", "xml"),
            ],
        )
    )
