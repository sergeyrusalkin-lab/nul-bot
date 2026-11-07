import re

class NULPrimaryVectorIsolator:
    def __init__(self, text: str):
        self.raw_text = text
        # Очищення: залишаємо кирилицю, латиницю та цифри, переводимо у верхній регістр
        self.clean_text = re.sub(r'[^А-ЯІЇЄҐA-Z0-9]', '', text.upper())
        
        # === КИРИЛИЧНА МАТРИЦЯ (R1: Петлі, R2: Каркас, R3: Розриви-шлюзи) ===
        self.CYRILLIC_MATRIX = {
            'А': (0, 3, 2), 'Б': (1, 1, 1), 'В': (2, 2, 0), 'Г': (0, 2, 2),
            'Ґ': (0, 2, 4), 'Д': (0, 3, 4), 'Е': (0, 4, 3), 'Є': (1, 0, 3),
            'Ж': (0, 0, 6), 'З': (0, 2, 2), 'И': (0, 3, 2), 'І': (0, 0, 2),
            'Ї': (0, 0, 4), 'Й': (0, 1, 4), 'К': (0, 3, 4), 'Л': (0, 3, 2),
            'М': (0, 4, 2), 'Н': (0, 3, 4), 'О': (1, 0, 0), 'П': (0, 3, 2),
            'Р': (1, 1, 1), 'С': (1, 0, 1), 'Т': (0, 2, 3), 'У': (0, 2, 2),
            'Ф': (1, 2, 2), 'Х': (0, 4, 4), 'Ц': (0, 4, 3), 'Ч': (0, 3, 3),
            'Ш': (0, 4, 2), 'Щ': (0, 4, 3), 'Ь': (1, 1, 1), 'Ю': (1, 3, 2),
            'Я': (1, 2, 2)
        }
        
        # === ЛАТИНСЬКА МАТРИЦЯ ===
        self.LATIN_MATRIX = {
            'A': (0, 3, 2), 'B': (2, 1, 2), 'C': (1, 0, 1), 'D': (1, 1, 1),
            'E': (0, 4, 3), 'F': (0, 3, 3), 'G': (1, 1, 1), 'H': (0, 3, 4),
            'I': (0, 0, 2), 'J': (0, 1, 1), 'K': (0, 3, 4), 'L': (0, 2, 2),
            'M': (0, 4, 2), 'N': (0, 3, 2), 'O': (1, 0, 0), 'P': (1, 1, 1),
            'Q': (1, 0, 1), 'R': (1, 1, 1), 'S': (1, 0, 1), 'T': (0, 2, 2),
            'U': (0, 2, 2), 'V': (0, 2, 0), 'W': (0, 4, 0), 'X': (0, 4, 4),
            'Y': (0, 2, 1), 'Z': (0, 3, 2)
        }

        # === МАТРИЦЯ ЦИФР ===
        self.DIGITS_MATRIX = {
            '0': (1, 0, 0), '8': (2, 0, 0), '1': (0, 0, 2), '4': (0, 4, 1)
        }

    def extract_primary_vectors(self):
        """Витягує первинний вектор (R1, R2, R3) для кожного окремого символу."""
        breakdown = []

        for char in self.clean_text:
            if char in self.CYRILLIC_MATRIX:
                alphabet = "CYRILLIC"
                vector = self.CYRILLIC_MATRIX[char]
            elif char in self.LATIN_MATRIX:
                alphabet = "LATIN"
                vector = self.LATIN_MATRIX[char]
            elif char in self.DIGITS_MATRIX:
                alphabet = "DIGIT"
                vector = self.DIGITS_MATRIX[char]
            else:
                alphabet = "UNKNOWN"
                vector = (0, 0, 1)

            breakdown.append({
                "char": char,
                "alphabet": alphabet,
                "vector_R1_R2_R3": vector
            })

        return {
            "source_text": self.clean_text,
            "character_vectors": breakdown
        }

# --- Тест первинного виділення ---
if __name__ == "__main__":
    isolator = NULPrimaryVectorIsolator("АБСОЛЮТ")
    result = isolator.extract_primary_vectors()
    
    print(f"Очищений текст: {result['source_text']}")
    print("Первинні вектори символів:")
    for item in result['character_vectors']:
        print(f"  [{item['alphabet']}] Символ '{item['char']}' -> Вектор (R1, R2, R3): {item['vector_R1_R2_R3']}")
