from gh.base import Command

class GistStarCommand(Command):
    name = 'gist.star'
    usage = '%prog [options] gist.star gist_id'
    summary = 'Star the gist specified by gist_id'
    subcommands = {}

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        if not args:
            self.parser.error('You must provide a gist identifier')
            return self.FAILURE

        self.login()

        gist = self.gh.gist(args[0])
        if not gist:
            self.parser.error('Cound not retrieve gist:{0}'.format(args[0]))
            return self.FAILURE

        if gist.is_starred():
            print("{0.html_url} is already starred.".format(gist))
            return self.SUCCESS

        if gist.star():
            print("Starred:")
            print('{0.html_url}: {0.description}'.format(gist))
            return self.SUCCESS
        else:
            print("Failed to star.")
            return self.FAILURE

GistStarCommand()
