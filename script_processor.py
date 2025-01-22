from PyQt6.QtCore import QTimer

class ScriptProcessor:
    def __init__(self, add_new_tab, navigate_to_custom_url):
        """
        Klasa do przetwarzania skryptów.
        add_new_tab: Funkcja do otwierania nowej karty.
        navigate_to_custom_url: Funkcja do nawigacji na konkretny URL.
        """
        self.script_data = None
        self.current_line = 0
        self.add_new_tab = add_new_tab
        self.navigate_to_custom_url = navigate_to_custom_url

    def set_script_data(self, script_data):
        """
        Ustaw dane skryptu do wykonania.
        """
        self.script_data = script_data
        self.current_line = 0

    def process_next_command(self):
        """
        Kontynuuj wykonywanie następnej komendy po czasie oczekiwania.
        """
        if self.script_data is None:
            print("Brak skryptu do wykonania!")
            return

        script = self.script_data["script"]
        lines = script.splitlines()

        if self.current_line >= len(lines):
            print("Skrypt zakończony!")
            return

        line = lines[self.current_line].strip()

        if not line:
            self.current_line += 1
            self.process_next_command()
            return

        if line.startswith("create_tab"):
            url = self.extract_argument(line)
            if url:
                self.add_new_tab(url)

        elif line.startswith("navigate_to"):
            url = self.extract_argument(line)
            if url:
                self.navigate_to_custom_url(url)

        elif line.startswith("wait"):
            time_count = self.extract_argument(line)
            if time_count:
                time_count = int(time_count)
                QTimer.singleShot(time_count * 1000, self.process_next_command)
                self.current_line += 1
                return

        self.current_line += 1
        self.process_next_command()

    def extract_argument(self, line):
        start = line.find("(")
        end = line.rfind(")")
        if start != -1 and end != -1:
            return line[start + 1:end].strip().strip('"')
        return None
    def extract_arguments(self, line):
        start = line.find('(')
        end = line.find(')')
        if start != -1 and end != -1:
            arguments = line[start + 1:end].split(',')
            return [arg.strip().strip('"').strip("'") for arg in arguments]
        return []