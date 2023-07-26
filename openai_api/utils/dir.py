import os


def get_current_dir(current_file):
    return os.path.dirname(current_file)


def get_project_dir(current_dir, abs_dir):
    return os.path.abspath(os.path.join(current_dir, abs_dir))


def get_swagger_dir(project_dir):
    return os.path.join(project_dir, "ddc_api", "swagger")


def get_swagger_dir_by_current_file_and_abs_dir(current_file, abs_dir):
    current_dir = os.path.dirname(current_file)
    project_dir = os.path.abspath(os.path.join(current_dir, abs_dir))
    return os.path.join(project_dir, "ddc_api", "swagger")
