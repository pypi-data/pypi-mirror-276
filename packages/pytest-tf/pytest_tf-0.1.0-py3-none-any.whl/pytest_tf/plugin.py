from pytest_tf.main import tf  # noqa: F401


def pytest_configure(config):
    config.addinivalue_line("markers", "only_plan: Only run plan, but don't apply.")
    config.addinivalue_line(
        "markers", "tf_path(path): Use the infrastructure defined under this folder."
    )


def pytest_addoption(parser):
    parser.addini(
        "tf_runner",
        "Which program should be used to build the infrastructure",
        default="tofu",
    )
