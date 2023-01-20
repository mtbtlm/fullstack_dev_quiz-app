class Answer():
    def __init__(self, text:str,isCorrect:bool) :
        self.text = text
        self.isCorrect = isCorrect

    def to_json(self):
        return {
            "text": self.text,
            "isCorrect": bool(self.isCorrect),
        }


class Question():
    def __init__(self
    ,text:str,title:str,image:str,position:int
    ,possibleAnswers:list[Answer]
    ) :
        self.text = text
        self.title = title
        self.image = image
        self.position = position
        self.possibleAnswers = possibleAnswers

    def to_json(self):
        return {
            "text":self.text,
            "title":self.title,
            "image": self.image,
            "position": self.position
            ,"possibleAnswers":[answer.to_json() for answer in self.possibleAnswers]
        }

    def isAnswerTrue(self, position: int):
        if position < 1:
            return "error, answer must be at least position 1" + str(position)

        if position > len(self.possibleAnswers):
            return "error, no answer on this position" + str(position)

        answer_position = self.possibleAnswers[position -1]
        
        return answer_position.isCorrect

    def from_json(self,question_json):
        for k,v in question_json.items() :
            setattr(self,k,v)



class Participation():
    def __init__(self,playerName:str,score:int) :
        self.playerName = playerName
        self.score = score

    def to_json(self):
        return {
            "playerName": self.playerName,
            "score": self.score
        }


    






    



