import requests
from bs4 import BeautifulSoup
import openai

# Set up your OpenAI API key
openai.api_key = "sk-proj-Er1tzB4NFvFrA18O3KpeT3BlbkFJ2ahpN0I678V9YwP7sYoM"

def scrape_website(url):
    """Scrapes all visible text from the given URL."""
    print("\n⏳ Scraping website... Please wait.")
    
    # Fetch website content
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Check for HTTP request errors
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching website: {e}")
        return None

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all visible text
    for script in soup(["script", "style"]):
        script.extract()  # Remove script & style elements

    text = soup.get_text(separator="\n").strip()
    
    if not text:
        print("\n❌ No readable content found on the page.")
        return None
    
    print("\n✅ Successfully scraped the website!")
    return text

def ask_question(content):
    """Handles chatbot interaction using OpenAI API."""
    print("\n🤖 Chatbot is ready! Ask anything about the website.")
    print("🔹 Type 'exit' to stop chatting.")

    while True:
        query = input("\n📝 Your Question: ")
        if query.lower() in ["exit", "quit", "bye"]:
            print("\n👋 Goodbye! Thanks for using the scraper chatbot.")
            break

        # Use GPT to answer based on scraped content
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that answers questions based on provided webpage content."},
                {"role": "user", "content": f"Content: {content}\n\nQuestion: {query}"}
            ]
        )

        answer = response.choices[0].message.content 
        print("\n🤖 Answer:", answer)

# Main chatbot function
def web_scraper_chatbot():
    print("\n🌐 Welcome to the Web Scraper Chatbot!")
    url = input("🔗 Enter a website URL to scrape: ")

    scraped_text = scrape_website(url)
    if scraped_text:
        ask_question(scraped_text)

# Run the chatbot
web_scraper_chatbot()