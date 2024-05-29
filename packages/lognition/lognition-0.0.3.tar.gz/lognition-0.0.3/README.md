# Lognition's CustomLogger

`CustomLogger` is a flexible and customizable logging utility for Python applications. This library extends the standard logging module to include additional features such as automatic message formatting, endpoint filtering, progress spinners, and timers.

## Experimental

This package is currently under development and is only experimental. Features are likely to change in the upcoming updates.

## Features

- **Extended Logging Levels**: Supports additional levels like SPAM, VERBOSE, NOTICE, and SUCCESS.
- **Endpoint Filtering**: Customizable filter to ignore logs containing specified endpoints.
- **Flexible JSON Serialization**: Automatically serializes complex objects to JSON in log messages.
- **Progress Spinner**: Context manager for displaying a progress spinner with customizable messages and optional timers.
- **Execution Timer**: Context manager for timing code blocks with automatic logging of elapsed time.

## Installation

You can install `lognition` using pip:

```bash
pip install lognition
```

## Usage

### Basic Setup

```python
from lognition import CustomLogger

# Initialize the logger
logger = CustomLogger()
```

### Logging Messages

```python
# Log a simple message
logger.info("This is an informational message.")

# Log a JSON serializable object
logger.debug({"key": "value", "list": [1, 2, 3]})
```

### Filtering Endpoints

The `EndpointFilter` can be used to ignore logs containing specific endpoints or texts:

```python
# Initialize the logger with endpoint filtering
logger = CustomLogger(ignore=["/health", "Press CTRL+C to quit"])
```

### CustomLogger().spinner()

Use the `spinner` context manager to display a progress spinner with a message:

```python
with logger.spinner("Processing 4 steps...") as spinner:
    time.sleep(2)
    spinner.log("Finished step 1.")

    time.sleep(2)
    spinner.log("Finished step 2.")
    spinner.change("Halfway done.")

    time.sleep(2)
    spinner.log("Finished step 3.")

    time.sleep(2)
    spinner.log("Finished step 4.")

    spinner.change("Processing complete!")
```
```
Finished step 1. (2.00s)
Finished step 2. (4.00s)
Finished step 3. (6.00s)
Finished step 4. (8.00s)
✅ Processing complete! (8.00s)
```

You can manually `.fail()` the spinner:
```python
def add(a, b):
    return a + b

with logger.spinner("Doing heavy math...") as spinner:
    time.sleep(1)
    total = add(2, 2)
    if total != 3:
        spinner.fail(f"The function gave the wrong answer. Expected 3, got {total}")
```
```
💥 The function gave the wrong answer. Expected 3, got 4 (1.00s)
```

You can also manually run `.success()` to stop the spinner:
```python
def add(a, b):
    return a + b

with logger.spinner("Doing heavy math...") as spinner:
    time.sleep(1)
    total = add(2, 2)
    if total == 3:
        spinner.success(f"Breakthrough in math achieved!")
        # The spinner will stop running below this point
    time.sleep(10)
    spinner.fail("Math is hard :(") # This has no effect
```
```
✅ Breakthrough in math achieved! (1.00s)
```

You can use `.revert()` to change message back to original:
```python
with logger.spinner("Processing...") as spinner:
    time.sleep(2)
    spinner.change("Halfway done.")
    time.sleep(2)
    spinner.revert()
```
```
✅ Processing... (4.00s)
```

Using `.get_time()`:
```python
with logger.spinner(f"Encrypting {original_path}") as spinner:
    output_folder = "D:/Encrypted"
    encrypt_file(path, output_folder, "SECRET_PASSWORD", settings)
    time_taken = spinner.get_time()
    spinner.change(f"Encryption complete for {original_path}")
    mark_as_complete(name, time_taken)
```

You can also set the frequency of how fast the timer is updated (default is 0.1):
```python
with logger.spinner("Processing...", frequency=0.5) as spinner:
    time.sleep(5)
```

### CustomLogger().timer()

Use the `timer` context manager to measure and log the time taken for a code block:

```python
with logger.timer("Executing task"):
    time.sleep(3)
```
```
Executing task: 3.0026s
```

The `timer().get_time()` behaves the same as `spinner().timer()`. It's only added to `timer` in case we want to store the elapsed time:

```python
with logger.timer(f"Encrypting files") as timer:
    path = find_file()
    time_taken = timer.get_time()
    print(f"Time taken to find file: {time_taken}s")
    encrypt_file(path, output_folder, "SECRET_PASSWORD")
    time_taken = timer.get_time()
    print(f"Time taken to find file and encrypt it: {time_taken}s")
    mark_as_complete(path, time_taken)
```
```
Time taken to find file: 1.2001s
Time taken to find file and encrypt it: 2.6014s
Encrypting files: 2.6066s
```

## License

This project is licensed under the MIT License.

## Acknowledgements

This library uses the following third-party libraries:

- `coloredlogs`
- `verboselogs`
- `yaspin`

## Contact

For any questions or suggestions, please open an issue on GitHub.