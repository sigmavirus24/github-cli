from gh.base import Command


class GistCommand(Command):
    name = 'gist'
    usage = '%prog [options] gist gist_id'
    summary = 'Display the gist specified by gist_id'
    subcommands = {}

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        if not args:
            self.parser.error('You must provide a gist identifier')
            return self.FAILURE

        gist = self.gh.gist(args[0])
        if not gist:
            self.parser.error('Cound not retrieve gist:{0}'.format(gist))
            return self.FAILURE

        print('{0.html_url}: {0.description}'.format(gist))
        for f in gist.iter_files():
            print('{0.filename}\n{0.content}\n'.format(f))

        return self.SUCCESS


GistCommand()
