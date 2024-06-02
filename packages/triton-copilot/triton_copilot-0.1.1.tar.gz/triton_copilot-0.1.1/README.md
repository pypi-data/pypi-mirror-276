# Triton-Server Co-Pilot

Triton-Server Co-Pilot is an innovative tool designed to streamline the process of converting any model code into Triton-Server compatible code, simplifying deployment on NVIDIA Triton Inference Server. This project automatically generates necessary configuration files (`config.pbtxt`) and custom wrapper code (`model.py`), among others, facilitating seamless integration and deployment of AI models in production environments.

## Features and Benefits

- **Automatic Code Conversion**: Convert your model code into Triton-Server compatible code.
- **Configuration File Generation**: Automatically generates `config.pbtxt` files tailored to your specific model requirements.

## Prerequisites
- Your model code ready for conversion

## Installation

1. Clone the Triton-Server Co-Pilot repository:
   ```bash
   git clone https://github.com/inferless/triton-copilot.git
   cd triton-copilot
   poetry build
   pip3 install ./dist/triton_copilot-0.1.0-py3-none-any.whl --force-reinstall 

### 6. File Structure

```markdown
## File Structure

- `config.pbtxt`: Configuration file for Triton Server, specifying model parameters.
- `model.py`: Custom wrapper code for your model, ensuring compatibility with Triton Server.
```

## Contributing

Contributions to Triton-Server Co-Pilot are welcome! Please refer to our contribution guidelines for more information on how to submit issues, make pull requests, and more.

## License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for more details.

## Contact

For support or queries, please contact us at [hello@inferless.com].
