import pymel.core as pm
import json
from cwmaya.lib import connections
from cwmaya.lib import const as k
from cwmaya.lib import window_utils
from ciocore import data as coredata


class SubmissionMenuGroup(object):

    def __init__(self, dialog):
        """
        Initialize the TemplatesMenuGroup with a dialog and set up the initial
        menu structure.

        Args:
            dialog: The PyMel UI dialog to which this menu will be attached.
        """
        self.dialog = dialog
        pm.setParent(dialog.menuBarLayout)
        self.menu = pm.menu(label="Submissions", tearOff=True)

        pm.menuItem(label="Show submission", command=pm.Callback(self.on_show_submission))

        # self.create_desktop_app_menu()
        # self.create_workflow_api_menu()

    def on_show_submission(self):
 
        node = self.dialog.node
        if not node:
            print("No node found")
            return
        payload = node.attr("output").get()
        payload = json.loads(payload)
        # print(payload)
        account_id = coredata.data()["account"]["account_id"]
        token = coredata.data()["account"]["token"]
        
        url = k.WORKFLOW_URLS["ACCOUNTS"]
        url = f"{url}/{account_id}/workflows"
        headers = {"Content-Type": "application/json"}
        
        data = {
            "request_data": {
                "headers": headers,
                "url": url,
                "token": token,
                "node": node.name()
            },
            "payload": payload
        }
        window_utils.show_data_in_window(data, title="Submission preview")

def create(dialog):
    return SubmissionMenuGroup(dialog)


