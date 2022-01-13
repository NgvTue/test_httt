from src.graph import PathGraph, Node, Graph
from src.model import predict, clean_text
import time
import logging
import json
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)


class NaiveBayesNode(Node):
    
    def excute(self, context):
        if context.get("follow_node",None)  is not None:
            return context.pop("follow_node").excute(context)
        if 'fallbacks' in context.get("user_input").lower().strip():
            return FallBackNode('fallbacks').excute(context)
        history = context.get("history",[])
        user_inputs = context.get("user_input","")
        follow_node = context.get("follow_node",None)
        
        # naive bayess
        value = predict(user_inputs)[0] #[{'p':'xác xuất của nhãn','value':nhãn predict ra, ' text':câu hỏi }]
        logging.info(f"Naive Bayess step return {value}")

        if value.get('p') < 0.7 : # fallbacks
            previous_intent = context.get("previous_intent",None)
            logging
            if previous_intent is None:
                context['history'].append(
                    {
                        'node':'NaiveBayes',
                        'value':value
                    }
                )
                redirect_node = FallBackNode('fallbacks')
            else:
                if  previous_intent == 'tra cứu luật':
                    context['previous_intent'] = 'tra cứu luât'
                    redirect_node = RuleNode('ruleNode')
                elif previous_intent =='tình huống':
                    context['previous_intent'] = 'tình huống'
                    redirect_node = ActionNode("action") 
                elif previous_intent == 'tra cứu cầu thủ':
                    context['previous_intent'] = 'tra cứu cầu thủ'
                    redirect_node = FindPerson("personNode")
                else:
                    redirect_node = FallBackNode("fallback")
        else:

            context['history'].append(
                {
                    'node':'NaiveBayes',
                    'value':value
                }
            )
            if value['value'] == 'tra cứu luật':
                context['previous_intent'] = 'tra cứu luât'
                  
                redirect_node = RuleNode('ruleNode')
            elif value['value'] == 'tình huống':
                context['previous_intent'] = 'tình huống'
                redirect_node = ActionNode("action")
                
            elif value['value'] == 'tra cứu cầu thủ':
                context['previous_intent'] = 'tra cứu cầu thủ'
                redirect_node = FindPerson('personNode')
                #
            elif value['value'] == 'kết thúc trò chuyện':
                context['answer'] = "Hẹn gặp lại bạn sau nhé!"
        return redirect_node.excute(context)


class FallBackNode(Node):
    def excute(self,context):
        if context.get("follow_node",None)  is not None:
            return context.pop("follow_node").excute(context)
        
        
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
                if value.lower() in sentence.lower():
                    entites_matched.append({
                        'start':sentence.lower().find(value.lower()),
                        'length':len(value) ,
                        'type':entitie
                    })
        return entites_matched
    def response(self, entiity_type):
        return self.db[entiity_type]['text']
    def excute(self, context):
        if context.get("follow_node",None)  is not None:
            return context.pop("follow_node").excute(context)
        logging.info(f'redirect to RuleNode with context {context}')
        history = context.get("history",[])
        history = history[-1]
        user_input = context.get("user_input","")
        # find rule 

        entites_matched = self.find_rule(user_input)
        # if len(entites_matched) == 0:
            # if context.get("previous_rule") is not None:
            #     entites_matched.extend(context.get("previous_rule"))
            # # Nếu không tìm thâý lấu rule matched trước đó 
            #     logging.info(f"use  old rule = {entites_matched}")

        context['rule'] = entites_matched
        logging.info(f"find rule = {entites_matched}")
        type_entities  = list(set([i['type'] for i in entites_matched]))

        context['previous_intent'] = 'rule'
        if len(type_entities) == 1:
            context['answer'] =self.response(type_entities[0])
            context['history'].append({
                    'node':self.name,
                    'value':context['answer']
                })
            return context
        elif len(type_entities) == 0:
            context['answer']  = f"Bạn muốn hỏi về luật nào nhỉ Option:\n" + """
            1. Sân thi đấu
            2. Yêu cầu về bóng
            3. Trang phục
            4. Thời gian thi đấu
            5. Bàn thắng hợp lệ
            6. Var
            7. Việt vị
            8. Hưởng lợi thế'
            9. Chèn cầu thủ
            10. Dùng tay chơi bóng
            11. Mừng bàn thắng
            12. Câu giờ
            13. Lỗi vi phạm với thủ môn
            14. Lỗi vi phạm của thủ môn
            15. đá phạt góc
            16. ném biên
            17. thẻ
            18. hình thức xử phạt
            19. Phạt trực tiếp
            20. Phạt gián tiếp
            21. fallbacks
            """
            context['follow_node'] = self
            context['history'].append({
                    'node':self.name,
                    'value':context['answer']
                })
            return context
        elif len(type_entities) > 1:
            context['answer'] = f'Bạn muốn hỏi về :\nOption:' + "\n".join([f'Luật {i}. {v}' for i,v in enumerate(type_entities, 1)]) + "\nFallbacks"
            context['follow_node'] = self
            context['history'].append({
                    'node':self.name,
                    'value':context['answer']
                })
            return context



class FindPerson(Node):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

        # load db
        with open("person.json",'r') as f:
            db = json.load(f)
            self.db = db 
    def find_person(self, sentence):
        entities = {
            'Nguyễn Công Phượng':["Nguyễn Công Phượng", "Cầu thủ Nguyễn Công Phượng", "Công Phượng", "Cầu thủ Công Phượng","công phượng"],
            "Nguyễn Văn Quyết":["Nguyễn Văn Quyết","Văn Quyết", "văn quyết"],
            "Quế Ngọc Hải":["Quế Ngọc Hải","quế ngọc hải"],
            "Hà Đức Chinh":["Hà Đức Chinh","Đức Chinh","đức chinh"],
            "Lương Xuân Trường":["Lương xuân Trường","lương xuân trường","xuân trường"],
            "Đặng Văn Lâm":["đặng văn lâm",'Đặng Văn Lâm',"Văn Lâm","văn lâm"],
            "Bùi Tiến Dũng":["Bùi Tiến Dũng","Tiến Dũng","tiến dũng"],
            "Phan Văn Đức":["Phan Văn Đức","phan văn đức","văn đức"],
            "Nguyễn Tuấn Anh":["Nguyễn Tuấn Anh","Tuấn Anh","tuấn anh"],
            "Nguyễn Tiến Linh":["Nguyễn Tiến Linh","Tiến Linh","tiến linh"],
            "Nguyễn Văn Toàn":["Nguyễn Văn Toàn","nguyễn văn toàn","Văn Toàn","văn toàn"],
            "Phạm Tuấn Hải":["Phạm Tuấn Hải","phạm tuấn hải","Tuấn Hải","tuấn hải"],
            "Nguyễn Trọng Hoàng":["Nguyễn Trọng Hoàng","Trọng Hoàng","trọng hoàng",],
            "Nguyễn Hoàng Đức":['Nguyễn Hoàng Đức',"Hoàng Đức","hoàng đưc"],
            "Hồ Tấn Tài":["Hồ Tấn Tài","Tấn Tài","tấn tài"],
            "Vũ Văn Thanh":["Vũ Văn Thanh","vũ văn thanh","Văn Thanh","văn thanh"],
            "Nguyễn Thành Chung":["Thành Chung","thành chung",],
            "Nguyễn Hồng Duy":['Nguyễn Hồng Duy','Hồng Duy',"hồng duy"],
            
        }
        entities_2={
            "năm sinh":['năm sinh','sinh ngày','sinh nhật',"ngày sinh"],
            "quê quán":['quê quán','địa chỉ nhà','ở đâu'],
            "Thành tích":['Thành tích','thành tích','thành quả','đạt được gì']
        }
        entites_matched = []
        for entitie in entities:
            for value in entities[entitie]:
                if value in sentence:
                    entites_matched.append({
                        'start':sentence.find(value),
                        'length':len(value) ,
                        'type':entitie
                    })
        entitie_matched_2=[]
        for entitie in entities_2:
            for value in entities_2[entitie]:
                if value in sentence:
                    entitie_matched_2.append({
                        'start':sentence.find(value),
                        'length':len(value) ,
                        'type':entitie
                    })
        return entites_matched, entitie_matched_2
    def response(self, name, form):
        if len(form) == 0:
            v=self.db[name]
            rx=f"{name}: {v['mô tả chung']}\nNgay Sinh:{v['năm sinh']}\nQuê quán: {v['quê quán']}"
            if len(v.get("thành tích","")) >0 or len(v.get("Thành tích","")) > 0:
                rx = rx+"\nThanhf tích : " + v.get("thành tích","") + v.get("Thành tích","") + "\n"
            return rx 

        else:return self.db[name][form[0]['type']]
    def excute(self, context):
        if context.get("follow_node",None)  is not None:
            return context.pop("follow_node").excute(context)
        
        history = context.get("history",[])
        history = history[-1]
        user_input = context.get("user_input","")
        # find rule 
        logging.info(f"redict node {self.name}")
        entites_matched, entitie_matched_2 = self.find_person(user_input)
        logging.info(f"answer for {entites_matched} - {entitie_matched_2}")
        if len(entites_matched) == 1:
            context['answer']   = self.response(entites_matched[0]['type'],entitie_matched_2)
            return context
        elif len(entites_matched) > 1:
            context['answer']  = f"Bạn muốn hỏi về cầu thủ nào nhỉ:\nOption:" + "\n".join([i['type'] for i in entites_matched] + ["falllbacks,"])
            context['follow_node'] = self
            context['history'].append({
                    'node':self.name,
                    'value':context['answer']
                })
            return context
        else:
            if context.get("just_find_entities",0) > 1 :
                context = FallBackNode("fallbacksnode_find_person").excute(context) # save lai vao cbr
                context['answer'] = f'Xin lỗi bạn hiện tại chúng tôi chưa cập nhật thông tin cầu thủ này !!!'
                return context

            context['answer'] = f"Bạn muốn hỏi về cầu thủ nào nhỉ:\n"
            context['follow_node'] = self
            context['just_find_entities']  = context.get("just_find_entities",0) + 1
            context['history'].append({
                    'node':self.name,
                    'value':context['answer']
                })
            return context

class ActionNode(Node):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

        # load db
        with open("action.json",'r') as f:
            db = json.load(f)
            self.db = db 
    def map_sentence(self, a, b):
        a=clean_text(a)
        b=clean_text(b)
        a = a.split()
        b = b.split()
        vocab_a = set(a)
        vocab_b = set(b)
        
        overlap_vocab = vocab_a - (vocab_a - vocab_b)

        iou = len(overlap_vocab) / (len(vocab_a) + len(vocab_b) - len(overlap_vocab))

        if iou >= 0.8:return True 
        return False 

    def find_answer(self, query):
        for root_type in self.db:
            print(root_type)
            for question, answer in zip(self.db[root_type]['question'],self.db[root_type]['answer']):
                if self.map_sentence(query, question):
                    return answer
        with open("cbr_tinhhuong.txt","a") as f:
            f.write(f"{query}\n")
        return "Tình huống bạn nhập bot sẽ update và trả lời bạn sau xin lỗi bạn."
    def excute(self, context):
        
        if context.get("follow_node",None)  is not None:
            return context.pop("follow_node").excute(context)
        logging.info(f'redirect to actionNode with context {context}')
        history = context.get("history",[])
        history = history[-1]
        user_input = "." + context.get("user_input","")
        if '"' not in user_input:
            answer = 'Vui lòng nhập tình huống vào dấu ""'
            context['answer'] = answer
            context['follow_node'] = self 

        user_input = user_input.split('"')[1]
        answer  =self.find_answer(user_input)
        if answer == "Tình huống bạn nhập bot sẽ update và trả lời bạn sau xin lỗi bạn.":
            context['answer']="""THeo bạn tình huống đó có thể bị lỗi gì trong lỗi sau Option: 
            Việt Vị
            Dùng tay chơi bóng 
            Phạm lỗi với thủ môn
            Thủ môn phạm lỗi
            fallbacks
            """  
            context['follow_node'] = OptionActionNode("option 1")
            
        else:   
            context['answer'] = answer
        context['history'].append({
            'node':self.name,
            'value':context['answer']
        })
        return context

class OptionActionNode(Node):
    def excute(self, context):
        if self.name == 'option 1':
            user_input = context.get("user_input","")   

            if user_input.strip() == "Việt Vị":
                context['answer'] = """Hỏi người dùng:
                                    Cầu thủ hiện tại có đứng tại phần sân đối phương không
                                    Option: yes\nno"""
                context['follow_node'] = OptionActionNode("option vietvi 1")
                context['history'].append({
                    'node':self.name,
                    'value':context['answer']
                })
                return context
            


            if user_input == 'Phạm lỗi với thủ môn':
                context['answer'] = """Cầu thủ có cản trở sự di chuyển của thủ môn không?
                                        Ví dụ như trong tình huống đá phạt có chèn ép, đẩy thủ môn ko ? 
                                        Option: yes\nno """
                context['follow_node'] =OptionActionNode("option plvtm 1")
                context['history'].append({
                    'node':self.name,
                    'value':context['answer']
                })
                return context
            
            # if user_input ==""

        if "option vietvi" in self.name:
            if "1" in self.name:
                user_input = context.get("user_input","")
                if user_input.strip() == "yes":
                    context['answer'] = """Hỏi người dùng:
                                        Cầu thủ hiện tài có đứng sau cầu thủ đối phương gần nhất thứ 2 kể từ vạch kẻ ngang hết sân phía đội bạn không?
                                        Option: yes\nno"""
                    context['follow_node'] = OptionActionNode("option vietvi 2")
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context
                else:
                    context['answer']="""Cẩu thủ chỉ bị lỗi việt vị khi đang đứng trên phần sân của đổi bạn tính từ vạch kẻ ngang giữa sân do vậy cầu thủ đó không phạm lỗi"""
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context
            if "2" in self.name:
                user_input = context.get("user_input","").strip()
                if "yes" in user_input:
                    context['answer']="""Cẩu thủ chỉ bị lỗi việt vị khi đứng trước cầu thủ đối phương thứ 2 tính từ vạch kẻ ngang hết sân phía đội bạn. Do vậy cầu thủ đó không phạm lỗi"""
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context
                if "no" in user_input:
                    context['answer'] ="""Cầu thủ đó có nhận bóng hay tham gia vào tình huống đó không ví dụ không chạm bóng nhưng cô tình dùng thân che chắn chèn ép đối phương trước bóng,... không? Option yes\nno"""
                    context['follow_node'] = OptionActionNode("option vietvi 3")
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context

            if "3" in self.name:
                user_input = context.get("user_input","").strip()
                if "yes" in user_input:
                    context['answer']  = "Cầu thủ trên đã ở tư thế việt vị và tham gia vào tình huống bóng nên phạm lỗi việt vị"
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context
                else:
                    context['answer']  = "Cầu thủ trên đã ở tư thế việt vị nhưng không tham gia vào tình huống bóng nên không phạm lỗi việt vị"
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context


        if "option plvtm" in self.name:
            if "1" in self.name:
                user_input = context.get("user_input","")  
                if user_input=="no":
                    context['answer']="""Cầu thủ này có cố tình đá bóng trong khi thủ môn đang tư thế thả bóng hay không?
                                            option : yes\nno"""
                    context['follow_node'] = OptionActionNode("option plvtm 2")
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context
                else:
                    context['answer'] ="tình huống đó có phạm lỗi với thủ môn"
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context 
            if "2" in self.name:
                user_input = context.get("user_input","")  
                if user_input=="no":
                    context['answer']="""Cầu thủ này có cố tình ngăn cản thủ môn thả bóng rời tay không?
                                            Option : yes\nno"""
                    context['follow_node'] = OptionActionNode("option plvtm 3")
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context
                else:
                    context['answer'] ="tình huống đó có phạm lỗi với thủ môn"
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context
            if '3' in self.name:
                user_input = context.get("user_input","") 
                if user_input == 'yes':
                    context['answer'] ="tình huống đó có phạm lỗi với thủ môn"
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context
                else:
                    context['answer'] = "tình huống đó không phạm lỗi với thủ môn"
                    context['history'].append({
                        'node':self.name,
                        'value':context['answer']
                    })
                    return context
        
