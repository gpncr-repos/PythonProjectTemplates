#!/usr/bin/env python
import re
import sys
import textwrap

COMMIT_MESSAGE_FILEPATH = ".git/COMMIT_EDITMSG"
REGEX = r"(build|chore|docs|feat|fix|perf|refactor|test)\(\S*\): .*\n\n.*\n\nРешено: (T-|TT-|#)\d*"
ERROR_MESSAGE = textwrap.dedent(
    """\
        <build | chore | docs | feat | fix | perf | refactor | test>(<scope>): <subject>

        <body>

        <footer>
    """
)


def main() -> None:
    """
    Точка входа в скрипт
    :return: успешность операции
    """

    commit_msg = get_commit_message()
    check_commit_message(commit_msg)


def get_commit_message() -> str:
    """
    Получить сообщение коммита
    :return: сообщение коммита
    """

    try:
        with open(COMMIT_MESSAGE_FILEPATH, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("Commit file not found")

        sys.exit(1)


def check_commit_message(commit_message: str) -> None:
    """
    Проверить сообщение коммита на соответствие шаблону
    :param commit_message: сообщение коммита
    """

    if re.search(REGEX, commit_message) is None:
        print(f"Current commit message: {commit_message}")
        print(f"The commit message does not meet the template: {ERROR_MESSAGE}")
        print("commit-msg hook failed (add --no-verify to bypass)")

        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
