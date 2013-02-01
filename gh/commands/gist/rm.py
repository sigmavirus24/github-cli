from gh.base import Command


class GistRmCommand(Command):
    name = 'gist.rm'
    usage = '%prog [options] gist.rm gist_id'
    summary = 'Delete a gist'
    subcommands = {}

    def run(self, options, args):
        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        if not args:
            self.parser.error('You must provide a valid gist_id')
            return self.FAILURE

        self.login()

        gist = self.gh.gist(args[0])
        if not gist:
            self.parser.error('Could not retrieve gist:{0}'.format(gist))
            return self.FAILURE

        if gist.delete():
            print('Successfully deleted gist:{0}'.format(gist))
            return self.SUCCESS

        print('Gist:{0} could not be deleted. You may not have the permissions'
              ' to do this'.format(gist))
        return self.FAILURE


GistRmCommand()
