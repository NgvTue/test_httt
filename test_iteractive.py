from src.graph import PathGraph, Node, Graph
from src.model import predict
from src.infer import NaiveBayesNode
print("-"*100)
first_node  = NaiveBayesNode('first_node_naive_bayes', )

context ={
    'db':{'cầu thủ':None, 'previous_intent':None, 'previous_rule':None},
    'history':[],
    'user_input':'Cho mình thông tin luật sân bóng và việt vị nào?',
    'verbose':1,
    'follow_node':None
}

context = first_node.excute(context)



print("-"*100)
print("Answer=", context['answer'])
print("-"*100)
context['user_input']='sân bóng ý bạn'
print(context,"dsadsadsa")
context = first_node.excute(context)
print("-"*100)
print("Answer=", context['answer'])
print("-"*100)
context['user_input']='Cho mình hỏi ngày sinh của Công Phượng với mình'

context = first_node.excute(context)
# print("-"*100)
print("Answer=", context['answer'])
print("-"*100)
print("-"*100)
context['user_input']='Cho mình hỏi về trang phục thi đấu với'

context = first_node.excute(context)
context['user_input']='Vậy cho mình hỏi tình huống "cầu thủ đội bạn di chuyển chèn đối phương trong tình huống phạt góc" có phạm lỗi không?'
context = first_node.excute(context)
print("ne")
import json


db = {
    'Sân thi đấu':{
    'text':"""
    Sân bóng đá là khoảng không gian hình chữ nhật nơi các cầu thủ thi đấu với nhau. Chúng có chiều dài là trong khoảng 100-110m và chiều rộng trong khoảng 64-75m. Hai đường giới hạn dài hơn theo chiều dọc gọi là đường biên dọc.
    Hai đường ngắn hơn gọi là đường biên ngang. Đường thẳng kẻ suốt chiều ngang ở giữa chia sân thành 2 phần bằng nhau gọi là đường giữa sân.
    Mỗi đội sẽ bảo vệ một nửa phần sân của mình và tấn công vào phần sân đối thủ. Một vòng tròn được kẻ vòng quanh có bán kính 9m15 gọi là vòng tròn trung tâm. Tại tâm điểm của sân bóng là điểm phát bóng giữa sân.
    Ở giữa 2 đường đường biên ngang cuối 2 đầu sân là khu cầu môn. Đây là khu vực có khung thành với chiều ngang 7,32m và cao 2,44m. Bao quanh khung thành là vùng cấm địa hay còn gọi là khu vực 16m50. Đây là phạm vi thủ môn được dùng tay để bắt bóng.
    Các cầu thủ phòng ngự phạm lỗi trong khu vực này sẽ bị thổi phạt penalty. Quả phạt sẽ được thực hiện trên chấm penalty. Nó được nằm ở giữa và cách khung thành 11m.
    Gần sát khung thành có một khung nhỏ hơn gọi là khu vực 5m50. Đây là nơi thực hiện những cú phát bóng lên. Ở 4 góc sân là 4 chấm phạt góc. Mặt sân bóng đá 11 người thường là cỏ tự nhiên hoặc cỏ nhân tạo. Chúng phải có màu xanh lá cây.
    """,
    'img':"datasets/san1.jpg"
    },
    "Yêu cầu về bóng":{
        'text':"""
            Quả bóng đá phải có hình cầu và được làm bằng da hoặc một chất liệu tương đương. Nó gồm có 5 loại kích cỡ được đánh số từ 1 đến 5. Cỡ số 5 là bóng tiêu chuẩn được áp dụng trong các trận đấu chuyên nghiệp.
            Cầu thủ từ 15 tuổi đều sử dụng loại bóng ở kích cỡ này. Bóng cỡ 5 có trọng lượng từ 410 đến 450 g. Chúng có chu vi từ 68 đến 70cm và được bơm căng ở áp suất từ 0,6 đến 1,1. Các kích thước bóng nhỏ hơn dành cho các giải đấu dành cho trẻ em tùy độ tuổi.
        """
    },
    "Trang phục":{
        "text":"""
        Giày là trang bị bắt buộc đầu tiên mà mọi cầu thủ bóng đá phải có. Giày sử dụng trong bóng đá 11 người là giày đá bóng chuyên dụng. Cầu thủ cũng cần có vớ (tất) và một cặp bảo vệ ống chân. Phần với phải che phủ hoàn toàn phần bảo vệ ống chân.
        Các cầu thủ trong một đội sẽ mặc đồng phục gồm quần ngắn, áo (ngắn tay hoặc dài tay). Thủ môn sẽ có một trang phục riêng để phân biệt với các cầu thủ còn lại trong đội. Trang phục của thủ môn cũng gồm quần áo (dài hoặc ngắn) và một đôi găng tay. Hai đội sẽ có màu trang phục khác nhau về màu sắc đáng kể để dễ phân biệt.
        Trọng tài là người kiểm tra các vấn đề trang bị của cầu thủ. Nếu không đạt yêu cầu theo các quy định trên, bạn không thể ra sân thi đấu.
        """
    },
    "Thời gian thi đấu":{
        "text":"""
        Một trận đấu bóng đá tiêu chuẩn sẽ có tổng cộng 90 phút thi đấu chính thức. Thời gian này được chia là 2 hiệp đấu với mỗi hiệp là 45 phút. Mỗi đội sẽ chơi ở một bên sân trong một hiệp rồi đổi bên ở hiệp còn lại.
        Khoảng nghỉ giữa 2 hiệp là 15 phút. Đây là thời gian các cầu thủ nghỉ ngơi và nghe chỉ đạo của huấn luyện viên. Trận đấu thường bị gián đoạn do các cầu thủ chấn thương hay bóng ra ngoài biên. Khi đó trọng tài sẽ cộng thêm thời gian bù giờ sau khi hết 45 phút ở mỗi hiệp.
        Trong một số trận đấu loại trực tiếp sẽ không chấp nhận kết quả hòa. Nếu trong 90 phút chính thức và bù giờ, các đội hòa nhau sẽ phải đá hiệp phụ. Hiệp phụ sẽ có tổng thời gian 30 phút và chia là 2 như trên. Tuy nhiên 2 đội sẽ đổi sân và thi đấu ngay sau mỗi hiệp phụ chứ không nghỉ.
        """
    },
    "Bàn thắng hợp lệ":{
        "text":"""
        Bàn thắng hợp lệ là quả bóng nằm hoàn toàn bên trong vạch cầu môn theo luật bóng đá 11 người.
        """
    },
    "Var":{
        "text":"""
            VAR (Video Assistant Referee) là công nghệ hỗ trợ trọng tài bằng video. Hiện tại, công nghệ này được sử dụng để hỗ trợ, giúp các trọng tài bóng đá nắm bắt tình hình trận đấu và đưa ra những quyết định chính xác nhất trong những trường hợp gây tranh cãi.
            Những trường hợp được áp dụng VAR:
            1. Bàn thắng gây tranh cãi
            2. Penalties
            3. Thẻ đỏ trực tiếp
            4. Nhận diện những sai lầm trọng tài
        """
    },
    "Việt vị":{
        "text":"""
            Việt vị là một lỗi thường xảy ra trong bóng đá khi một đội đang tấn công. Một cầu thủ sẽ bị thổi phạt việt vị nếu mắc cả lỗi việt vị. Lỗi này được quy định như sau:
            Một cầu thủ sẽ rơi vào vị trí việt vị khi bất cứ bộ phận nào của cầu thủ này ở phần sân của đối phương và gần vạch cầu môn khung thành đối phương hơn cả bóng và cầu thủ phòng ngự thứ 2 (tính từ cầu môn) của đối phương. Cầu thủ đứng ở vị trí trên nhưng không tham gia tình huống tấn công không mắc lỗi việt vị.
        """
    },
    "Hưởng lợi thế":{
        "text":"""
            
        """
    }


}
with open("rule.json","w+") as f:
    json.dump(db,f)