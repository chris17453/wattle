from . import db


def get_task_choices_by_account_id(id):
    query="select id,display from wattle.task"
    res=db.query(query);
    #print(res.data)
    choices=[]
    choices.append( (0,"None") )
    if res.data_length!=0:

        for task in res.data:
            choices.append( (task['data']['id'],task['data']['display']) )
    return choices


def get_tasks_by_account_id(account_id):
    query="select id,display,name from wattle.task"
    res=db.query(query);
    if res.data_length!=0:
        return res.data
    return None