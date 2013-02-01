from gh.base import Command


class ForkGistCommand(Command):
    name = 'fork.gist'
    usage = '%prog [options] fork.gist [options] login/repo'
    summary = 'Fork a gist'
    subcommands = {}

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)
        self.login()

        if opts.help:
            self.help()

        if not args:
            self.parser.error('You must provide a gist id')
            return self.FAILURE

        g = self.gh.gist(args[0])
        if not g:
            self.parser.error('Could not retrieve gist: {0}'.format(args[0]))
            return self.FAILURE

        fork = g.fork()
        if not fork:
            self.parser.error('Cound not fork gist: {0}'.format(g))
            return self.FAILURE

        print('git clone {0}'.format(fork.git_push_url))
        print(fork.html_url)
        return self.SUCCESS


ForkGistCommand()
