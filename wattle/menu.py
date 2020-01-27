from . import db 

def get_group_membership_by_id(account_id):
    res=db.query("select group_id from wattle.group_membership where account_id=@account_id",{'@account_id':account_id})
    # no gorups
    #res.debug()
    groups={}
    if res.data_length>0:
        for row in res.data:
            group_id=row.group_id.strip()
            groups[group_id]={'id':group_id,'type':'menu','name':group_id,'display':'UNK','links':[],'ordinal':0}  
        return groups

    return None

def get_groups_by_list(groups):
    # OK we have the groups... now pull the links
    if groups and len(groups)>0:
        group_where=[]
        parameters={}
        for group in groups:
            group_id=groups[group]['id']
            group_where.append('id=@group_id_{0}'.format(group_id))
            parameters['@group_id_{0}'.format(group_id)]=group_id

        where_clause="where "+" or ".join(group_where)
        res=db.query("select id,display,ordinal from wattle.group  {0} ".format(where_clause),parameters)
        if res.data_length>0:
            for row in res.data:
                group_id=row.id
                groups[group_id]['display']=row.display
                groups[group_id]['ordinal']=row.ordinal
            return groups
    return None

def get_methods_by_list(method_list,entity):
    if method_list:
        methods={}
        methods_where=[]
        parameters={}
        for method in method_list:
            methods_where.append('id=@method_id_{0}'.format(method))
            parameters['@method_id_{0}'.format(method)]=method

        where_clause="where "+" or ".join(methods_where)
        res=db.query("select id,name,display,url from wattle.methods {0}".format(where_clause),parameters)
        #res.debug()
        if res.data_length!=0:
            for row in res.data:
                method_id=row.id
                display  =row.display
                name     =row.name
                url      =row.url
                if entity:
                    entity_display=entity.display
                    entity_name=entity.name
                else :
                    entity_display=''
                    entity_name=''
                url=url.replace("{{ entity_display }}",str(entity_display))
                url=url.replace("{{ entity_name }}",str(entity_name))
                url=url.replace("{{ method_display }}",display)
                url=url.replace("{{ method_name }}",name)
                url="/m/"+url
                methods[method_id]={'method_id':method_id,'display':display,'name':name,'url':url}
            return methods
    return None

def get_links_by_group_list(groups,entity):
    # OK we have the groups... now pull the links
    group_membership_where=[]
    parameters={}
    if groups and len(groups)>0:
        for group in groups:
            group_id=groups[group]['id']
            group_membership_where.append('group_id=@group_id_{0}'.format(group_id))
            parameters['@group_id_{0}'.format(group_id)]=group_id

            where_clause="where "+" or ".join(group_membership_where)
            res=db.query("select id,display,method_id,group_id,ordinal from wattle.link {0} ".format(where_clause),parameters)
            #res.debug()
            if res.data_length>0:
                methods={}
                for row in res.data:
                    methods[row.method_id]=row.method_id
                methods=get_methods_by_list(methods,entity)
                for row in res.data:
                    link_id     =row.id
                    group_id    =row.group_id
                    method_id   =row.method_id
                    link_display=row.display
                    ordinal     =row.ordinal
                    # maybe the method doesnt exist?
                    if methods==None or  method_id not in methods:
                        method_url  ="BOB"
                    else:
                        method_url  =methods[method_id]['url']
                    groups[group_id]['links'].append({'type':'link','display':link_display,'id':link_id,'method_id':method_id,'group_id':group_id,'url':method_url,'ordinal':ordinal})

                return groups
    return None

def sort_groups(groups):
    # Sort the mess by menu ordinal, then link ordinal
    if groups:
        group2=[]
        for group in groups:
            group2.append(groups[group])

        group2=sorted(group2, key=lambda group: int(group['ordinal']))
        for group in group2:
            group['links']=sorted(group['links'],key=lambda link: int(link['ordinal']))

        return group2
    
    return None


def menu(account_id,entity):
    groups=get_group_membership_by_id(account_id)
    groups=get_groups_by_list(groups)
    #print(groups)
    groups=get_links_by_group_list(groups,entity)
    groups=sort_groups(groups)
    return groups    