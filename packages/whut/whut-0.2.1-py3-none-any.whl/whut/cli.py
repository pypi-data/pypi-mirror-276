import argparse
import google.generativeai as genai

def search(query, prompt_template):
    api_key = 'AIzaSyDzjP-c_fUAjiKybq81Rd-leQSejOaqO7I'
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt = prompt_template.format(query=query)
    response = model.generate_content(prompt)
    return response.text

def main():
    parser = argparse.ArgumentParser(description='Search the internet from the terminal using Google Generative AI')
    parser.add_argument('query', nargs='+', help='Search query')
    parser.add_argument('-C', '--custom', default="Give decluttered answer possible. What's: {query}",
                        help='Custom prompt template for the search')
    args = parser.parse_args()
    query = ' '.join(args.query)
    result = search(query, args.custom)
    print(result)

if __name__ == '__main__':
    main()
