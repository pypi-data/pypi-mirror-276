QnAs = {}
Cmds = {}

def AddQna(question, response):
    QnAs[question] = response

def Addcmd(cmd, code):
    Cmds[cmd] = code

def Start(chatbotname, lang):
    if lang == "en":
        print("Use 'exit' to exit")
        print("Use 'questions' to see all questions you can do")
        while True:
            question = input(f"Talk with {chatbotname}! > ")

            if question == "exit":
                break
            elif question == "questions":
                for questi in QnAs:
                    print(questi)
            else:
                for cmd in Cmds:
                    if question == cmd:
                        exec(cmd)
                for ques in QnAs:
                    if question == ques:
                        print(f"{chatbotname}: {QnAs[question]}")
    elif lang == "pt":
        print("Use 'sair' para sair")
        print("Use 'perguntas' para ver as perguntas")
        while True:
            question = input(f"Talk with {chatbotname}! > ")

            if question == "sair":
                break
            elif question == "perguntas":
                for questi in QnAs:
                    print(questi)
            else:
                for cmd in Cmds:
                    if question == cmd:
                        exec(cmd)
                for ques in QnAs:
                    if question == ques:
                        print(f"{chatbotname}: {QnAs[question]}")