# omnijp
 OmniJP is a Python library that provides tools for common tasks in software development. 
It now supports features for caching database results to disk and making HTTP requests with caching support.

## Features

- **Database Disk Cache**: OmniJP provides a way to cache database results to disk. This is useful for large datasets that you don't want to query every time. The data is saved in CSV format and can be optionally zipped.

- **HTTP Requests**: OmniJP includes a simple HTTP request class with caching support. This can be used to make GET requests and cache the results for future use.

## Installation

You can install OmniJP using pip:

```bash
pip install omnijp
```

## Usage
### DbDiskCache

Here's an example of how to use the `DbDiskCache` class to cache database results:

```python
from src.dbdisk.db_disk_cache_builder import DbDiskCacheBuilder
from src.dbdisk.types import DbType, DiskFileType

CONNECTION_STRING = "your_connection_string"

result = DbDiskCacheBuilder.create(lambda x: (
    x.set_db_type(DbType.POSTGRESQL)
    # currently only csv is supported
    .set_disk_file_type(DiskFileType.CSV)
    .set_cache_path(r"C:\temp\diskCache")
    .set_cache_name("users")
    .set_connection_string(CONNECTION_STRING)
    .set_rows_per_file(1000)
    .set_can_zip(True)
)).execute("select * from Users where retired != 1")
```
### HttpCachedRequest
And here's an example of how to use the `HttpCachedRequest` class to make a GET request and cache the result:

```python
from omnijp import HttpCachedRequest

http_cached_request = HttpCachedRequest().set_base_url('https://jsonplaceholder.typicode.com').\
    set_cache('C:\\temp\\restq').build()

response = http_cached_request.request_get('posts?_limit=10', 'posts')
```
### AsyncOpenAIBot
And here's an example of how to use the `AsyncOpenAIBot` 
To use the AsyncOpenAIBot class, you need to provide a valid OpenAI API key when creating an instance of the class. 
This key is used to authenticate your requests to the OpenAI API.  

Here's a basic example of how to use the AsyncOpenAIBot class:
```python
import os
from src.openaibot.openai_bot import OpenAIBot
def my_callback(response):
    print("Received response:", response)

def run_bot_async():
    import asyncio
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key is None:
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)

    openai_bot = AsyncOpenAIBot(openai_key)
    while True:
        user_input = input("Enter your question:").lower()
        if user_input == "exit":
            break
        asyncio.run(openai_bot.get_response_async(user_input, my_callback))


if __name__ == "__main__":
    try:
        run_bot_async()
    except Exception as e:
        print(e)
```
In this example, my_callback is a function that will be called with the response from the OpenAI API.

### OpenAIBot
Synchronous version of the OpenAIBot class
```python
def run_bot():
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key is None:
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)

    openai_bot = OpenAIBot(openai_key)
    response = openai_bot.get_response("1+1?")
    print("OpenAI Response:", response)
```
```python
if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        print(e)
```

#### Error Handling
The OpenAIBot class also handles some exceptions that might occur during the interaction with the OpenAI API:  
**openai.RateLimitError**: This exception is raised when the rate limit of the API is exceeded. The method raises a new exception with a custom message in this case.  
**openai.AuthenticationError**: This exception is raised when the authentication with the API fails (for example, if the API key is incorrect). The method raises a new exception with a custom message in this case.  
**openai.OpenAIError**: This is a general exception for other errors that might occur during the interaction with the API. The method raises a new exception with a custom message in this case.  
You can catch these exceptions in your code and handle them as needed.

## Testing

The library includes unit tests that you can run to verify its functionality. You can run the tests using the following command:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.