from breadslicer.utility.command import capture_cmd


def get_author_from_git() -> str:
    return capture_cmd(["git", "config", "--global", "user.name"]).strip()


def get_email_from_git() -> str:
    return capture_cmd(["git", "config", "--global", "user.email"]).strip()
