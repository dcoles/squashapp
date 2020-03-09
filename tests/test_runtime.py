import subprocess

import pytest

from util import build_squashapp, TESTDIR


@pytest.fixture(params=['bash', 'mksh', 'busybox'])
def build_testapp(request, tmp_path):
    sh = TESTDIR / 'shells' / request.param / 'sh'
    if not sh.exists():
        pytest.skip(f'{request.param} shell not available')

    def _build(*args, squashapp=None):
        squashapp = squashapp or tmp_path / 'testapp.run'
        build_squashapp(TESTDIR / 'testapp', *args, shell=sh, cwd=tmp_path)
        return SquashApp(squashapp)

    _build.tmp_path = tmp_path
    return _build


class SquashApp:
    def __init__(self, squashapp):
        self.squashapp = squashapp

    def run(self, args=None, **kwargs):
        args = args or []
        return subprocess.check_output([self.squashapp, *args], **kwargs)


def test_args(build_testapp):
    app = build_testapp()
    values = parse_values(app.run(['1', '2 two', '3'], encoding='utf-8'))

    assert values['ARGV0'].endswith('/bin/testapp')
    assert values['ARGV1'] == '1'
    assert values['ARGV2'] == '2 two'
    assert values['ARGV3'] == '3'
    assert values['SQUASHAPP_ARGV0'].endswith('/testapp')


def test_args_symlink(build_testapp):
    (build_testapp.tmp_path / 'foo').symlink_to('testapp.run')
    app = build_testapp(squashapp=build_testapp.tmp_path / 'foo')
    values = parse_values(app.run(['1', '2 two', '3'], encoding='utf-8'))

    assert values['ARGV0'].endswith('/bin/testapp')
    assert values['ARGV1'] == '1'
    assert values['ARGV2'] == '2 two'
    assert values['ARGV3'] == '3'
    assert values['SQUASHAPP_ARGV0'].endswith('/foo')


def test_env(build_testapp):
    app = build_testapp()
    values = parse_values(app.run(encoding='utf-8'))

    assert values['SQUASHAPP_NAME'] == 'testapp'
    assert values['SQUASHAPP_MAIN'] == 'bin/testapp'
    assert values['SQUASHAPP_ARGV0'].endswith('/testapp')
    assert values['SQUASHAPP_MOUNT'].startswith('/tmp/squashapp.')


def parse_values(s):
    """Parse `key: value` lines"""
    lines = s.splitlines()
    return {k.strip(): v.strip() for k, v in (l.split(':') for l in lines)}