from gh.base import Command
from gh.util import tc


class MyCommand(Command):
    name = 'my'
    usage = '%prog [options] my [options] [sub-command]'
    summary = 'Access to authorized user content'
    subcommands = {
        'dashboard': 'Print your received events',
        'issues': 'Print your issues',
        'notifications': 'Print your notifications',
        'stars': 'Print your stars',
    }
    issue_fs = '#{0[bold]}{num}{0[default]} {title:.36} - ({repo})'
    event_fs = '{date} {0[bold]}{by}{0[default]} {event}'
    thread_fs = ('{updated} [{0[bold]}{type}{0[default]}] {subject:.36} '
                 '({repo})')

    def __init__(self):
        super(MyCommand, self).__init__()
        add = self.parser.add_option
        add('-n', '--number',
            dest='number',
            help='Number of items to print at most',
            type='int',
            default=20,
            nargs=1,
            )
        add('-f', '--filter',
            dest='filter',
            help='How to filter your issues',
            choices=('assigned', 'created', 'mentioned', 'subscribed'),
            nargs=1,
            )
        add('-s', '--state',
            dest='state',
            help='State of the issues',
            choices=('open', 'closed'),
            nargs=1,
            )
        add('-l', '--labels',
            dest='labels',
            help='Comma-separated list of labels',
            type='str',
            nargs=1,
            )
        add('-d', '--direction',
            dest='direction',
            help='Direction to display the issues',
            choices=('asc', 'desc'),
            nargs=1,
            )
        add('-S', '--since',
            dest='since',
            help='ISO 8601 formatted date to cut off issues',
            type='str',
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
            return 'pushed {0} {1} to {2} on {3}/{4}'.format(
                event.payload['size'], commits,
                event.payload['ref'], *event.repo
            )

        if event.type == 'TeamAddEvent':
            return 'added {0} to {1}'.format(
                event.payload['user'] or event.payload['repository'],
                event.payload['repo']
            )

        if event.type == 'WatchEvent':
            return 'starred {0}/{1}'.format(*event.repo)

    def run(self, options, args):
        self.opts, args = self.parser.parse_args(args)

        if self.opts.help:
            self.help()

        if not args:
            self.parser.error('No command given.')
            return self.FAILURE

        self.login()

        cmd = args.pop(0)
        status = self.COMMAND_UNKNOWN

        if cmd == 'dashboard':
            status = self.dashboard()
        elif cmd == 'notifications':
            status = self.notifications()
        elif cmd == 'issues':
            status = self.issues()
        elif cmd == 'stars':
            status = self.stars()
        elif cmd == 'profile':
            status = self.profile()

        return status

    def dashboard(self):
        u = self.gh.user()

        for e in u.iter_received_events(number=self.opts.number):
            event = {
                'date': e.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'by': e.actor.login,
                'event': self._event_handler(e)
            }
            print(self.event_fs.format(tc, **event))

        return self.SUCCESS

    def notifications(self):
        for n in self.gh.iter_notifications(number=self.opts.number):
            thread = {
                'updated': n.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'repo': n.repository,
                'subject': n.subject['title'],
                'type': n.subject['type'],
            }
            print(self.thread_fs.format(tc, **thread))

        return self.SUCCESS

    def issues(self):
        o = self.opts
        for i in self.gh.iter_issues(o.filter, o.state, o.labels, o.sort,
                                     o.direction, o.since, o.number):
            issue = {
                'num': i.number,
                'title': i.title,
                'repo': '/'.join(i.repository),
            }
            print(self.issue_fs.format(tc, **issue))

        return self.SUCCESS

    def profile(self):
        u = self.gh.user()
        print('{0[bold]}{1} -- {1.name}{0[default]}'.format(tc, u))
        print('  Joined: {0}'.format(u.created_at.strftime('%Y-%m-%d')))
        print('  email: {0}'.format(u.email))
        print('  Followers: {0}'.format(u.followers))
        print('  Following: {0}'.format(u.following))
        print('  Public repos: {0}'.format(u.public_repos))
        print('  Public gists: {0}'.format(u.public_gists))

        if u.blog:
            print('  Website: {0}'.format(u.blog))

        if u.owned_private_repos > 0:
            print('  Owned private repos: {0}'.format(u.owned_private_repos))

        if u.total_private_repos > 0:
            print('  Total private repos: {0}'.format(u.total_private_repos))

        if u.total_private_gists > 0:
            print('  Total private gists: {0}'.format(u.total.private_gists))

        if u.hireable:
            print('  For hire')

        return self.SUCCESS

    def stars(self):
        for r in self.gh.iter_starred(number=self.opts.number):
            print('{0}'.format(r))

        return self.SUCCESS


MyCommand()
