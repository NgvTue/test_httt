

import logging
init_context={
    'db':{'cầu thủ':None, 'previous_intent':None},
    'history':[],
    'user_input':'',
    'verbose':1,
    'follow_node':None
}
context_user={
    -1:init_context
}
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from web_service.auth import login_required
from web_service.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from src.graph import PathGraph, Node, Graph
from src.model import predict
from src.infer import NaiveBayesNode
import copy
bp = Blueprint('chat', __name__)





@bp.route('/',methods=['GET', 'POST'])
def index():
    db = get_db()
    if  request.method == 'GET':
        user_id = session.get('user_id',-1) # get user
        context_user[user_id] = copy.deepcopy(init_context)
        context = copy.deepcopy(context_user.get(user_id,copy.deepcopy(init_context))) # get context
        logging.info(context)
        
        return render_template('chat/main.html', context=context)
    elif request.method == 'POST':
        user_input  =request.form['msg']
        user_id = session.get('user_id',-1) # get user

        if user_input == 'f5':
            context_user[user_id] = init_context
            return {}
        context = context_user.get(user_id,init_context) # get context
        context['user_input'] = user_input

        logging.info(request.form)


        # if request.form.get("is_option","false") in "true":

        #     # user_input = [i.strip() for i in user_input.replace("<br>","\n").replace("  "," ").split("\n")]

        #     list_option = request.form.get("list_option")
        #     a = list_option
        #     list_option = [i.strip().replace("<br>","\n") for i in list_option.replace("\n\n","\n").replace("  "," ").split("\n")]
        #     def compare(a,b):
        #         if len(a) <= 1:return False
        #         return a in b
        #     print(list_option)
        #     true_ = [compare(user_input, i) for i in list_option ]
        #     logging.info(true_)
        #     true_ = sum(true_)
        #     if true_ == 0:
        #         context.pop("follow_node",None)
        #         context['answer']= "Vui lòng chọn đúng yêu cầu!"
        #         return jsonify({'context':context,'is_option':True,'list_option':a})
            
        #     print(list_option)
        #     logging.info(context['follow_node'])
        #     logging.info(context['user_input'])            

        
        first_node  = NaiveBayesNode('first_node_naive_bayes', )
        context = first_node.excute(context)
        context_user[user_id] = copy.deepcopy(context)
        answer = context.get("answer")
        context.pop("follow_node",None)
        print(answer)
        is_option = "option" in answer.lower()
        if is_option:
            list_option = answer.split("Option")[-1].split("\n")
            # answer = answer.split("Option")[0]
            print(list_option,"dsadsa")
            context['answer'] = answer.replace("\n","<br>")
            return jsonify({'context':context,'is_option':True,'list_option':list_option})
        else:
            context['answer'] = answer.replace("\n","<br>")
            return jsonify({'context':context,'is_option':False,'list_option':[]})
            # return render_template('chat/main.html', context=context)
