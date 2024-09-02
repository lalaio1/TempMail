# TempMail Library Documentation

Welcome to the TempMail library documentation! This guide will walk you through how to use all the features of the `TempMail` library. The library provides an easy-to-use interface for generating temporary email addresses, checking inboxes, and retrieving email messages. This is particularly useful for testing, protecting your primary email, and other scenarios where disposable email addresses are needed.

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Class Overview](#class-overview)
4. [Features](#features)
   - [Connecting to Tor Network](#connecting-to-tor-network)
   - [Proxy Check](#proxy-check)
   - [Generating Temporary Email](#generating-temporary-email)
   - [Checking Inbox](#checking-inbox)
   - [Processing Emails](#processing-emails)
   - [Storing Emails](#storing-emails)
5. [Usage Examples](#usage-examples)
   - [Basic Usage](#basic-usage)
   - [Using with Custom Headers](#using-with-custom-headers)
   - [Using with Tor](#using-with-tor)
   - [Using with Proxy](#using-with-proxy)
   - [Email Storage in CSV](#email-storage-in-csv)
6. [Configuration Options](#configuration-options)
7. [Error Handling](#error-handling)
8. [Contributing](#contributing)
9. [License](#license)

---

## Installation

You can install the TempMail library via pip. Ensure that you have Python 3.6+ installed.

```bash
pip install .
```

---

## Quick Start

Here’s a quick example to get you started with TempMail:

```python
from TempMail import TempMail

# Initialize the TempMail object
tm = TempMail()

# Generate a random email
tm.generate_email()

# Check the inbox for new emails
tm.check_inbox()
```

---

## Class Overview

### `TempMail` Class

The `TempMail` class is the main class you will interact with. It contains methods to generate temporary emails, check inboxes, and process emails.

### Constructor Parameters:

- **domain**: (Optional) Domain name for the email. If not provided, a random domain will be selected.
- **check_interval**: Interval in seconds to check the inbox. Default is `0.5`.
- **output_file**: File to store the emails. Supports text and CSV files.
- **no_box**: Boolean to skip retrieving the full email body. Default is `False`.
- **only_subject**: Boolean to store only the email subject. Default is `False`.
- **only_id**: Boolean to store only the email ID. Default is `False`.
- **no_router**: Boolean to skip connecting to the Tor network. Default is `False`.
- **agent**: Custom user agent string. If not provided, a random one is generated.
- **proxy**: Proxy server to use. If not provided, defaults to Tor proxy.
- **tor_port**: Port for Tor connection. Default is `9051`.
- **tor_password**: Password for Tor connection. Default is `obagulhoeouvirplug`.
- **custom_headers**: Dictionary of custom headers for requests. Default is `None`.
- **initial_check_interval**: Delay in seconds before starting the first inbox check. Default is `0`.
- **log_errors**: Boolean to log errors. Default is `False`.
- **storage_type**: Type of storage for emails (`file` or `csv`). Default is `file`.

---

## Features

### Connecting to Tor Network

By default, TempMail connects to the Tor network to enhance privacy. This can be disabled by setting `no_router=True`.

```python
tm = TempMail(no_router=True)
```

### Proxy Check

You can check the current IP address and location of your proxy.

```python
tm.check_proxy()
```

### Generating Temporary Email

Generate a temporary email address with a random or specified domain.

```python
tm.generate_email(domain='1secmail.com')
```

### Checking Inbox

Check the inbox for new emails. The inbox is checked at regular intervals defined by `check_interval`.

```python
tm.check_inbox()
```

### Processing Emails

The `process_email` method processes and outputs email details. It supports storing email information in a file or CSV format.

```python
def process_email(self, username, domain, email):
    # Process and store email details
```

### Storing Emails

Emails can be stored in a text file or a CSV file. You can specify the storage type and file path during initialization.

```python
tm = TempMail(output_file='emails.txt', storage_type='file')
```

---

## Usage Examples

### Basic Usage

```python
from TempMail import TempMail

# Initialize the TempMail object
tm = TempMail()

# Generate a random email
tm.generate_email()

# Check the inbox for new emails
tm.check_inbox()
```

### Using with Custom Headers

```python
headers = {
    'X-Custom-Header': 'value'
}

tm = TempMail(custom_headers=headers)
tm.generate_email()
```

### Using with Tor

```python
tm = TempMail(tor_port=9051, tor_password='your_tor_password')
tm.run()
```

### Using with Proxy

```python
tm = TempMail(proxy='http://yourproxy.com:8080')
tm.run()
```

### Email Storage in CSV

```python
tm = TempMail(output_file='emails.csv', storage_type='csv')
tm.run()
```

---

## Configuration Options

Below are the options available for configuring the `TempMail` class:

| Parameter             | Description                                                | Default Value          |
|-----------------------|------------------------------------------------------------|------------------------|
| `domain`              | Domain for the email.                                       | `None`                 |
| `check_interval`      | Interval to check the inbox (in seconds).                   | `0.5`                  |
| `output_file`         | File path to store the emails.                              | `None`                 |
| `no_box`              | Skip retrieving the full email body.                        | `False`                |
| `only_subject`        | Store only the email subject.                               | `False`                |
| `only_id`             | Store only the email ID.                                    | `False`                |
| `no_router`           | Disable Tor connection.                                     | `False`                |
| `agent`               | Custom user agent string.                                   | `None`                 |
| `proxy`               | Proxy server URL.                                           | `None`                 |
| `tor_port`            | Port for Tor connection.                                    | `9051`                 |
| `tor_password`        | Password for Tor connection.                                | `obagulhoeouvirplug`   |
| `custom_headers`      | Dictionary of custom headers.                               | `None`                 |
| `initial_check_interval` | Delay before starting the first inbox check (in seconds). | `0`                    |
| `log_errors`          | Enable error logging.                                       | `False`                |
| `storage_type`        | Type of storage for emails (`file` or `csv`).               | `file`                 |

---

## Error Handling

The TempMail class includes basic error handling. Errors are logged using the `log_error` method if `log_errors=True`.

```python
def log_error(message, log_errors):
    if log_errors:
        print(f"Error: {message}")
```

---

## Contributing

Contributions are welcome! If you find a bug or want to add a new feature, feel free to open an issue or submit a pull request on GitHub.

---

## License

This library is licensed under the MIT License. See the `LICENSE` file for more details.

