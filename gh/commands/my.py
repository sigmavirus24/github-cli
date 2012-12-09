from gh.base import Command


class MyCommand(Command):
    name = 'my'
    usage = '%prog [options] my [options] [sub-command]'
    summary = 'Access to authorized user content'
    subcommands = {
        'dashboard': 'Print your received events',
        'issues': 'Print your issues',
        'notifications': 'Print your notifications',
        'pulls': 'Print your pull requests',
        'stars': 'Print your stars',
    }
    event_fs = '{date} {by} {event}'

    def __init__(self):
        super(MyCommand, self).__init__()
        self.parser.add_option('-n', '--number',
                               dest='number',
                               help='Number of items to print at most',
                               type='int',
                               default=20,
                               nargs=1,
                               )

    def _event_handler(self, event):
        if event.type == 'CommitCommentEvent':
            return 'commented on commit {1}/{2}#{0:.8}'.format(
                event.payload['comment'].commit_id,
                *event.repo
            )

        if event.type == 'CreateEvent':
            s = 'created a new {0}'.format(event.payload['ref_type'])
            if event.payload['ref_type'] in ('branch', 'tag'):
                s = ' '.join([s, event.payload['ref']])
            else:
                s = ' '.join([s, event.repo[0], event.repo[1]])
            return s

        if event.type == 'DeleteEvent':
            return 'deleted {0} {1:.8} from {2}/{3}'.format(
                event.payload['ref_type'], event.payload['ref'],
                *event.repo
            )

        if event.type == 'DownloadEvent':
            return 'created download {0} on {1}/{2}'.format(
                event.payload['download'].name, *event.repo
            )

        if event.type == 'FollowEvent':
            return 'followed {0}'.format(event.payload['target'].login)

        if event.type == 'ForkEvent':
            return 'forked {1}/{2} to {0}'.format(
                event.payload['forkee'],
                *event.repo
            )

        # ForkApplyEvent ???

        if event.type == 'GistEvent':
            return '{0}d {1}'.format(
                event.payload['action'], event.payload['gist'].id
            )

        if event.type == 'GollumEvent':
            return 'edited some wiki pages'

        if event.type == 'IssueCommentEvent':
            return 'commented on {1}/{2}#{0}'.format(
                event.payload['issue'].number,
                *event.payload['issue'].repository
            )

        if event.type == 'IssuesEvent':
            return '{0} issue {1} on {2}/{3}'.format(
                event.payload['action'],
                event.payload['issue'].number,
                *event.repo
            )

        if event.type == 'MemberEvent':
            return '{0} added {1} as a collaborator on {2}/{3}'.format(
                event.payload['action'],
                event.payload['user'].login,
                *event.repo
            )

        if event.type == 'PublicEvent':
            return 'open sourced {0}/{2}'.format(*event.repo)

        if event.type == 'PullRequestEvent':
            return '{0} pull request #{1} on {2}/{3}'.format(
                event.payload['action'],
                event.payload['pull_request'].number,
                *event.repo
            )

        # PullRequestReviewCommentEvent

        if event.type == 'PushEvent':
            commits = 'commits' if event.payload['size'] > 1 else 'commit'
            return 'pushed {0} {1} to {1} on {2}/{3}'.format(
                event.payload['size'], commits,
                event.payload['ref'], *event.repo
            )

        if event.type == 'TeamAddEvent':
            return 'added {0} to {1}'.format(
                event.payload['user'] or event.payload['repository'],
                event.payload['repo']
            )

        if event.type == 'WatchEvent':
            return '{0} {1}/{2}'.format(event.payload['action'], *event.repo)

    def run(self, options, args):
        self.opts, args = self.parser.parse_args(args)

        if not args:
            self.parser.error('No command given.')
            return self.FAILURE

        self.login()

        cmd = args.pop(0)
        status = self.SUCCESS

        if cmd == 'dashboard':
            status = self.dashboard()

        return status

    def dashboard(self):
        u = self.gh.user()

        for e in u.iter_received_events(number=self.opts.number):
            event = {
                'date': e.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'by': e.actor.login,
                'event': self._event_handler(e)
            }
            print(self.event_fs.format(**event))

        return self.SUCCESS


MyCommand()
