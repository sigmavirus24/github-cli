from gh.base import Command, CustomOptionParser
from gh.util import tc, trim_numbers, sep, wrap


class PullsCommand(Command):
    name = 'pulls'
    usage = ('%prog [options] [user/repo] pulls [options] [number]'
             ' [sub-command]')
    summary = 'Interact with the Pull Requests API'
    fs = ('#{bold}{0.number}{default} {0.title:.36} - @{u.login}')
    subcommands = {
        '[#]num': 'Print full information about specified pull request',
        '[#]num comments': 'Print comments on specified pull request',
        '[#]num close': 'Close this pull request',
        '[#]num reopen': 'Re-open this pull request',
        '[#]num merge': 'Merge this pull request',
        '[#]num create [options]': 'Create a pull request from an issue',
        'create [options]': 'Create a brand new pull request',
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
                               default=-1,
                               nargs=1,
                               )

    def run(self, options, args):
        self.get_repo(options)

        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        if not args:
            return self.print_pulls(opts)

        args[0] = trim_numbers(args[0])

        if args[0].lower() == 'create':
            return self.create(args[1:])

        if not args[0].isdigit():
            return self.COMMAND_UNKNOWN

        status = self.COMMAND_UNKNOWN
        number = args.pop(0)

        subcmd = None
        if args:
            subcmd = args.pop(0).lower()

        if not subcmd:
            status = self.print_pull(number)
        elif subcmd == 'comments':
            status = self.print_comments(number)
        elif subcmd == 'close':
            status = self.close(number)
        elif subcmd == 'reopen':
            status = self.reopen(number)
        elif subcmd == 'merge':
            status = self.merge(number, args)

        return status

    def create(self, args):
        parser = CustomOptionParser()
        parser.set_usage('%prog [options] pulls create [options] base head')
        parser.add_option('-i', '--from-issue',
                          dest='issue',
                          help='Create the pull from issue provided',
                          type='int',
                          default=-1,
                          nargs=1,
                          )
        parser.add_option('-t', '--title',
                          dest='title',
                          help='Title for a new pull request',
                          type='str',
                          default='',
                          nargs=1,
                          )
        opts, args = parser.parse_args(args)

        if opts.help:
            parser.print_help()
            return self.SUCCESS

        if opts.issue < 1 and not (opts.title and len(args) >= 2):
            parser.error('Invalid create call')
            parser.print_help()
            return self.FAILURE

        self.login()
        if opts.issue >= 1:
            pr = self.repo.create_pull_from_issue(args[0], args[1])
        elif opts.title:
            pr = self.repo.create_pull(opts.title, args[0], args[1])

        if pr:
            return self.SUCCESS

        return self.FAILURE

    def format_short_pull(self, pull):
        return self.fs.format(pull, u=pull.user, bold=tc['bold'],
                              default=tc['default'])

    def get_pull(self, number, with_auth=False):
        pull = None
        if with_auth:
            self.login()
            owner, repo = str(self.repo).split('/')

        if with_auth:
            pull = self.gh.pull_request(owner, repo, number)
        else:
            pull = self.repo.pull_request(number)

        return pull

    def print_pull(self, number):
        pull = self.get_pull(number)
        if not pull:
            return self.FAILURE

        header = self.format_short_pull(pull)
        body = wrap(pull.body_text)
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

    def close(self, number):
        p = self.get_pull(number, True)
        if p and p.close():
            return self.SUCCESS
        return self.FAILURE

    def reopen(self, number):
        p = self.get_pull(number, True)
        if p and p.reopen():
            return self.SUCCESS
        return self.FAILURE

    def merge(self, number, args):
        p = self.get_pull(number, True)
        if p and p.merge(' '.join(args)):
            return self.SUCCESS
        return self.FAILURE


PullsCommand()
