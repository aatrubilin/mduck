from unittest.mock import MagicMock, patch

from mduck.main.webhook import create_app, main


def test_create_app() -> None:
    """
    Test create_app function.

    GIVEN create_app function
    WHEN the app is created
    THEN it should include the healthcheck router
    """
    app = create_app()
    app_routes = [route.path for route in app.routes if hasattr(route, "path")]
    assert "/healthcheck" in app_routes


def test_main_function_runs_uvicorn_with_defaults() -> None:
    """
    Test main function with defaults.

    GIVEN the main function
    WHEN it is called with no arguments
    THEN it should run uvicorn with default arguments
    """
    with patch("argparse.ArgumentParser") as mock_parser:
        # Mock the argument parser to return default values
        mock_args = MagicMock()
        mock_args.host = "0.0.0.0"
        mock_args.port = 8000
        mock_args.reload = False
        mock_args.log_level = "info"
        mock_args.log_format = "human"
        mock_args.log_file = None
        mock_parser.return_value.parse_args.return_value = mock_args

        with patch("uvicorn.run") as mock_uvicorn_run:
            main()
            mock_uvicorn_run.assert_called_once_with(
                app="mduck.main.webhook:create_app",
                host="0.0.0.0",
                port=8000,
                reload=False,
                proxy_headers=True,
                log_config=None,
                factory=True,
            )


def test_main_function_runs_uvicorn_with_custom_args() -> None:
    """
    Test main function with custom args.

    GIVEN the main function
    WHEN it is called with custom arguments
    THEN it should run uvicorn with those custom arguments
    """
    with patch("argparse.ArgumentParser") as mock_parser:
        # Mock the argument parser to return custom values
        mock_args = MagicMock()
        mock_args.host = "127.0.0.1"
        mock_args.port = 8080
        mock_args.reload = True
        mock_args.log_level = "debug"
        mock_args.log_format = "human"
        mock_args.log_file = None
        mock_parser.return_value.parse_args.return_value = mock_args

        with patch("uvicorn.run") as mock_uvicorn_run:
            main()
            mock_uvicorn_run.assert_called_once_with(
                app="mduck.main.webhook:create_app",
                host="127.0.0.1",
                port=8080,
                reload=True,
                log_config=None,
                proxy_headers=True,
                factory=True,
                reload_dirs=["src"],
            )
