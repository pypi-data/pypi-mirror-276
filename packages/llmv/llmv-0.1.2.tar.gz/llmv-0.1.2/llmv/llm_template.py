import json
from typing import Any, Tuple, Union
import re
from pathlib import Path
"""
# Overview

This code provides a framework for managing and formatting prompts using template files and extracting settings within those templates. Primarily, it is designed to facilitate the generation of text prompts for AI models, such as OpenAI's GPT series. Here is a high-level description of each component:

- **Settings Class**:
  - Contains default configuration settings including keys for input/output directories, filenames, temperature, max tokens, and model type.
  - The constructor initializes these settings either from defaults or from a given settings dictionary passed during instantiation.

- **LlmTemplate Class**:
  - Manages template strings for text generation prompts.
  - Offers methods to format these templates with input variables, extract and remove settings from the template, and substitute file contents into the templates.

## How to Use

1. **Initialization and Template Loading**:
    - Create an instance of `LlmTemplate` by passing the path to a template file or directly passing a template string.
    - Example:
      ```python
      llm_template = LlmTemplate.from_file('path/to/template.txt')
      ```

2. **Formatting the Template**:
    - Use the `format` method with the necessary arguments that will substitute placeholders in the template.
    - Example:
      ```python
      prompt, settings = llm_template.format(variable1="value1", variable2="value2")
      ```
    - This `format` method returns a tuple containing the formatted prompt string and a `Settings` object with extracted settings.

3. **Template Features**:
    - Variable Substitution: Placeholders in the form of `{{variable}}` in the template will be replaced by corresponding values from arguments passed to the `format` method.
    - File Content Insertion: Placeholders in the form of `{{file: filename}}` will be replaced by the contents of the specified file.
    - Settings Extraction: Lines in the template matching the format `<key>: <value>` will be extracted as settings and removed from the final formatted prompt.

This design allows flexible configuration and management of templates for various text generation tasks in a systematic and structured way.
"""

class Settings:
    input_dir_key = "input_directory"
    input_file_text_key = "input_file_text"
    input_filename_key = "input_filename"
    output_directory_key = "output_directory"
    split_input_json_key = "split_input_json"
    output_file_key = "output_file"

    temperature = 0.7
    max_tokens = 3500
    model = "gpt-4-turbo-preview"

    def __init__(self, settings) -> None:
        self.temperature = settings.get("temperature", self.temperature)
        self.max_tokens = settings.get("max_tokens", self.max_tokens)
        self.model = settings.get("model", self.model)


class LlmTemplate:
    template: str = ""

    def __init__(self, template: str):
        self.template = template

    def format(self, **kwargs: Any) -> Tuple[str, Settings]:
        """Format the prompt with the inputs.

        Args:
            kwargs: Any arguments to be passed to the prompt template.

        Returns:
            A formatted string.

        Example:

            .. code-block:: python

                prompt.format(variable1="foo")
        """
        prompt_args = kwargs
        template_with_subs = self.subsitute_variables(prompt_args)

        ## extract settings after subsitution
        settings = self.extract_settings(template_with_subs)
        prompt = self.subsitute_file_contents(self.remove_settings(template_with_subs))
        return prompt, Settings(settings)

    @classmethod
    def from_file(cls, template_file: Union[str, Path]):
        """Load a template from a file."""
        with open(str(template_file), "r") as f:
            template = f.read()
        return cls(template)

    def extract_settings(self, template):
        matches = re.findall("(\w*): ([^\n]*)", template)
        settings = {match[0]: match[1] for match in matches}
        return settings

    def remove_settings(self, template: str) -> str:
        return re.sub("(.|\n)*---", "", template)

    def subsitute_variables(self, vars):
        output = self.template
        indented_var_matches = re.findall("{{[^\$]*\$\[([^\]]*).*}}", self.template)
        for indented_match in indented_var_matches:
            if indented_match in vars:
                # output = output.replace("\$\["+ indented_match + "\]", indented_match)
                value = vars[indented_match]
                # if value is not a string, convert it to a string
                if not isinstance(value, str):
                    value = json.dumps(value, ensure_ascii=False)
                    
                escaped_replacement = re.escape(vars[indented_match])
                output = re.sub(
                    "\$\[" + indented_match + "\]", escaped_replacement, output
                )

        for key, value in vars.items():
            if not isinstance(value, str):
                    value = json.dumps(value, ensure_ascii=False)
            escaped_replacement = re.escape(value)
            output = re.sub("{{" + key + "}}", escaped_replacement, output)
        return output

    def subsitute_file_contents(self, template):
        p = re.compile("{{file:\s?([^}]*)}}", re.IGNORECASE)
        match = p.search(template)
        if not match:
            return template

        file_name = match.group(1)

        with open(file_name) as f:
            text = f.read()
        template_with_sub = template.replace(match.group(), text)
        return self.subsitute_file_contents(template_with_sub)
