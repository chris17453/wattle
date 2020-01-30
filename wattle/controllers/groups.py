from . import db


def get_group_membership_by_account_id(account_id):
    res=db.query("select group_id from wattle.group_membership where account_id=@account_id",{'@account_id':account_id})
    # no groups
    #res.debug()
    groups={}
    if res.data_length>0:
        for row in res.data:
            group_id=row.group_id.strip()
            groups[group_id]=group_id
        return groups
    return None

# returns a list or records with id,display,ordinal
def get_user_groups_by_account_id(account_id):
    # OK we have the groups... now pull the links
    groups=get_group_membership_by_account_id(account_id)
    if groups and len(groups)>0:
        group_where=[]
        parameters={}
        for group in groups:
            # prevents duplicates
            group_id=groups[group]
            group_where.append('id=@group_id_{0}'.format(group_id))
            parameters['@group_id_{0}'.format(group_id)]=group_id

        where_clause="where "+" or ".join(group_where)
        res=db.query("select id,display,ordinal from wattle.group  {0} ".format(where_clause),parameters)
        if res.data_length>0:
            return res.data
    return None