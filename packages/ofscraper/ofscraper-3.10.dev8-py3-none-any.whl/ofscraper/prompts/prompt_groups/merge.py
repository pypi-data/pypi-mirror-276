import pathlib

from InquirerPy.base import Choice
from InquirerPy.validator import PathValidator
from prompt_toolkit.shortcuts import prompt as prompt
from rich.console import Console

import ofscraper.prompts.prompt_validators as prompt_validators
import ofscraper.prompts.promptConvert as promptClasses
from ofscraper.utils.paths.common import get_profile_path

console = Console()
models = None


def backup_prompt_db() -> bool:
    name = "continue"
    answer = promptClasses.batchConverter(
        *[
            {
                "type": "list",
                "name": name,
                "message": "Have you backed up your database files?",
                "option_instruction": "Database files will be recursely searched and modified during the merge process",
                "choices": [Choice(True, "Yes"), Choice(False, "No")],
            }
        ]
    )
    return answer[name]


def folder_prompt_db():
    answer = promptClasses.batchConverter(
        *[
            {
                "type": "filepath",
                "name": "database",
                "message": "root database folder: ",
                "option_instruction": "The database path given will be searched recursively, so pick the closest path possible",
                "filter": lambda x: prompt_validators.cleanTextInput(x),
                "validate": PathValidator(is_dir=True),
                "default": str(get_profile_path()),
            },
        ]
    )
    return answer["database"]


def new_db_prompt():
    answer = promptClasses.batchConverter(
        *[
            {
                "type": "filepath",
                "name": "database",
                "message": "Merge db folder: ",
                "option_instruction": """
                directory for new merge database
                It is best if merged database is stored seperately from source database(s)
                """,
                "default": str(get_profile_path()),
                "filter": lambda x: prompt_validators.cleanTextInput(x),
            },
        ]
    )
    return answer["database"]


def confirm_prompt_db(folder, new_db) -> bool:
    name = "continue"
    answer = promptClasses.batchConverter(
        *[
            {
                "type": "list",
                "name": name,
                "message": "Confirm merge: ",
                "instruction": f"user_data.db files from {folder} will be merged into {str(pathlib.Path(new_db,'user_data.db'))}",
                "choices": [
                    Choice(True, "Yes"),
                    Choice(False, "No"),
                    Choice(None, "Back to Main Menu"),
                ],
                "default": False,
            }
        ]
    )
    return answer[name]


def model_id_prompt():
    answer = promptClasses.batchConverter(
        *[
            {
                "type": "inpit",
                "name": "database",
                "message": "Username/UD: ",
                "option_instruction": """
                Preferably the model ID
                """,
            },
        ]
    )
    return answer["database"]
