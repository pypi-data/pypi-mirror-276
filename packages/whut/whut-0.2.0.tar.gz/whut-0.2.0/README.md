# Whut

Whut is a command-line tool that allows you to search the internet using Google Generative AI. It provides a simple interface to get decluttered answers for your queries.

## Features

- Search the internet directly from your terminal.
- Customize the search prompt.
- Simple and easy-to-use command-line interface.

## Installation

You can install Whut from PyPI:

```sh
pip install whut


## Usage
To use Whut, simply type:

```whut "your search query"```

> Exampl: ```whut "Mahatma Gandhi"```

#-----

# Custom Prompt
You can customize the prompt used for searching by using the -C or --custom option:

```whut -C "Please provide detailed information about: {query}" "your search query"```

> Example: ```whut -C "Tell me in detail about: {query}" "Sam Altman"```
