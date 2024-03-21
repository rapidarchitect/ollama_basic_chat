# Ollama Chatbot

## Overview

This is a simple chatbot application that utilizes the Ollama AI platform to provide conversational responses. The chatbot is built using Python and HyperDiv for the user interface.

HyperDiv is a Python library for creating reactive user interfaces in web applications. It allows you to build interactive UI components using a declarative syntax.

## Installation

Before running the application, ensure you have Python 3.9 or later installed on your system. You also need to install the Ollama package from [https://ollama.ai](https://ollama.ai) on your chosen platform. And lastly you will need to be running Ollama on either your local machine or another host.

You can install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

## Note:

If you are running ollama on another host or a different port, change this line to reflect the host and port

```python
ollama_url = 'http://localhost:11434'
```

# Some HyperDiv Environment Variables

### HD_HOST

This environment variable allows setting the host that a Hyperdiv app runs on. The value should be a string representing a valid IP address or hostname, e.g. "0.0.0.0" (default value="localhost").

### HD_PORT

This environment variable allows setting the port that a Hyperdiv app runs on. The value should be an integer in valid port range, e.g. 8000.

### HD_PRODUCTION

When set to a true value, this environment disables "debug mode" in the internal Tornado server, which normally watches for file changes and auto-reloads the app when a dependent file is modified, and limits logging output.

Setting this environment variable causes all the environment variables in the Development Mode section below to be ignored, regardless of their values.

### HD_PRODUCTION_LOCAL

Works exactly like HD_PRODUCTION but in addition:

It causes run to automatically open a browser tab with the app running in it.

Hyperdiv automatically finds an open port on which to run the app when HD_PORT is left unset. The port search starts and 8988 and goes upward.

This environment variable is meant to be set when shipping apps that users can run locally on their computers. For example, when distributing an app on PyPI.
