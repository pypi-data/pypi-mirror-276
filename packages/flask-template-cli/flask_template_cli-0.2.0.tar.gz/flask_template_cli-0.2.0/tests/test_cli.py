from unittest.mock import patch

from flask_template_cli import cli


def test_primary_questions_returns_correct_values():
    with patch('flask_template_cli.cli.prompt',
               return_value={'name': 'test', 'project_type': 'api', 'need_database': False, 'need_auth': False}):
        result = cli._primary_questions()
        assert result == {'name': 'test', 'project_type': 'api', 'need_database': False, 'need_auth': False}


def test_user_database_choice_returns_correct_values():
    with patch('flask_template_cli.cli.prompt',
               side_effect=[{'database_type': 'SQL'}, {'database_engine': 'Postgres'}]):
        result = cli._user_database_choice()
        assert result == {'database_type': 'SQL', 'database_engine': 'Postgres'}


def test_create_project_structure_creates_directories():
    project = cli.Project()
    project.name = 'test'
    project.project_type = 'api'
    project.need_database = False
    with patch('os.makedirs') as mock_makedirs:
        cli.create_project_structure(project)
        assert mock_makedirs.call_count == 4


def test_start_building_calls_functions():
    project = cli.Project()
    with patch('flask_template_cli.cli.create_project_structure') as mock_create_project_structure, \
            patch('flask_template_cli.cli.init_gen') as mock_init_gen, \
            patch('flask_template_cli.cli.routes_gen') as mock_routes_gen, \
            patch('flask_template_cli.cli.generate_models') as mock_generate_models, \
            patch('flask_template_cli.cli.req_txt_gen') as mock_req_txt_gen:
        cli._start_building(project)
        mock_create_project_structure.assert_called_once_with(project)
        mock_init_gen.assert_called_once_with(project)
        mock_routes_gen.assert_called_once_with(project)
        mock_generate_models.assert_called_once_with(project)
        mock_req_txt_gen.assert_called_once_with(project)


def test_install_dependencies_runs_pip_install():
    project = cli.Project()
    project.name = 'test'
    with patch('flask_template_cli.cli.prompt', return_value={'install_dependencies': True}), \
            patch('os.system') as mock_system:
        cli._install_dependencies(project)
        mock_system.assert_called_once_with('cd test && pip install -r requirements.txt')


def test_main_creates_project():
    with patch('flask_template_cli.cli._primary_questions',
               return_value={'name': 'test', 'project_type': 'api', 'need_database': False, 'need_auth': False}), \
            patch('flask_template_cli.cli._start_building'), \
            patch('flask_template_cli.cli._install_dependencies'), \
            patch('typer.echo'):
        cli.main()
