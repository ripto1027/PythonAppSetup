from urllib.error import HTTPError, URLError

from pythonappsetup.github import Github
from pythonappsetup.pdf_editor import PdfEditor
from pythonappsetup.release import Release


def main() -> None:
    try:
        repo_name: str = "PdfEditor"
        latest_release: Release = Github.get_release(repo_name)
        editor: PdfEditor = PdfEditor(latest_release)
        editor.download()

    except HTTPError as e:
        print(f"HTTPエラー: {e.reason}")
        print("リポジトリ名、公開設定、APIのURLを確認してください。")

    except URLError as e:
        print(f"通信エラー: {e.reason}")

    except (KeyError, ValueError, FileNotFoundError) as e:
        print(f"エラー: {e}")

if __name__ == "__main__": main()