# converter.py
import json
import markdown

class ContentConverter:
    @staticmethod
    def save_as_text(content, output_file):
        """
        Saves the content as a text file.
        
        Args:
            content (str): The content to save.
            output_file (str): The path to the output file.
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def save_as_json(content, output_file):
        """
        Saves the content as a JSON file.
        
        Args:
            content (str): The content to save.
            output_file (str): The path to the output file.
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def convert_to_markdown(content):
        """
        Converts the content to Markdown format.
        
        Args:
            content (str): The content to convert.
        
        Returns:
            str: The content in Markdown format.
        """
        return markdown.markdown(content)
