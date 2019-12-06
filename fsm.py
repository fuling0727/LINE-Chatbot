from transitions.extensions import GraphMachine
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage
from utils import send_text_message,send_image_message
import datetime
 

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_riddle1(self, event):
        text = event.message.text
        return text.lower() == "1"

    def is_going_to_riddle2(self, event):
        text = event.message.text
        return text.lower() == "2"

    def on_enter_riddle1(self, event):
        print("I'm entering riddle1")
        reply_token = event.reply_token
        send_text_message(reply_token, "皮卡丘站起來變什麼?")
        #self.go_back()

    def on_enter_riddle2(self, event):
        print("I'm entering riddle2")

        reply_token = event.reply_token
        send_text_message(reply_token, "有一天長方形、正方形、三角型約好一起出去玩，結果大家都到了剩下三角型沒到，這種情況叫什麼？")
        #self.go_back()

    def is_going_to_giveup(self, event):
        text = event.message.text
        return (text.lower() == "放棄" or text.lower() == "不知道")

    def on_enter_giveup(self, event):
        print("I'm entering giveup")
        reply_token = event.reply_token
        send_text_message(reply_token, "不要放棄啦!重新來一次吧~")
        self.go_back()

    def is_going_to_right(self, event):
        text = event.message.text
        return text.lower() == "皮卡兵" or text.lower() == "全等三角形"
    
    def on_enter_right(self, event):
        print("I'm entering right")
        reply_token = event.reply_token
        image_url = "https://memes.tw/user-template-thumbnail/03f01617946e73cbcb2259e47a4a69ca.jpg"
        #message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
        send_image_message(reply_token,image_url)
        self.go_back()
#wrong1
    def is_going_to_wrong1(self, event):
        text = event.message.text
        return text.lower() != "皮卡兵"

    def on_enter_wrong1(self, event):
        print("I'm entering wrong1")

        reply_token = event.reply_token
        send_text_message(reply_token, "答錯了. 剩下兩次機會!")
        
    def is_going_to_wrong1_1(self, event):
        text = event.message.text
        return text.lower() != "皮卡兵"

    def on_enter_wrong1_1(self, event):
        print("I'm entering wrong1_1")

        reply_token = event.reply_token
        send_text_message(reply_token, "答錯了. 最後一次機會囉~")
        
    def is_going_to_wrong1_2(self, event):
        text = event.message.text
        return text.lower() != "皮卡兵"

    def on_enter_wrong1_2(self, event):
        print("I'm entering wrong1_2")

        reply_token = event.reply_token
        send_text_message(reply_token, "答錯了!答案是 皮卡兵")
        self.go_back()
#wrong2
    def is_going_to_wrong2(self, event):
        text = event.message.text
        return text.lower() != "全等三角形"

    def on_enter_wrong2(self, event):
        print("I'm entering wrong2")

        reply_token = event.reply_token
        send_text_message(reply_token, "答錯了. 剩下兩次機會!")

    def is_going_to_wrong2_1(self, event):
        text = event.message.text
        return text.lower() != "全等三角形"

    def on_enter_wrong2_1(self, event):
        print("I'm entering wrong2_1")

        reply_token = event.reply_token
        send_text_message(reply_token, "答錯了. 最後一次機會囉~")

    def is_going_to_wrong2_2(self, event):
        text = event.message.text
        return text.lower() != "全等三角形"

    def on_enter_wrong2_2(self, event):
        print("I'm entering wrong1")

        reply_token = event.reply_token
        send_text_message(reply_token, "答錯了! 答案是 全等三角形!")
        self.go_back()
    #def on_exit_right(self):
    #    print("Leaving right")
    #def on_exit_giveup(self):
    #    print("Leaving giveup")

    #def on_exit_riddle1(self):
    #   print("Leaving riddle1")

    #def on_exit_riddle2(self):
    #    print("Leaving riddle2")
    def is_going_to_greet(self, event):
        text = event.message.text
        return (text.lower() == "hi" or text.lower() == "你好" or text.lower() == "hello" 
        or text.lower() == "嗨" or text.lower() == "早安")

    def on_enter_greet(self, event):
        print("I'm entering greet")

        reply_token = event.reply_token
        x = datetime.datetime.now()
        if (x.hour+8) < 12 and (x.hour+8) >= 6:
            message = "早安啊~現在是 "+str((x.hour+8))+"點"+str(x.minute)+"分"
        elif (x.hour+8) < 18 and (x.hour+8) >= 12:
            message = "午安~現在是 "+str((x.hour+8))+"點"+str(x.minute)+"分"
        elif (x.hour+8) < 24 and (x.hour+8) >= 18:
            message = "晚安~現在是 "+str((x.hour+8))+"點"+str(x.minute)+"分"
        elif (x.hour+8) < 6 and (x.hour+8) >= 0:
            message = "我在睡覺不要吵我...現在是 "+str((x.hour+8))+"點"+str(x.minute)+"分了ㄟ"
        
        send_text_message(reply_token, message)
        self.go_back()

    
    #def on_exit_greet(self):
    #    print("Leaving greet")