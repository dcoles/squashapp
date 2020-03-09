import os
import pathlib
import subprocess

import pytest

TESTDIR = pathlib.Path(__file__).parent
BASEDIR = TESTDIR.parent


@pytest.fixture
def testapp(tmp_path):
    subprocess.check_call([BASEDIR / 'build_squashapp', TESTDIR / 'testapp'], cwd=tmp_path)
    yield tmp_path


class SquashApp:
    def __init__(self, squashapp):
        self.squashapp = squashapp

    def run(self, args=None, **kwargs):
        args = args or []
        return subprocess.check_output([self.squashapp, *args], **kwargs)


def test_args(testapp):
    app = SquashApp(testapp / 'testapp.run')
    values = parse_values(app.run(['1', '2 two', '3'], encoding='utf-8'))

    assert values['ARGV0'].endswith('/bin/testapp')
    assert values['ARGV1'] == '1'
    assert values['ARGV2'] == '2 two'
    assert values['ARGV3'] == '3'
    assert values['SQUASHAPP_ARGV0'].endswith('/testapp')


def test_args_symlink(testapp):
    (testapp / 'foo').symlink_to('testapp.run')
    app = SquashApp(testapp / 'foo')
    values = parse_values(app.run(['1', '2 two', '3'], encoding='utf-8'))

    assert values['ARGV0'].endswith('/bin/testapp')
    assert values['ARGV1'] == '1'
    assert values['ARGV2'] == '2 two'
    assert values['ARGV3'] == '3'
    assert values['SQUASHAPP_ARGV0'].endswith('/foo')


def test_env(testapp):
    app = SquashApp(testapp / 'testapp.run')
    values = parse_values(app.run(encoding='utf-8'))

    assert values['SQUASHAPP_NAME'] == 'testapp'
    assert values['SQUASHAPP_MAIN'] == 'bin/testapp'
    assert values['SQUASHAPP_ARGV0'].endswith('/testapp')
    assert values['SQUASHAPP_MOUNT'].startswith('/tmp/squashapp.')


def parse_values(s):
    lines = s.splitlines()
    return {k.strip(): v.strip() for k, v in (l.split(':') for l in lines)}