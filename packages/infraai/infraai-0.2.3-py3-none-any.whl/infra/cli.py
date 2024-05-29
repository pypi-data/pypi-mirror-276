import argparse
import sys
from infra.config import get_config, set_key, set_model, ask_ai



def cli():
    parser = argparse.ArgumentParser(description='Infra: AI helper that makes it easy for infrastructure developers to find commands quickly and effectively.',
                                     epilog=
                'Examples:\n'
                '  infra setup nginx webserver\n'
                '  infra how to initialize git repository\n'
                '  infra create python virtual environment',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('prompt', nargs='*', help='Ask clear specific questions about commands or any task related to infrastructure', default=None)
    parser.add_argument('--setkey', help='Set the Google API key.', action='store_true')
    parser.add_argument("--set-model", metavar='MODEL', help="Set the Gemini model. Default is gemini-pro.")
    args = parser.parse_args()

    if args.setkey:
        api_key = input("Enter your Google API key: ")
        set_key(api_key)
        print("API key set successfully.")
    elif args.set_model:
        set_model(args.set_model)
        print(f"Model set to {args.set_model} successfully.")
    elif args.prompt:
        prompt_query = " ".join(args.prompt)  
        api_key, model = get_config()
        if not api_key:
            print("API key not found. Please set it using --setkey.")
            sys.exit(1)
        response = ask_ai(prompt_query, api_key, model)
    else:
        parser.print_help()

if __name__ == '__main__':
    cli()
