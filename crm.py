
class Crm:
    # queryByResolved = "None"
    # queryByClosed = "None"
    # queryByVerified = "None"
    # queryAll = "None"
    # crmList = "None"
    # id = "None"
    def create_Name_For_Jql(self, name):
        self.name = str(name).replace("[arh+]", "").replace("[", " ").replace("]", " ").replace("-", " ").replace(":", " ")
        return self.name

    def set_Query_By_Name(self, name):
        self.name = name
        self.queryByResolved    = str('project=HL and status=Resolved and type="IT: Helpline Incident" and text ~ \"' + str(self.name ) + "\"")
        self.queryByClosed  = str('project=HL and status=Closed and type="IT: Helpline Incident" and text ~ \"' + str(self.name ) + "\"")
        self.queryByVerified = str('project=HL and status=VERIFIED and type="IT: Helpline Incident" and text ~ \"' + str(self.name ) + "\"" + " ORDER BY created DESC")
        self.queryAll = str(self.queryByResolved) + " or " + str(self.queryByClosed) + " or " + str(self.queryByVerified)

    def set_Query_By_Email(self, email):
        self.email = email
        self.queryAll = str('project=CRM and status="Active" and email~"'+str(self.email)+'"')

    def search_Crm_In_Jira(self, queryAll, jira):
        self.crmList = jira.search_issues(queryAll, maxResults=1)
        if len(self.crmList) == 1:
            for crm in self.crmList:
                try:
                    return crm.fields.customfield_11256
                except AttributeError:
                    return crm.key
        else:
            return 0

    def display_Query_All(self):
        print(self.queryAll)