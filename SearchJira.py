from wox import Wox
import webbrowser
import json


class SearchJira(Wox):

    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    def generate_response(self, ticket_number, project):
        return {
            'Title': f"{ticket_number}",
            'SubTitle': f'Open: {ticket_number} in JIRA in your browser.',
            'IcoPath': 'Images/pic.png',
            'JsonRPCAction': {
                'method': 'action',
                'parameters': [f"https://{project['host']}/browse/{ticket_number}"],
                'dontHideAfterAction': False
            }
        }

    def find_project(self, ticket_prefix):
        workspaces = self.settings['jiraWorkspaces']

        if workspaces:
            workspace = [w for w in workspaces if ticket_prefix in w['keys']]
            if len(workspace) > 0:
                return workspace[0]
        return False

    def query(self, user_input):
        responses = []

        ticket_prefix = user_input.split('-')[0]
        project = self.find_project(ticket_prefix)

        # ToDo :: Update to actually search the JIRA API
        if not project:
            return [{
                'Title': f"No project found for: {user_input}",
                'SubTitle': f'Detected prefix: {ticket_prefix}',
                'IcoPath': 'Images/pic.png'
            }]

        responses.append(self.generate_response(user_input, project))

        return responses

    def action(self, url):
        webbrowser.open(url)

if __name__ == '__main__':
    SearchJira()

