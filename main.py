from jira import JIRA
import requests
from requests.auth import HTTPBasicAuth

from helpline import Helpline
from crm import Crm


def login():
    login = 'xxx'
    password = 'xxx'
    auth = (login, password)
    return auth

def get_Jira(auth, jiraUrl):
    jira = JIRA(options=jiraUrl, basic_auth=(auth))
    return jira

def get_New_Helpline_Id_From_Jira(newHlsIdsList, jql_Query_New_Helpline, jira):
    searchNewHlList = jira.search_issues(jql_Query_New_Helpline)
    for hl in searchNewHlList:
        newHlsIdsList.append(hl.id)
    return newHlsIdsList
#Adress
jiraUrl = {'server': 'xxx'}
jira = get_Jira(login(), jiraUrl)

#Create list for Hls Ids
newHlsIdsList = []
#Create list for hl object
hlObjectToAcceptList = []
hlObjectFailList = []
#Query for new Ids
jql_Query_New_Helpline = 'project=HL and status="New"'
# jql_Query_IIline_Helpline = 'project=HL and status="II Line"'

#Get New Hl Ids List
get_New_Helpline_Id_From_Jira(newHlsIdsList, jql_Query_New_Helpline, jira)
print("| OK | New HLs Id list: "+str(newHlsIdsList))
if len(newHlsIdsList) == 0:
    print("| SYS | Found -> " + str(len(newHlsIdsList)) + " new Hls is Jira")
else:
    print("| SYS | Found -> " + str(len(newHlsIdsList)) + " new Hls is Jira")
    for newHlId in newHlsIdsList:
        new_helpline = Helpline(newHlId)
        new_helpline.set_Data(jira)
        #Print
        print("========================================================")
        new_helpline.display_Name()
        new_helpline.display_Email()
        # new_helpline.display_Group_Id()
        if new_helpline.check_Hl_Is_From_Partner() == True:
            print("| SYS | Task from Partner")
            crm = Crm()
            crm.set_Query_By_Email(new_helpline.email)
            crmKey = crm.search_Crm_In_Jira(crm.queryAll, jira)
            if crmKey == 0:
                "| ERROR | Not Found CRM"
            else:
                new_helpline.set_Crm(crmKey)
        else:
            print("| SYS | Task from Inside Office")
            crm = Crm()
            crm.set_Query_By_Name(crm.create_Name_For_Jql(new_helpline.name))
            crmKey = crm.search_Crm_In_Jira(crm.queryAll, jira)
            if crmKey == 0:
                print("| ERROR | Not Found CRM")
                hlObjectFailList.append(new_helpline)
            else:
                new_helpline.set_Crm(crmKey)
                hlObjectToAcceptList.append(new_helpline)
        print("========================================================")
    print("| OK | New " + str(len(hlObjectToAcceptList)) + " hl to accept object list -> " + str(hlObjectToAcceptList))
    print("| ERROR| New " + str(len(hlObjectFailList)) + " hl with ERROR object list -> " + str(hlObjectFailList))
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

    urlPost = 'xxx'
    for hl in hlObjectToAcceptList:
        post = hl.accept_Hl(urlPost)
        print(post.text)