<h1 align="center">Salve v0.2.0</h1>

> **Note**
> This package does not work on Windows machines as `Selector.select()` does not work on them.

# Installation

In the Command Line, paste the following: `pip install salve_ipc`

## Description

Salve is an IPC library that can be used by code editors to get autocompletions, replacements, and syntax highlighting.

## Documentation

### `COMMANDS`

The `COMMANDS` list contains all valid commands to request server output from. If multiple requests of different commands are made they will be kept and held seperately and can be retrieved seperately. Current commands are as follows:

- "autocomplete"
- "replacements"
- "highlight"

### `generic_tokens`

The `generic_tokens` list is a list of strings that define all of the generic token types returned by the server which can be mapped to colors for syntax highlighting.

### `Request` and `Response` TypedDict classes

The `Request` and `Response` TypedDict classes allow for type checking when handling output from salve_ipc.

### `Token` dataclass

The `Token` dataclass gives easy type checking for tokens returned from the highlight command.

### `is_unicode_letter(char: str) -> bool`

The `is_unicode_letter()` function returns a boolean if a given word is a unicode letter (includes "\_" as special case) which can be useful when trying to find the current word being typed to hand to the IPC for autocompletion.

### `tokens_from_result(result: list[str]) -> list[Token]`

The `tokens_from_result()` function takes the results from a `highlight` commands results output and returns a list `Token` types from it to be used for highlighting.

### `IPC` Class

| Method              | Description                                                                                                                                                                                                                                                                                          | Arguments                                                                                                                                                                         |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.ping()`           | Pings the server. After five seconds the server closes if not pinged so it is better for performance to keep it alive but it will be reopened either way                                                                                                                                             | None                                                                                                                                                                              |
| `.get_response()`   | Gets a response of the requested command                                                                                                                                                                                                                                                             | `command`: str                                                                                                                                                                    |
| `.request()`        | Makes a request to the server                                                                                                                                                                                                                                                                        | `command`: str, `file`: str, `expected_keywords`: list[str] ("autocomple" or "replacements"), `current_word`: str ("autocomple" or "replacements"), `language`: str ("highlight") |
| `.cancel_request()` | Cancels request of command type and removes reponse if it was recieved. Must be called before `.get_response()` to work                                                                                                                                                                              | `command`: str                                                                                                                                                                    |
| `.update_file()`    | Updates files stored on the server that are used to get responses                                                                                                                                                                                                                                    | `filename`: str, `current_state`: str (just the text of the file)                                                                                                                 |
| `.remove_file()`    | Removes a file of the name given if any exists. Note that a file should only be removed when sure that all other requests using the file are completed. If you delete a file right after a request you run the risk of it removing the file before the task could be run and causing a server crash. | `filename`: str                                                                                                                                                                   |
| `.kill_IPC()`       | This kills the IPC process and acts as a precaution against wasted CPU when the main thread no longer needs the IPC                                                                                                                                                                                  | None                                                                                                                                                                              |

### Basic Usage:

```python
from os import set_blocking
from selectors import EVENT_READ, DefaultSelector
from sys import stdin, stdout

from salve_ipc import IPC, Response

autocompleter = IPC()

set_blocking(stdin.fileno(), False)
set_blocking(stdin.fileno(), False)
selector = DefaultSelector()
selector.register(stdin, EVENT_READ)

stdout.write("Code: \n")
stdout.flush()

while True:
    # Keep IPC alive
    autocompleter.ping()

    # Add file
    autocompleter.add_file("test", "")

    # Check input
    events = selector.select(0.025)
    if events:
        # Make requests
        for line in stdin:
            autocompleter.update_file("test", line)
            autocompleter.request(
                "autocomplete",
                expected_keywords=[],
                full_text=line,
                current_word=line[-2],
            )

    # Check output
    output: Response | None = autocompleter.get_response()
    if not output:
        continue
    stdout.write(str(output) + "\n")
    stdout.flush()
```

## How to run and contribute

### Running

To run the example, move `examples/example_usage.py` to the root directory and run with python.

To test newer features or test code in a Pull Review, do the same but move it back after if you plan to make a PR.

### Contributing

To contribute, fork the repository, make your changes, and then make a pull request. If you want to add a feature, please open an issue first so it can be discussed. Note that whenever and wherever possible you should try to use stdlib modules rather than external ones.

## License

This project is licensed under the MIT License - see the [LICENSE](./LISCENSE).
