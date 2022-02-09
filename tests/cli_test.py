from click.testing import CliRunner

import gitsearch

def test_command_exists():
    runner = CliRunner()
    result = runner.invoke(gitsearch.searcher, ['--help'])

    commands = ['-r, --reponame TEXT', '-s, --sort TEXT', '-i, --ignore TEXT']

    for command in commands:
        assert command in result.output
    
def test_commands():
    commands = [
        ['-r', 'test'],
        ['-r', 'test', '-s', 'asc'],
        ['-r', 'test', '-s', 'desc'],
        ['-r', 'test', '-i', 'test'],
        ['-r', 'test', '-i', 'test', '-s', 'asc'],
        ['-r', 'test', '-i', 'test', '-s', 'desc'],
        ['-r', 'test', '-i', 'test', '-s', 'asc', '-s', 'desc'],
        ['-r', 'test', '-i', 'test', '-s', 'desc', '-s', 'asc'],
    ]

    runner = CliRunner()
    for command in commands:
        result = runner.invoke(gitsearch.searcher, command)
        print("Command {} exit code {}".format(command[0], result.exit_code))
        assert result.exit_code == 0 

if __name__ == '__main__':
    test_command_exists()
    # test_commands() # Works, but because of the API call takes so much time to execute 
