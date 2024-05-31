# ---------------------------------------------------------------
# Test the RAI CLI commands
# ---------------------------------------------------------------

import sys
import pytest
from unittest.mock import patch
from click.testing import CliRunner

from relationalai.clients.config import ConfigStore

@pytest.fixture(autouse=True)
def run_before_each_test(mocker):
    # Mock get_config before each test so we can deal with the ensure_config
    get_config = mocker.patch('relationalai.tools.cli_helpers.get_config')
    gs_instance = get_config.return_value
    gs_instance.get.file_path = "some path"

    yield

    # Cleanup
    mocker.stopall()

# ---------------------------------------------------------------
# rai config:check
# ---------------------------------------------------------------
def test_config_check(mocker):
    from relationalai.tools.cli import config_check
    engine_response = {'name': 'foo', 'size': 'XS', 'state': 'SUSPENDED'}
    rv = {}
    rv['platform'] = 'snowflake'
    rv['account'] = 'foo-account'
    rv['role'] = 'CONSUMER'
    rv['warehouse'] = 'WH'
    rv['rai_app_name'] = 'APP'
    rv['user'] = 'usr'
    rv['password'] = 'pwd'

    mocker.stopall()

    cs = mocker.patch.object(ConfigStore, 'get')
    cs.return_value = None

    gfc = mocker.patch('relationalai.clients.config._get_full_config')
    gfc.return_value = rv, "some path"

    # ---------------------------------------------------------------
    #  Engine/Prop not found
    # ---------------------------------------------------------------

    runner = CliRunner()
    result = runner.invoke(config_check)

    assert "Error: Missing config value for 'engine'" in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Engine not found
    # ---------------------------------------------------------------

    rv['engine'] = 'foo'

    get_rp = mocker.patch('relationalai.tools.cli.get_resource_provider')
    instance = get_rp.return_value
    instance.get_engine.return_value = None

    result = runner.invoke(config_check)

    assert "Error: Configured engine 'foo' not found" in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Engine in wrong state
    # ---------------------------------------------------------------

    instance.get_engine.return_value = engine_response
    instance.is_valid_engine_state.return_value = False

    result = runner.invoke(config_check)

    assert "Error: Engine 'foo' is in an invalid state: 'SUSPENDED'" in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  All good
    # ---------------------------------------------------------------

    instance.is_valid_engine_state.return_value = True
    spy = mocker.spy(instance, 'get_engine')

    result = runner.invoke(config_check)

    spy.assert_called_once_with('foo')
    assert "Connection successful!" in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Exception handling
    # ---------------------------------------------------------------

    with patch('relationalai.tools.cli.get_resource_provider', side_effect=Exception('Provider Error')):
      result = runner.invoke(config_check)

    assert "Error: Provider Error" in result.output
    assert result.exit_code == 0

# ---------------------------------------------------------------
# rai profiles:switch
# ---------------------------------------------------------------
def test_profiles_switch(mocker):
    from relationalai.tools.cli import profile_switch

    # Setup mocks for the ConfigStore used throughout the test
    rv = {'sf': { "platform":"snowflake" }, 'az': { "platform":"azure" }}
    mocker.patch('relationalai.clients.config.ConfigStore.get_profiles', return_value = rv)
    mocker.patch('relationalai.clients.config.ConfigStore.change_active_profile', return_value = True)
    mocker.patch('relationalai.clients.config.ConfigStore.save', return_value = True)

    # ---------------------------------------------------------------
    #  Switch profile (non-interactive mode)
    # ---------------------------------------------------------------

    spy_profile = mocker.spy(ConfigStore, 'change_active_profile')
    spy_save = mocker.spy(ConfigStore, 'save')

    runner = CliRunner()
    result = runner.invoke(profile_switch, ['--profile', 'az'])
    spy_profile.assert_called_once_with('az')
    spy_save.assert_called_once_with()
    assert "✓ Switched to profile 'az'" in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Switch profile (interactive mode)
    # ---------------------------------------------------------------

    spy_profile = mocker.spy(ConfigStore, 'change_active_profile')
    spy_save = mocker.spy(ConfigStore, 'save')

    fuzzy_mock = mocker.patch('relationalai.tools.cli_controls.fuzzy')
    fuzzy_mock.return_value = 'sf'

    runner = CliRunner()
    result = runner.invoke(profile_switch)

    spy_profile.assert_called_once_with('sf')
    spy_save.assert_called_once_with()
    assert "✓ Switched to profile 'sf'" in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Clean slate - no profiles
    # ---------------------------------------------------------------

    # Kills all mocks - last in this test - position matters
    mocker.stopall()
    runner = CliRunner()
    result = runner.invoke(profile_switch)
    assert 'No profiles found' in result.output
    assert result.exit_code == 0

# ---------------------------------------------------------------
# rai engines:get
# ---------------------------------------------------------------
def test_engines_get(mocker):
    from relationalai.tools.cli import engines_get
    mocked_response = {'name': 'foo', 'size': 'XS', 'state': 'READY'}
    text_mock = mocker.patch('relationalai.tools.cli_controls.text')
    get_rp = mocker.patch('relationalai.tools.cli.get_resource_provider')
    instance = get_rp.return_value

    # ---------------------------------------------------------------
    #  Get the engine (non-interactive mode)
    # ---------------------------------------------------------------

    instance.get_engine.return_value = None

    runner = CliRunner()
    result = runner.invoke(engines_get, ['--name', 'baz'])
    assert 'Engine "baz" not found' in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Get the engine (interactive mode)
    # ---------------------------------------------------------------

    instance.get_engine.return_value = mocked_response

    # controls.text() is mocked to return "foo" here
    text_mock.return_value = "foo"

    runner = CliRunner()
    result = runner.invoke(engines_get)
    assert "foo    XS     READY" in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Engine not found
    # ---------------------------------------------------------------

    instance.get_engine.return_value = None

    runner = CliRunner()
    result = runner.invoke(engines_get)
    assert 'Engine "foo" not found' in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Exception handling
    # ---------------------------------------------------------------

    with patch('relationalai.tools.cli.get_resource_provider', side_effect=Exception('Provider Error')):
      result = runner.invoke(engines_get)

    assert "Error fetching engine: Provider Error" in result.output
    assert result.exit_code == 1

# ---------------------------------------------------------------
# rai engines:delete
# ---------------------------------------------------------------
def test_engines_delete(mocker):
    from relationalai.tools.cli import engines_delete
    get_rp = mocker.patch('relationalai.tools.cli.get_resource_provider')
    instance = get_rp.return_value

    # ---------------------------------------------------------------
    #  Engine not found
    # ---------------------------------------------------------------

    instance.get_engine.return_value = None

    runner = CliRunner()
    result = runner.invoke(engines_delete, ['--name', 'baz'])
    assert "Engine 'baz' not found" in result.output
    assert result.exit_code == 1

    # ---------------------------------------------------------------
    #  Engine found - Delete engine
    # ---------------------------------------------------------------

    engine_response = {'name': 'foo', 'size': 'S', 'state': 'READY'}
    instance.get_engine.return_value = engine_response
    spy = mocker.spy(instance, 'delete_engine')

    runner = CliRunner()
    result = runner.invoke(engines_delete, ['--name', 'foo'])
    spy.assert_called_once_with('foo')
    assert "Engine 'foo' deleted!" in result.output

    # ---------------------------------------------------------------
    #  SETUP_CDC Exception
    # ---------------------------------------------------------------

    instance.get_engine.return_value = [{'name': 'bar', 'size': 'S', 'state': 'READY'}]
    instance.delete_engine.side_effect = Exception('SETUP_CDC Error')

    runner = CliRunner()
    result = runner.invoke(engines_delete, ['--name', 'bar'])

    assert "Imports are setup to utilize this engine.\nUse 'rai imports:setup --engine' to set a different engine for imports." in result.output
    assert result.exit_code == 0

# ---------------------------------------------------------------
# rai engines:list
# ---------------------------------------------------------------
def test_engines_list(mocker):
    from relationalai.tools.cli import engines_list
    mocked_response = [
      {'name': 'test', 'size': 'XS', 'state': 'READY'},
      {'name': 'foo', 'size': 'XS', 'state': 'READY'},
      {'name': 'bar', 'size': 'S', 'state': 'READY'},
      {'name': 'baz', 'size': 'M', 'state': 'PENDING'}
    ]

    # ---------------------------------------------------------------
    #  Listing the engines
    # ---------------------------------------------------------------

    get_rp = mocker.patch('relationalai.tools.cli.get_resource_provider')
    instance = get_rp.return_value
    instance.list_engines.return_value = mocked_response

    runner = CliRunner()

    result = runner.invoke(engines_list)

    assert "1   test   XS     READY" in result.output
    assert "2   foo    XS     READY" in result.output
    assert "3   bar    S      READY" in result.output
    assert "4   baz    M      PENDING" in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Listing the engines (Filter by state)
    # ---------------------------------------------------------------

    get_rp = mocker.patch('relationalai.tools.cli.get_resource_provider')
    instance = get_rp.return_value
    spy = mocker.spy(instance, 'list_engines')

    runner = CliRunner()
    result = runner.invoke(engines_list, ['--state', 'ready'])

    spy.assert_called_once_with('ready')
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  No engines found
    # ---------------------------------------------------------------

    instance.list_engines.return_value = []

    result = runner.invoke(engines_list)
    assert "No engines found" in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Handle exception
    # ---------------------------------------------------------------

    with patch('relationalai.tools.cli.get_resource_provider', side_effect=Exception('Provider Error')):
      result = runner.invoke(engines_list)

    assert "Error fetching engines: Provider Error" in result.output
    assert result.exit_code == 1

# ---------------------------------------------------------------
# rai version
# ---------------------------------------------------------------
def test_rai_version(mocker):
    from relationalai.tools.cli import version
    from relationalai import __version__ as rai_version
    from railib import __version__ as railib_version

    runner = CliRunner()
    python_version = sys.version.split()[0]

    # ---------------------------------------------------------------
    #  No configuration file found with no latest version
    # ---------------------------------------------------------------

    get_config = mocker.patch('relationalai.tools.cli.get_config')
    instance = get_config.return_value
    instance.file_path = None

    latest_version = mocker.patch('relationalai.tools.cli.latest_version')
    latest_version.return_value = None

    result = runner.invoke(version)

    assert f"RelationalAI   {rai_version}" in result.output
    assert f"Rai-sdk        {railib_version}" in result.output
    assert f"Python         {python_version}" in result.output
    assert "App            No configuration file found. To create one, run: rai init" in result.output
    assert "→" not in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  No configuration file found with latest version
    # ---------------------------------------------------------------

    latest_version.return_value = "10000.1.1"

    result = runner.invoke(version)

    assert f"RelationalAI   {rai_version} → 10000.1.1" in result.output
    assert f"Rai-sdk        {railib_version} → 10000.1.1" in result.output
    assert f"Python         {python_version}" in result.output
    assert "App            No configuration file found. To create one, run: rai init" in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Current is newer than latest
    # ---------------------------------------------------------------

    latest_version.return_value = "0.0.1"

    result = runner.invoke(version)
    assert f"RelationalAI   {rai_version}" in result.output
    assert "→ 0.0.1" not in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Configuration file found - Snowflake - Show App version
    # ---------------------------------------------------------------

    get_config = mocker.patch('relationalai.tools.cli.get_config')
    instance = get_config.return_value
    instance.file_path = "some path"
    instance.get.return_value = "snowflake"

    get_rp = mocker.patch('relationalai.tools.cli.get_resource_provider')
    instance = get_rp.return_value
    instance.get_version.return_value = "1.0.0"

    result = runner.invoke(version)

    assert f"RelationalAI   {rai_version}" in result.output
    assert f"Rai-sdk        {railib_version}" in result.output
    assert f"Python         {python_version}" in result.output
    assert "App            1.0.0" in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Configuration file found - Azure
    # ---------------------------------------------------------------

    get_config = mocker.patch('relationalai.tools.cli.get_config')
    instance = get_config.return_value
    instance.file_path = "some path"
    instance.get.return_value = "azure"

    result = runner.invoke(version)

    assert f"RelationalAI   {rai_version}" in result.output
    assert f"Rai-sdk        {railib_version}" in result.output
    assert f"Python         {python_version}" in result.output
    assert "App" not in result.output
    assert result.exit_code == 0

    # ---------------------------------------------------------------
    #  Error getting versions - Azure/Snowflake
    # ---------------------------------------------------------------

    with patch('relationalai.tools.cli.get_config', side_effect=Exception('Config Error')):
      result = runner.invoke(version)

    assert "Error checking app version: Config Error" in result.output
    assert result.exit_code == 1

    # ---------------------------------------------------------------
    #  Error getting app version - Snowflake specific
    # ---------------------------------------------------------------

    get_config = mocker.patch('relationalai.tools.cli.get_config')
    instance = get_config.return_value
    instance.file_path = "some path"
    instance.get.return_value = "snowflake"

    with patch('relationalai.tools.cli.get_resource_provider', side_effect=Exception('Provider Error')):
      result = runner.invoke(version)

    assert f"RelationalAI   {rai_version}" in result.output
    assert f"Rai-sdk        {railib_version}" in result.output
    assert f"Python         {python_version}" in result.output
    assert "App   Provider Error" in result.output
    assert result.exit_code == 0


