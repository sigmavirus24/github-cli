from gh.base import Command
from gh.util import tc, trim_numbers, sep, wrap
from github3 import GitHubError


class PullsCommand(Command):
    name = 'pulls'
    usage = ('%prog [options] [user/repo] pulls [options] [number]'
            ' [sub-command]')
    summary = 'Interact with the Pull Requests API'
    fs = ('#{bold}{0.number}{default} {0.title:.36} - @{u.login}')
    subcommands = {
            '[#]num': 'Print full information about specified pull request',
            '[#]num comments': 'Print comments on specified pull request',
            }

    def __init__(self):
        super(PullsCommand, self).__init__()
        self.parser.add_option('-s', '--state',
                dest='state',
                help='State of the pull request.',
                choices=('open', 'closed'),
                default='open',
                nargs=1,
                )
        self.parser.add_option('-n', '--number',
                dest='number',
                help='Number of pulls to list',
                type='int',
                nargs=1,
                default=-1,
                )

    def run(self, options, args):
        self.get_repo(options)

        opts, args = self.parser.parse_args(args)

        if not args:
            return self.print_pulls(opts)

        args[0] = trim_numbers(args[0])

        if not args[0].isdigit():
            return self.COMMAND_UNKNOWN

        status = self.SUCCESS
        number = args.pop(0)

        subcmd = None
        if args:
            subcmd = args.pop(0).lower()

        if not subcmd:
            status = self.print_pull(number)
        elif subcmd == 'comments':
            status = self.print_comments(number)

        return status

    def format_short_pull(self, pull):
        return self.fs.format(pull, u=pull.user, bold=tc['bold'],
                default=tc['default'])

    def get_pull(self, number):
        pull = None
        try:
            pull = self.repo.pull_request(number)
        except GitHubError as ghe:
            if ghe.code == 404:
                print("There is no pull request #{0} on {1}/{2}.".format(
                    number, *self.repository))
            raise ghe
        return pull

    def print_pull(self, number):
        pull = self.get_pull(number)
        if not pull:
            return self.FAILURE

        header = self.format_short_pull(pull)
        body = '\n'.join(wrap(pull.body_text))
        print('{0}\n{1}\n{2}\n'.format(header, sep, body))
        print('{0}Files modified:{1}'.format(tc['underline'], tc['default']))
        self.print_files(pull)
        return self.SUCCESS

    def print_pulls(self, opts):
        for p in self.repo.iter_pulls(opts.state, opts.number):
            print(self.format_short_pull(p))
            self.print_files(p)
        return self.SUCCESS

    def print_files(self, pull):
        for f in pull.iter_files():
            print('  {0}: +{1}/-{2}'.format(f.filename, f.additions,
                f.deletions))

    def print_comments(self, number):
        pull = self.get_pull(number)
        if not pull:
            return self.FAILURE

        for c in pull.iter_comments():
            fs = '@{uline}{u.login}{default} -- {date}\n{body}\n'
            body = '\n'.join(wrap(c.body_text))
            date = c.created_at.strftime('%Y-%m-%d %H:%M:%S')
            print(fs.format(u=c.user, date=date, body=body,
                uline=tc['underline'], default=tc['default']))

        return self.SUCCESS

PullsCommand()
