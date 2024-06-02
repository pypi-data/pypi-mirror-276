# Installation

S3 Bucket helper utils. Async list objects by folders 

## Installation

## Installing pipx
[`pipx`](https://pypa.github.io/pipx/) creates isolated environments to avoid conflicts with existing system packages.

=== "MacOS"
    In the terminal, execute:
    ```bash
    --8<-- "install_pipx_macos.sh"
    ```

=== "Linux"
    First, ensure Python is installed.

    Enter in the terminal:

    ```bash
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    ```

=== "Windows"
    First, install Python if it's not already installed.

    In the command prompt, type (if Python was installed from the Microsoft Store, use `python3` instead of `python`):
    
    ```bash
    python -m pip install --user pipx
    ```

## Installing `aws-s3`:
In the terminal (command prompt), execute:

```bash
pipx install aws-s3
```

### Advanced

Use 
```bash
aws-s3 --help
```
to see all available options.

![About](images/about.jpg)
[About][aws_s3.__about__]

