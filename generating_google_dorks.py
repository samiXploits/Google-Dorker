import os
import sqlite3
import logging
from colorama import Fore, init
import google.generativeai as genai
import time
from prettytable import PrettyTable
import requests
from bs4 import BeautifulSoup
import shodan
import json
import csv
from pyfiglet import Figlet

# Initialize colorama
init(autoreset=True)

# Define folder paths
DB_FOLDER = "db"
LOGS_FOLDER = "logs"
DATABASE_NAME = os.path.join(DB_FOLDER, "google_dorks.db")
LOG_FILE = os.path.join(LOGS_FOLDER, "google_dorks.log")

# Configure Gemini API
GEMINI_API_KEY = ""  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# Configure Shodan API
SHODAN_API_KEY = "YOUR_SHODAN_API_KEY"  # Replace with your actual Shodan API key
shodan_client = shodan.Shodan(SHODAN_API_KEY)

def setup_logging():
    """Set up logging configuration."""
    try:
        # Create the 'logs' folder if it doesn't exist
        if not os.path.exists(LOGS_FOLDER):
            os.makedirs(LOGS_FOLDER)
            print(Fore.GREEN + f"Created folder: {LOGS_FOLDER}")

        # Configure logging
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        print(Fore.GREEN + f"Logging initialized successfully at: {LOG_FILE}")
    except Exception as e:
        print(Fore.RED + f"Error setting up logging: {e}")

def initialize_database():
    """Initialize the SQLite database and create the table if it doesn't exist."""
    try:
        # Create the 'db' folder if it doesn't exist
        if not os.path.exists(DB_FOLDER):
            os.makedirs(DB_FOLDER)
            print(Fore.GREEN + f"Created folder: {DB_FOLDER}")

        # Connect to the database (it will be created if it doesn't exist)
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Create the 'dorks' table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dorks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                dork TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print(Fore.GREEN + f"Database initialized successfully at: {DATABASE_NAME}")
        logging.info(f"Database initialized successfully at: {DATABASE_NAME}")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        print(Fore.RED + f"Error initializing database: {e}")

def save_dork_to_database(category, dork):
    """Save a generated dork to the database."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dorks (category, dork) VALUES (?, ?)", (category, dork))
        conn.commit()
        conn.close()
        logging.info(f"Dork saved to database: {dork}")
    except Exception as e:
        logging.error(f"Error saving dork to database: {e}")
        print(Fore.RED + f"Error saving dork to database: {e}")

def get_dorks_from_database():
    """Retrieve all dorks from the database."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT category, dork FROM dorks")
        dorks = cursor.fetchall()
        conn.close()
        logging.info("Dorks retrieved from database.")
        return dorks
    except Exception as e:
        logging.error(f"Error retrieving dorks from database: {e}")
        print(Fore.RED + f"Error retrieving dorks from database: {e}")
        return []

def display_banner():
    """Display a god-level banner."""
    custom_fig = Figlet(font='slant')  # You can change the font (e.g., 'block', 'banner', 'doom')
    banner_text = custom_fig.renderText('Google Dorks')
    print(Fore.CYAN + "=" * 80)
    print(Fore.GREEN + banner_text)
    print(Fore.CYAN + "=" * 80)
    print(Fore.YELLOW + "Welcome to the Ultimate Google Dorks Generator".center(80))
    print(Fore.CYAN + "=" * 80)
    print(Fore.MAGENTA + "Coded with ❤️ by Your Name".center(80))
    print(Fore.CYAN + "=" * 80)

class GeneratingGoogleDorks:
    def __init__(self):
        display_banner()  # Display the banner
        self.user_choices_list = []
        self.generated_dorks = {}  # To store generated dorks
        self.user_interest_list = [
            "Finding Sensitive Information for Files",
            "Finding Login Portals and Admin Panels", 
            "Finding Geo-Location Information",
            "Finding Related Websites", 
            "Finding Specific Files",
            "Finding Specific Directories",
            "Finding Specific Files with Specific Keywords",
            "Finding Subdomains",
            "Finding Vulnerabilities",
            "Finding Emails",
            "Finding WordPress Vulnerabilities",
            "Finding Cloud Storage Files",
            "Finding Open Cameras and Webcams",
            "Finding FTP Servers",
            "Finding Index of Public Files",
            "Exit"
        ]
        self.saved_api_keys = {}  # To store user API keys
        self.user_profile = {}  # To store user preferences

    def show_menu(self):
        print(Fore.BLUE + "\nMain Menu:")
        print(Fore.YELLOW + "1. Generate Google Dorks")
        print(Fore.YELLOW + "2. View Generated Dorks")
        print(Fore.YELLOW + "3. Save Generated Dorks to File")
        print(Fore.YELLOW + "4. Clear Selections")
        print(Fore.YELLOW + "5. Advanced Filtering")
        print(Fore.YELLOW + "6. Custom Dork Generation")
        print(Fore.YELLOW + "7. Automated Search")
        print(Fore.YELLOW + "8. Shodan Integration")
        print(Fore.YELLOW + "9. User Authentication")
        print(Fore.YELLOW + "10. Enhanced Output Options")
        print(Fore.YELLOW + "11. Interactive Tutorials")
        print(Fore.YELLOW + "12. View Database Dorks")
        print(Fore.YELLOW + "13. Exit")

    def asking_user_for_his_interest(self):
        print(Fore.BLUE + "\nPlease Select your choice (you can select multiple like 1, 3, 5): ")
        table = PrettyTable()
        table.field_names = ["Index", "Choice"]
        for index, interest in enumerate(self.user_interest_list, start=1):
            table.add_row([index, interest])
        print(Fore.YELLOW + str(table))

    def user_choice(self):
        while True:
            user_choices = input(Fore.CYAN + "Enter the Choice (you can choose multiple like 1, 3, 5): ").split(',')
            valid_choices = [str(i) for i in range(1, len(self.user_interest_list) + 1)]
            invalid_choices = [choice.strip() for choice in user_choices if choice.strip() not in valid_choices]

            if invalid_choices:
                print(Fore.RED + f"Invalid Choices: {', '.join(invalid_choices)}")
                continue
            else:
                for choice in user_choices:
                    choice = choice.strip()
                    if choice == "16":
                        print(Fore.RED + "Exiting the Program..........")
                        print(Fore.GREEN + "Thank You for using the Google Dorks Generator")
                        return

                    selected_choice = self.user_interest_list[int(choice) - 1]
                    if selected_choice in self.user_choices_list:
                        print(Fore.RED + f"You have already selected {selected_choice}")
                    else:
                        print(Fore.GREEN + f"You selected {selected_choice}")
                        self.user_choices_list.append(selected_choice)

    def generate_google_dorks(self):
        if not self.user_choices_list:
            print(Fore.RED + "No choices selected. Please select at least one choice.")
            return

        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        print(Fore.GREEN + "\nGenerating Google Dorks using Gemini API...")

        for choice in self.user_choices_list:
            try:
                prompt = f"Generate exactly 5 best Google dorks for: {choice}. Only return the dorks, nothing else."
                response = model.generate_content(prompt)
                generated_text = response.text.strip()
                dorks = generated_text.split("\n")
                self.generated_dorks[choice] = dorks
                
                # Save each dork to the database
                for dork in dorks:
                    save_dork_to_database(choice, dork)
                
                table = PrettyTable()
                table.field_names = [Fore.YELLOW + "Choice", Fore.CYAN + "Generated Google Dorks"]
                table.align = "l"
                for i, dork in enumerate(dorks, start=1):
                    table.add_row([f"{Fore.YELLOW}{i}", f"{Fore.CYAN}{dork}"])
                print(Fore.YELLOW + f"\nGenerated Dorks for '{choice}':")
                print(table)
                
            except Exception as e:
                logging.error(f"Error generating dorks for '{choice}': {e}")
                print(Fore.RED + f"Error generating dorks for '{choice}': {e}")

            time.sleep(2)

    def view_generated_dorks(self):
        if not self.generated_dorks:
            print(Fore.RED + "No dorks have been generated yet.")
            return

        print(Fore.GREEN + "\nViewing Generated Dorks:")
        for choice, dorks in self.generated_dorks.items():
            table = PrettyTable()
            table.field_names = [Fore.YELLOW + "Choice", Fore.CYAN + "Generated Google Dorks"]
            table.align = "l"
            for i, dork in enumerate(dorks, start=1):
                table.add_row([f"{Fore.YELLOW}{i}", f"{Fore.CYAN}{dork}"])
            print(Fore.YELLOW + f"\nGenerated Dorks for '{choice}':")
            print(table)

    def save_dorks_to_file(self):
        if not self.generated_dorks:
            print(Fore.RED + "No dorks have been generated yet.")
            return

        filename = input(Fore.CYAN + "Enter the filename to save the dorks (e.g., dorks.txt): ")
        try:
            with open(filename, "w") as file:
                for choice, dorks in self.generated_dorks.items():
                    file.write(f"Generated Dorks for '{choice}':\n")
                    for dork in dorks:
                        file.write(f"{dork}\n")
                    file.write("\n")
            print(Fore.GREEN + f"Dorks saved to '{filename}' successfully.")
            logging.info(f"Dorks saved to file: {filename}")
        except Exception as e:
            logging.error(f"Error saving dorks to file: {e}")
            print(Fore.RED + f"Error saving dorks to file: {e}")

    def clear_selections(self):
        self.user_choices_list.clear()
        self.generated_dorks.clear()
        print(Fore.GREEN + "Selections and generated dorks cleared.")
        logging.info("Selections and generated dorks cleared.")

    def advanced_filtering(self):
        print(Fore.BLUE + "\nAdvanced Filtering Options:")
        print(Fore.YELLOW + "1. Domain Filtering")
        print(Fore.YELLOW + "2. File Type Filtering")
        print(Fore.YELLOW + "3. Date Range Filtering")
        choice = input(Fore.CYAN + "Enter your choice (1-3): ").strip()

        if choice == "1":
            domain = input(Fore.CYAN + "Enter the domain (e.g., example.com): ").strip()
            if domain:
                self.user_choices_list.append(f"Domain: {domain}")
                print(Fore.GREEN + f"Domain '{domain}' added to filters.")
                logging.info(f"Domain filter added: {domain}")
        elif choice == "2":
            file_type = input(Fore.CYAN + "Enter the file type (e.g., pdf, doc): ").strip()
            if file_type:
                self.user_choices_list.append(f"File Type: {file_type}")
                print(Fore.GREEN + f"File type '{file_type}' added to filters.")
                logging.info(f"File type filter added: {file_type}")
        elif choice == "3":
            date_range = input(Fore.CYAN + "Enter the date range (e.g., 2023-01-01..2023-12-31): ").strip()
            if date_range:
                self.user_choices_list.append(f"Date Range: {date_range}")
                print(Fore.GREEN + f"Date range '{date_range}' added to filters.")
                logging.info(f"Date range filter added: {date_range}")
        else:
            print(Fore.RED + "Invalid choice.")
            logging.warning("Invalid choice in advanced filtering.")

    def custom_dork_generation(self):
        print(Fore.BLUE + "\nCustom Dork Generation:")
        custom_keywords = input(Fore.CYAN + "Enter custom keywords (comma-separated): ").strip()
        custom_operators = input(Fore.CYAN + "Enter custom operators (comma-separated, e.g., site:, intitle:): ").strip()

        if not custom_keywords or not custom_operators:
            print(Fore.RED + "Keywords and operators are required.")
            logging.warning("Custom dork generation failed: Missing keywords or operators.")
            return

        keywords = [keyword.strip() for keyword in custom_keywords.split(",")]
        operators = [operator.strip() for operator in custom_operators.split(",")]

        custom_dorks = []
        for operator in operators:
            for keyword in keywords:
                custom_dorks.append(f"{operator}{keyword}")

        self.generated_dorks["Custom Dorks"] = custom_dorks

        # Save custom dorks to the database
        for dork in custom_dorks:
            save_dork_to_database("Custom Dorks", dork)

        table = PrettyTable()
        table.field_names = [Fore.YELLOW + "Index", Fore.CYAN + "Custom Google Dorks"]
        table.align = "l"
        for i, dork in enumerate(custom_dorks, start=1):
            table.add_row([f"{Fore.YELLOW}{i}", f"{Fore.CYAN}{dork}"])
        print(Fore.YELLOW + "\nGenerated Custom Dorks:")
        print(table)
        logging.info("Custom dorks generated and saved to database.")

    def automated_search(self):
        if not self.generated_dorks:
            print(Fore.RED + "No dorks have been generated yet.")
            return

        for choice, dorks in self.generated_dorks.items():
            print(Fore.GREEN + f"\nSearching for '{choice}':")
            for dork in dorks:
                print(Fore.YELLOW + f"Searching for: {dork}")
                try:
                    response = requests.get(f"https://www.google.com/search?q={dork}")
                    soup = BeautifulSoup(response.text, 'html.parser')
                    results = soup.find_all('h3')
                    for result in results:
                        print(Fore.CYAN + result.get_text())
                    logging.info(f"Automated search completed for dork: {dork}")
                except Exception as e:
                    logging.error(f"Error searching for '{dork}': {e}")
                    print(Fore.RED + f"Error searching for '{dork}': {e}")
                time.sleep(2)  # To avoid being blocked by Google

    def shodan_integration(self):
        print(Fore.BLUE + "\nShodan Integration:")
        query = input(Fore.CYAN + "Enter your Shodan query (e.g., 'apache'): ").strip()
        if not query:
            print(Fore.RED + "Query cannot be empty.")
            logging.warning("Shodan query cannot be empty.")
            return

        try:
            results = shodan_client.search(query)
            print(Fore.GREEN + f"Total results found: {results['total']}")
            for result in results['matches']:
                print(Fore.YELLOW + f"IP: {result['ip_str']}")
                print(Fore.CYAN + f"Data: {result['data']}\n")
            logging.info(f"Shodan search completed for query: {query}")
        except shodan.APIError as e:
            logging.error(f"Shodan API Error: {e}")
            print(Fore.RED + f"Shodan API Error: {e}")

    def user_authentication(self):
        print(Fore.BLUE + "\nUser Authentication:")
        print(Fore.YELLOW + "1. Save API Key")
        print(Fore.YELLOW + "2. View Saved API Keys")
        choice = input(Fore.CYAN + "Enter your choice (1-2): ").strip()

        if choice == "1":
            service = input(Fore.CYAN + "Enter the service name (e.g., Gemini, Shodan): ").strip()
            api_key = input(Fore.CYAN + "Enter the API key: ").strip()
            if service and api_key:
                self.saved_api_keys[service] = api_key
                print(Fore.GREEN + f"API key for '{service}' saved successfully.")
                logging.info(f"API key saved for service: {service}")
        elif choice == "2":
            if not self.saved_api_keys:
                print(Fore.RED + "No API keys saved yet.")
                logging.warning("No API keys saved yet.")
            else:
                print(Fore.GREEN + "\nSaved API Keys:")
                for service, key in self.saved_api_keys.items():
                    print(Fore.YELLOW + f"{service}: {key}")
                logging.info("Saved API keys viewed.")
        else:
            print(Fore.RED + "Invalid choice.")
            logging.warning("Invalid choice in user authentication.")

    def enhanced_output_options(self):
        print(Fore.BLUE + "\nEnhanced Output Options:")
        print(Fore.YELLOW + "1. Export to CSV")
        print(Fore.YELLOW + "2. Export to JSON")
        choice = input(Fore.CYAN + "Enter your choice (1-2): ").strip()

        if choice == "1":
            filename = input(Fore.CYAN + "Enter the filename (e.g., dorks.csv): ").strip()
            if not filename:
                print(Fore.RED + "Filename cannot be empty.")
                logging.warning("Filename cannot be empty.")
                return

            try:
                with open(filename, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Choice", "Generated Google Dorks"])
                    for choice, dorks in self.generated_dorks.items():
                        for dork in dorks:
                            writer.writerow([choice, dork])
                print(Fore.GREEN + f"Dorks exported to '{filename}' successfully.")
                logging.info(f"Dorks exported to CSV: {filename}")
            except Exception as e:
                logging.error(f"Error exporting to CSV: {e}")
                print(Fore.RED + f"Error exporting to CSV: {e}")
        elif choice == "2":
            filename = input(Fore.CYAN + "Enter the filename (e.g., dorks.json): ").strip()
            if not filename:
                print(Fore.RED + "Filename cannot be empty.")
                logging.warning("Filename cannot be empty.")
                return

            try:
                with open(filename, "w") as file:
                    json.dump(self.generated_dorks, file, indent=4)
                print(Fore.GREEN + f"Dorks exported to '{filename}' successfully.")
                logging.info(f"Dorks exported to JSON: {filename}")
            except Exception as e:
                logging.error(f"Error exporting to JSON: {e}")
                print(Fore.RED + f"Error exporting to JSON: {e}")
        else:
            print(Fore.RED + "Invalid choice.")
            logging.warning("Invalid choice in enhanced output options.")

    def interactive_tutorials(self):
        print(Fore.BLUE + "\nInteractive Tutorials:")
        print(Fore.YELLOW + "1. What are Google Dorks?")
        print(Fore.YELLOW + "2. How to Use Google Dorks Effectively")
        print(Fore.YELLOW + "3. Examples of Common Google Dorks")
        choice = input(Fore.CYAN + "Enter your choice (1-3): ").strip()

        if choice == "1":
            print(Fore.GREEN + "\nGoogle Dorks are advanced search operators used to find specific information on the web.")
            logging.info("User viewed tutorial: What are Google Dorks?")
        elif choice == "2":
            print(Fore.GREEN + "\nTo use Google Dorks effectively, combine operators like 'site:', 'intitle:', and 'filetype:' with specific keywords.")
            logging.info("User viewed tutorial: How to Use Google Dorks Effectively")
        elif choice == "3":
            print(Fore.GREEN + "\nExamples of common Google Dorks:")
            print(Fore.YELLOW + "1. site:example.com filetype:pdf")
            print(Fore.YELLOW + "2. intitle:'index of'")
            print(Fore.YELLOW + "3. inurl:'admin'")
            logging.info("User viewed tutorial: Examples of Common Google Dorks")
        else:
            print(Fore.RED + "Invalid choice.")
            logging.warning("Invalid choice in interactive tutorials.")

    def view_database_dorks(self):
        """View all dorks stored in the database."""
        dorks = get_dorks_from_database()
        if not dorks:
            print(Fore.RED + "No dorks found in the database.")
            logging.warning("No dorks found in the database.")
            return

        table = PrettyTable()
        table.field_names = [Fore.YELLOW + "Category", Fore.CYAN + "Dork"]
        table.align = "l"
        for category, dork in dorks:
            table.add_row([f"{Fore.YELLOW}{category}", f"{Fore.CYAN}{dork}"])
        print(Fore.YELLOW + "\nDorks in Database:")
        print(table)
        logging.info("User viewed dorks from the database.")

# Main execution
if __name__ == "__main__":
    setup_logging()  # Set up logging
    initialize_database()  # Initialize the database
    new = GeneratingGoogleDorks()
    while True:
        new.show_menu()
        choice = input(Fore.CYAN + "Enter your choice (1-13): ").strip()

        if choice == "1":
            new.asking_user_for_his_interest()
            new.user_choice()
            new.generate_google_dorks()
        elif choice == "2":
            new.view_generated_dorks()
        elif choice == "3":
            new.save_dorks_to_file()
        elif choice == "4":
            new.clear_selections()
        elif choice == "5":
            new.advanced_filtering()
        elif choice == "6":
            new.custom_dork_generation()
        elif choice == "7":
            new.automated_search()
        elif choice == "8":
            new.shodan_integration()
        elif choice == "9":
            new.user_authentication()
        elif choice == "10":
            new.enhanced_output_options()
        elif choice == "11":
            new.interactive_tutorials()
        elif choice == "12":
            new.view_database_dorks()
        elif choice == "13":
            print(Fore.RED + "Exiting the Program..........")
            print(Fore.GREEN + "Thank You for using the Google Dorks Generator")
            logging.info("Program exited by user.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")
            logging.warning("Invalid choice selected by user.")