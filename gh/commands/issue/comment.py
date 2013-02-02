from gh.base import Command
from gh.util import get_issue_number


class IssueCommentCommand(Command):
    name = 'issue.comment'
    usage = '%prog [options] issue.comment [#]number'
    summary = 'Comment on a command'
    subcommands = {}

    def run(self, options, args):
        self.get_repo(options)

        opts, args = self.parser.parse_args(args)

        if opts.help:
            self.help()

        number = get_issue_number(
            args, self.parser, 'issue.comment requires a valid number'
        )

        if number is None:
            return self.FAILURE

        return self.comment_on(number)

    def comment_on(self, number):
        self.login()
        user, repo = self.repository
        issue = self.gh.issue(user, repo, number)

        name = ''
        status = self.SUCCESS

        # I need to handle this on Windows too somehow
        if not expandvars('$EDITOR'):
            print("$EDITOR not set")
            return self.FAILURE

        with mktmpfile('gh-issuecomment-') as fd:
            name = fd.name
            system('$EDITOR {0}'.format(fd.name))

        comment = issue.create_comment(open(name).read())
        if not comment:
            status = self.FAILURE
            print('Comment creation failed. Comment stored at {0}'.format(
                name))
        else:
            print('Comment created successfully.  {0}'.format(
                comment.html_url))
            rmtmpfile(name)

        return status


IssueCommentCommand()
