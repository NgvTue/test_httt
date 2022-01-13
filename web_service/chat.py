

import logging
init_context={
    'db':{'cầu thủ':None, 'previous_intent':None, 'previous_rule':None},
    'history':[],
    'user_input':'Cho mình thông tin luật sân bóng và việt vị nào?',
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
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
bp = Blueprint('chat', __name__)





@bp.route('/')
def index():
    db = get_db()
    if  request.method == 'GET':
        user_id = session.get('user_id',-1) # get user
        context = context_user.get(user_id,init_context) # get context
        logging.info(context)
    
        return render_template('chat/main.html', context=context)
    elif request.method == 'POST':
        print(request.__dict__)