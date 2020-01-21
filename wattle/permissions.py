class permissions:
    account_id=0
    
    def __int__(self,account_id):
        self.account_id=account_id



    def get_group_membership_by_id(self,account_id):
        res=db.query("select group_id from wattle.group_membership where account_id=@account_id",{'@account_id':self.account_id})
        # no gorups
        groups={}
        if res.data_length>0:
            for row in res.data:
                group_id=row['data']['group_id'].strip()
                groups[group_id]={'id':group_id,'name':group_id,'display':'UNK','links':[],'ordinal':0}  
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
            res=db.query("select id,display,ordinal from wattle.group  {0} ".format(where_clause),parameters)
            if res.data_length>0:
                for row in res.data:
                    group_id=row['data']['id']
                    groups[group_id]['display']=row['data']['display']
                    groups[group_id]['ordinal']=row['data']['ordinal']
                return groups
        return None

    def get_components_by_list(method_list,entity):
        if method_list:
            methods={}
            methods_where=[]
            parameters={}
            for method in method_list:
                methods_where.append('id=@method_id_{0}'.format(method))
                parameters['@method_id_{0}'.format(method)]=method

            where_clause="where "+" or ".join(methods_where)
            res=db.query("select id,name,display,url from wattle.methods {0}".format(where_clause),parameters)
            if res.data_length!=0:
                for row in res.data:
                    method_id=row['data']['id']
                    display  =row['data']['display']
                    name     =row['data']['name']
                    url      =row['data']['url']
                    if entity:
                        entity_display=entity['display']
                        entity_name=entity['name']
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



        permissions
        r,w,x,a

        