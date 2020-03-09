import subprocess

import pytest

import util
from util import TESTDIR


@pytest.fixture(params=['bash', 'mksh', 'busybox'])
def build_squashapp(request, tmp_path):
    sh = TESTDIR / 'shells' / request.param / 'sh'
    if not sh.exists():
        pytest.skip(f'{request.param} shell not available')

    def _build(*args):
        util.build_squashapp(*args, shell=sh, cwd=tmp_path)

    _build.tmp_path = tmp_path
    return _build


def test_build(build_squashapp):
    build_squashapp(TESTDIR / 'testapp')

    assert (build_squashapp.tmp_path / 'testapp.run').exists()


def test_build_main(build_squashapp):
    build_squashapp(TESTDIR / 'testapp', 'bin/testapp')

    assert (build_squashapp.tmp_path / 'testapp.run').exists()


def test_build_missing_main_is_error(build_squashapp):
    with pytest.raises(subprocess.CalledProcessError):
        build_squashapp(TESTDIR / 'testapp', 'bin/no-such-file')


def test_build_abs_main_is_error(build_squashapp):
    with pytest.raises(subprocess.CalledProcessError):
        build_squashapp(TESTDIR / 'testapp', '/bin/testapp')


def test_build_external_main_is_error(build_squashapp):
    with pytest.raises(subprocess.CalledProcessError):
        build_squashapp(TESTDIR / 'testapp', '/bin/true')


def test_bad_shell_is_error(tmp_path):
    env = {'SQUASHAPP_SHELL': '/no-such-file'}
    with pytest.raises(subprocess.CalledProcessError):
        util.build_squashapp(TESTDIR / 'testapp', shell='/no-such-file', cwd=tmp_path)