# ErrorViewer
ErrorViewer is a Python script that provides a comprehensive way to handle and log errors in your Python programs. It offers various functionalities to customize error logging based on your requirements.
## Features
- **Error Logging**: Easily log errors along with customizable details.
- **Error Details**: Display error details such as error type, message, file name, file path, line number, and traceback information.
- **Flexible Configuration**: Choose specific error details to log based on your needs.
### Installation
ErrorViewer does not require any installation. Simply include the `errorlaw` function in your Python script or import it as a module.
### Example
```python
from syrabrox_errorviewer import errorlaw
try:
    # Your code that may raise exceptions
    pass
except Exception as e:
    errorlaw(e, "12345678", "filename.txt")
```
In the above example, the errorlaw function is called in the except block to log the error details.
### Parameters
exception: The exception object raised in the except block.\
intents: A string representing the error details to log. Each character corresponds to a specific detail:\
1: Error message.\
2: Error type.\
3: Error message.\
4: File name where the error occurred.\
5: Full file path.\
6: Line number where the error occurred.\
7: Traceback details.\
8: Log to file (optional, requires filename parameter).\
filename (optional): The name of the file to log errors. Defaults to "Error_Logs.txt".\
### Contribution
Contributions are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.
### License
```text
Copyright 2024 SyraBroX
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```