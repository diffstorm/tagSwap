# tagSwap - Tag Replacement Tool

TagSwap is a versatile tool for replacing predefined tags in multiple files based on variant-specific configurations. It simplifies the process of modifying files to adapt them to different target environments or use cases. TagSwap is particularly useful for multi-target deployments, pre-compile steps, or any scenario where you need to customize files with specific values.

## Features

- Replace tags in multiple files with variant-specific values.
- Create backups of modified files, allowing you to revert changes if needed.
- Support for various file types, including text-based formats such as code files, configuration files, HTML, and more.
- Easy-to-configure JSON files for specifying the files to modify and the variants to apply.

## Requirements

- Python 3.x
- Libraries listed in `requirements.txt`

To install the necessary libraries, use:
```
pip install -r requirements.txt
```

## Usage

1. Configure the `config.json` with the files and variants you want to apply.
2. Run the script with:
```
python tagSwap.py <config> <action> <variant_name>
```
- `<config>`: Specify the path to the `config.json` file, which contains all the configuration settings.
- `<action>`: Choose between `replace` to apply the variant-specific replacements, or `revert` to revert to the original files.
- `<variant_name>`: Provide the name of the variant as defined in the `config.json` file.

## Configuration (`config.json`)

- `files`: A list of files you want to modify.
- `variants`: A list of variant configurations. Each variant has:
  - `name`: Name of the variant.
  - `replacements`: Dictionary of tag-value pairs for replacements.

## Example

To replace tags in files based on the `variant1` configuration, use the following command:
```
python src/tagSwap.py config/config.json replace variant1
```

To revert the changes and restore the original files, use the following command:
```
python src/tagSwap.py config/config.json revert
```

## Summarize Configuration

To see a summary of the files and variants specified in config.json, you can use the `summarize` option:
```
python src/tagSwap.py config/config.json summarize
```

## Sample Configuration (config.json)

Here's an example config.json file:
```
{
    "files": [
        "file1.html",
        "file2.java",
        "file3.cpp"
    ],
    "variants": [
        {
            "name": "variant1",
            "replacements": {
                "{{MAX_USERS}}": "50",
                "{{LANGUAGE}}": "English",
                "{{WELCOME_MSG}}": "Hello, User!"
            }
        },
        // Additional variants...
    ]
}
```

## Sample Files

You can find sample files in various formats in the `test` directory of this repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```
This README.md file provides users with detailed information about how to use the TagSwap tool, its features, and configuration options. Users can also find examples and a sample configuration for reference. Don't forget to include the necessary license information in your project.
```
