from src.graph import PathGraph, Node, Graph
from src.model import predict
import time
import logging
import json
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)


class NaiveBayesNode(Node):
    
    def excute(self, context):
        history = context.get("history",[])
        user_inputs = context.get("user_input","")
        # naive bayess
        value = predict(user_inputs)[0]
        logging.info(f"Naive Bayess step return {value}")

        if value.get('p') < 0.9 : # fallbacks
            previous_intent = context.get("previous_intent",Node)
            if previous_intent is None:
                context['history'].append(
                    {
                        'node':'NaiveBayes',
                        'value':value
                    }
                )
                redirect_node = FallBackNode('fallbacks')
            else:
                if previous_intent == 'tra cứu luật':
                    redirect_node = RuleNode('ruleNode')
        else:

            context['history'].append(
                {
                    'node':'NaiveBayes',
                    'value':value
                }
            )
            if value['value'] == 'tra cứu luật':
                redirect_node = RuleNode('ruleNode')
            else:
                pass

        return redirect_node.excute(context)


class FallBackNode(Node):
    def excute(self,context):
        debug = context.get("verbose",0)
        if debug:
            logging.info(f'redirect to fallbacks save object {context}')
        context["answer"]="Xin lỗi không nhận ra câu hỏi của bạn"
        with open("cbr.logs.txt",'a') as f:
            f.write(
                json.dumps(context)
            ) 
            f.write("\n")
        return context

class RuleNode(Node):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

        # load db
        with open("rule.json",'r') as f:
            db = json.load(f)
            self.db = db 
        
    def find_rule(self, sentence):
        # db = ['việt vị','liệt vị','để tay chạm bóng','đá phạt','']
        entities ={
            'Sân thi đấu':['sân thi đấu','sân bóng','sân chơi bóng','sân đá','sân vận động'],
            'Yêu cầu về bóng':['bóng thi đấu','quả cầu','quả bóng'],
            'Trang phục':['trang phục thi đấu','quần áo cầu thủ','quần áo','trang phục'],
            'Thời gian thi đấu':['thời gian trận đấu','thời lượng trận đấu','số giờ trên trận đấu','số phút trên một trận đấu', 'thời gian bù giờ','hiệp phụ','hiệp chính'],
            'Bàn thắng hợp lệ':['bàn thắng','bàn thắng hợp lệ','bàn thắng chấp nhận'],
            'Var':["Công nghệ Var","Var","Vê a rờ"],
            "Việt vị":['Liệt vị','việt vị'],
            'Hưởng lợi thế':['hưởng lợi thế', 'lợi thế','pha tình huống lợi thế',],
            'Chèn cầu thủ':['chèn đối phương','chèn ép đối phương'],
            'Dùng tay chơi bóng':['dùng tay choi bóng','để bóng chạm tay','bóng chạm vào tay','tiếp xúc tay vào bóng'],
            'Mừng bàn thắng':['Cách ăn mừng','ăn mừng bàn thắng',],
            'Câu giờ':['câu giờ','trì hoãn'],
            'Lỗi vi phạm với thủ môn':['tác động tới thủ môn','phạm lỗi với thủ môn','vi phạm với thủ môn'],
            'Lỗi vi phạm của thủ môn':['các lỗi của thủ môn','các lỗi thủ môn mắc phải','thủ môn giữ bóng'],
            'đá phạt góc':['đá phạt góc','phạt góc'],
            'ném biên':['ném biên','đáp biên'],
            'thẻ':['thẻ đỏ','thẻ vàng','thẻ phạt'],
            'hình thức xử phạt':['xử phạt như thế nào','xử phạt kiểu gì','bị xử phạt ra sao'],
            'Phạt trực tiếp':['lỗi phạt trực tiếp','phạt thẳng'],
            'Phạt gián tiếp':['lỗi phạt gián tiếp', 'phạt gián tiếp'],
        }

        entites_matched = []
        for entitie in entities:
            for value in entities[entitie]:
                if value in sentence:
                    entites_matched.append({
                        'start':sentence.find(value),
                        'end':len(value),
                        'type':entitie
                    })
        return entites_matched
    def response(self, entiity_type):
        return self.db[entiity_type]
    def excute(self, context):
       
        logging.info(f'redirect to RuleNode with context {context}')
        history = context.get("history",[])
        history = history[-1]
        user_input = context.get("user_input","")
        # find rule 

        entites_matched = self.find_rule(user_input)
        if len(entites_matched) == 0:
            if context.get("previous_rule") is not None:
                entites_matched.extend(context.get("previous_rule"))
            # Nếu không tìm thâý lấu rule matched trước đó 
            logging.info(f"use  old rule = {entites_matched}")

        context['rule'] = entites_matched

        logging.info(f"find rule = {entites_matched}")
        type_entities  = list(set([i['type'] for i in entites_matched]))

        context['previous_intent'] = 'rule'
        if len(type_entities) == 1:
            context['answer'] =self.response(type_entities[0])
            return context
        elif len(type_entities) == 0:
            context['answer']  = f"Bạn muốn hỏi về luật nào nhỉ"
            return context
        elif len(type_entities) > 1:
            context['answer'] = f'Bạn muốn hỏi về :\n' + "\n".join([f'Luật {i}. {v}' for i,v in enumerate(type_entities, 1)])
            return context



