from jira import JIRA
import requests
from requests.auth import HTTPBasicAuth

class Helpline():
    # groupId = 3
    # # name = "None"
    # crm = "None"
    # email = "None"
    # priority = "None"

    def __init__(self, id):
        self.id     = id

    def set_Data(self, jira):
        hl = jira.issue(self.id)
        self.name = str(hl.fields.customfield_12902)
        self.email = hl.fields.customfield_11208
        if self.name == "None":
            self.name = str(hl.fields.summary)
        self.groupId = self.get_Email_Group_Id(self.email)

    def check_Hl_Is_From_Partner(self):
        if self.groupId == 0:
            return True
        else:
            return False

    def get_Email_Group_Id(self, email):
        self.email = email
        if self.email == "arhplus@avantis.pl":
            return 1
        elif self.email == "orion@mail.avantis.pl":
            return 2
        elif (self.email == "None") or (not self.email):
            return 3
        elif self.email == "notify@notify.dotcom-monitor.com":
            return 4
        else:
            return 0

    def set_Crm(self, crm):
        self.crm = crm
        print("Crm -> " + str(crm))

    def display_Name(self):
        print("Name -> "+ self.name)

    def display_Group_Id(self):
        print("GroupId -> "+str(self.groupId))

    def display_Email(self):
        print("Email -> "+str(self.email))

    def accept_Hl(self, url):
        self.url = url
        self.data = {'id': self.id, 'customfield_11256': self.crm, 'customfield_11213': '10916', 'priority': '4', 'customfield_10906': '10723', 'action': '11'}
        cookie = {'atlassian.xsrf.token': 'BJRJ-VNI7-LB9Z-CMCM|8bfa8cac52245131ba165a1e35df9b7b07f4ff38|lin'}
        request = requests.post(self.url, data=self.data, auth=("xxx", 'xxx'), cookies=cookie)
        return request