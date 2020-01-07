CREATE TABLE wattle.user        ('id', 'account','password','entity_id','created','modified','active') file='wattle/user.txt' delimiter=',';
CREATE TABLE wattle.location    ('id', 'name', 'designation','address1','address2','city','postalcode','state','country') file='wattle/locations.txt' delimiter=',';
CREATE TABLE wattle.entity      ('id', 'name', 'division','group','location','parent_id')  file='wattle/entity.txt' delimiter=',';
CREATE TABLE wattle.group       ('id', 'name', 'display', 'order', 'entity_id') file='wattle/group.txt' delimiter=',';
CREATE TABLE wattle.link        ('id', 'method_id', 'title', 'group_id') file='wattle/link.txt' delimiter=',';
CREATE TABLE wattle.methods     ('id', 'title', 'description', 'header', 'footer', 'theme', 'input_module' ,'display_module', 'auto_run') file='wattle/methods.txt' delimiter=',';
CREATE TABLE wattle.permissions ('id', 'type' , 'parent', 'child', 'deny') file='wattle/methods.txt' delimiter=',';







