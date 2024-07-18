#coding: utf8
from django.shortcuts import render, HttpResponse, redirect
import re

from repository import models


treeLevelBaseSpace = '1'


def printCurrentTree(treeNode, depth):
    print treeNode
    if treeNode.children:
        depth += 1
        for child in treeNode.children:
            print treeLevelBaseSpace * depth
            printCurrentTree( child, depth )


class MenuHelper( object ):

    def __init__(self, request, username):

        self.request = request

        self.username = username

        self.current_url = request.path_info

        self.permission2action_dict = None

        self.menu_leaf_list = None

        self.menu_list = None

        self.session_data()

    def session_data(self):
        permission_dict = self.request.session.get( 'permission_info' )
        if permission_dict:
            self.permission2action_dict = permission_dict['permission2action_dict']
            self.menu_leaf_list = permission_dict['menu_leaf_list']
            self.menu_list = permission_dict['menu_list']
        else:

            role_list = models.Role.objects.filter( user2role__user__username=self.username )

            permission2action_list = models.Permission2Action.objects. \
                filter( permission2action2role__role__in=role_list ). \
                values( 'permission__url', 'action__code' ).distinct()

            permission2action_dict = {}
            for item in permission2action_list:
                if item['permission__url'] in permission2action_dict:
                    permission2action_dict[item['permission__url']].append( item['action__code'] )
                else:
                    permission2action_dict[item['permission__url']] = [item['action__code'], ]

            menu_leaf_list = list( models.Permission2Action.objects. \
                                   filter( permission2action2role__role__in=role_list ).exclude( permission__menu__isnull=True ). \
                                   values( 'permission_id', 'permission__url', 'permission__caption', 'permission__menu' ).distinct() )

            menu_list = list( models.Menu.objects.values( 'id', 'caption', 'parentMenu' ) )

            self.request.session['permission_info'] = {
                'permission2action_dict': permission2action_dict,
                'menu_leaf_list': menu_leaf_list,
                'menu_list': menu_list,
            }

            # self.permission2action_list = permission2action_list
            # self.menu_leaf_list = menu_leaf_list
            # self.menu_list = menu_list

    def menu_data_list(self):

        menu_leaf_dict = {}
        open_leaf_parent_id = None

        for item in self.menu_leaf_list:
            item = {
                'id': item['permission_id'],
                'url': item['permission__url'],
                'caption': item['permission__caption'],
                'parent_id': item['permission__menu'],
                'child': [],
                'status': True,
                'open': False
            }
            if item['parent_id'] in menu_leaf_dict:
                menu_leaf_dict[item['parent_id']].append( item )
            else:
                menu_leaf_dict[item['parent_id']] = [item, ]

            if re.match( item['url'], self.current_url ):
                item['open'] = True
                open_leaf_parent_id = item['parent_id']

        menu_dict = {}
        for item in self.menu_list:
            item['child'] = []
            item['status'] = False
            item['open'] = False
            menu_dict[item['id']] = item

        for k, v in menu_leaf_dict.items():
            menu_dict[k]['child'] = v
            parent_id = k

            while parent_id:
                menu_dict[parent_id]['status'] = True
                parent_id = menu_dict[parent_id]['parentMenu']

        while open_leaf_parent_id:
            menu_dict[open_leaf_parent_id]['open'] = True
            open_leaf_parent_id = menu_dict[open_leaf_parent_id]['parentMenu']

        result = []
        for row in menu_dict.values():
            if not row['parentMenu']:
                result.append( row )
            else:
                menu_dict[row['parentMenu']]['child'].append( row )

        return result

    def menu_content(self, child_list):
        response = ""
        tpl = """
            <div class="item %s">
                <div class="title">%s</div>
                <div class="content">%s</div>
            </div>
        """
        for row in child_list:
            if not row['status']:
                continue
            active = ""
            if row['open']:
                active = "active"
            if 'url' in row:
                response += "<a class='%s' href='%s'>%s</a>" % (active, row['url'], row['caption'])
            else:
                title = row['caption']
                content = self.menu_content( row['child'] )
                response += tpl % (active, title, content)
        return response

    def menu_tree(self):
        response = ""
        tpl = """
        <div class="item %s">
            <div class="title">%s</div>
            <div class="content">%s</div>
        </div>
        """
        for row in self.menu_data_list():
            if not row['status']:
                continue
            active = ""
            if row['open']:
                active = "active"

            title = row['caption']

            content = self.menu_content( row['child'] )
            response += tpl % (active, title, content)
        return response

    def actions(self):

        action_list = []

        for k, v in self.permission2action_dict.items():
            if re.match( k, self.current_url ):
                action_list = v  # ['GET',POST,]
                break

        return action_list


def permission(func):
    def inner(request,*args,**kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return redirect('/login.html')
        obj = MenuHelper(request, user_info['username'])
        # action_list = obj.actions()
        # if not action_list:
        #     return HttpResponse('')
        kwargs['menu_string'] = obj.menu_tree()
        return func(request,*args,**kwargs)
    return inner