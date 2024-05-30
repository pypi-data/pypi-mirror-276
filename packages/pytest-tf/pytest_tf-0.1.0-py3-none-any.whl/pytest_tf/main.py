import json
import pathlib
import types
import pytest
import sh

from pytest_tf.runner import TFRunner
from pytest_tf.exception import TFInitError, TFPlanError, TFApplyError, TFDestroyError
from pytest_tf.markers import TF_MARKER_PATH


@pytest.fixture
def tf(request, pytestconfig):
    path = _get_tf_path(request)

    runner = _get_tf_runner(pytestconfig)

    print(f"Running tf as {runner}")

    # Run tofu init
    _tf_init(runner, path)

    # Run tofu plan
    _tf_plan(runner, path)

    # Run tofu apply
    _tf_apply(runner, path)

    tfstate_path = path / "terraform.tfstate"
    with tfstate_path.open() as f:
        state = json.load(f)

    yield types.SimpleNamespace(state=state)

    # Run tofu destroy
    _tf_destroy(runner, path)


def handle_stdout(line):
    print(line, end="")


def _get_tf_runner(pytestconfig: pytest.Config) -> TFRunner:
    runner = pytestconfig.getini("tf_runner")
    return TFRunner(runner)


def _tf_init(runner: TFRunner, path: pathlib.Path):
    try:
        return runner.command.init(_cwd=path, _out=handle_stdout)
    except sh.ErrorReturnCode as e:
        raise TFInitError(e) from e


def _tf_plan(runner: TFRunner, path: pathlib.Path):
    try:
        return runner.command.plan(_cwd=path, _out=handle_stdout)
    except sh.ErrorReturnCode as e:
        raise TFPlanError.from_sh_error(e, path=path) from e


def _tf_apply(runner: TFRunner, path: pathlib.Path, auto_approve=True):
    try:
        return (
            runner.command.apply("-auto-approve", _cwd=path, _out=handle_stdout)
            if auto_approve
            else runner.command.apply(_cwd=path, _out=handle_stdout)
        )
    except sh.ErrorReturnCode as e:
        raise TFApplyError(e) from e


def _tf_destroy(runner: TFRunner, path: pathlib.Path, auto_approve=True):
    try:
        return (
            runner.command.destroy("-auto-approve", _cwd=path, _out=handle_stdout)
            if auto_approve
            else runner.command.destroy(_cwd=path, _out=handle_stdout)
        )
    except sh.ErrorReturnCode as e:
        raise TFDestroyError(e) from e


def _get_tf_path(request):
    tf_path = pathlib.Path(str(request.fspath)).parent

    for marker in request.node.iter_markers(name=TF_MARKER_PATH):
        tf_path /= pathlib.Path(marker.args[0])

    return tf_path
