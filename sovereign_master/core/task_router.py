class TaskRouter:
    categories=("general","reasoning","math","coding","research","translation","language","documents","data","vision","voice","spiritual","education")
    keywords={"math":("calculate","math","equation","calcul"),"coding":("code","python","bug","api"),"research":("research","source","recherche"),"translation":("translate","traduire"),"spiritual":("bible","prayer","prière","dieu","god","proph"),"education":("learn","explain","apprendre","explique"),"reasoning":("why","logic","pourquoi","solve")}
    def register(self, category, words): self.keywords[category]=tuple(words)
    def classify(self, message):
        text=message.lower()
        for category, words in self.keywords.items():
            if any(word in text for word in words): return category
        return "general"
