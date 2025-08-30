from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet
import nltk

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')

class IntentClassifier:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classifier = LogisticRegression()
        self.intent_examples = self._build_intent_examples()
        self.train()

    def _get_synonyms(self, phrase):
        """Expand phrase with synonyms from WordNet."""
        words = phrase.split()
        synonyms = set()

        for word in words:
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    synonym = lemma.name().replace("_", " ").lower()
                    if synonym != word.lower():
                        synonyms.add(synonym)

        expanded_phrases = set([phrase])
        for synonym in synonyms:
            expanded_phrases.add(phrase.replace(word, synonym))

        return list(expanded_phrases)

    def _build_intent_examples(self):
        base_intents = {
            "intro":[
                "introduce youself","who are you","who made you","give your introduction",
                "introduce yourself to me",
            ],
            "greeting": [
                "hello", "hi there", "good morning", "hey", "hi",
                "good evening", "good afternoon", "how are you",
                "hey there", "hi assistant", "hello there",
                "hi buddy", "greetings", "yo", "what's up"
            ],
            "tell_date": [
                "what's the date today", "tell me today's date", "what day is it",
                "current date", "today's date", "date please", "give me the date",
                "what is today's date", "tell date", "show me the date"
                "what is the date", "today's date", "current date", "date please",
                "tell me the date", "what's the date today", "give me the date",
                "date bolo", "today date", "current date please", "can you tell me date"
            ],
            "joke": [
                "tell me a joke", "make me laugh", "say something funny",
                "i want to hear a joke", "do you know any jokes",
                "tell a funny story", "crack a joke", "give me some humor",
                "make me smile", "entertain me", "funny joke please",
                "tell another joke", "say a hilarious thing", "joke for me"
            ],
            "play_song": [
                "play a song", "play music", "start music", "start playing music",
                "song please",
                "play something", "start my song", "music on", "play tunes",
                "can you play music", "put on music", "start my playlist", "play mp3",
                 "track play ", "music please"
            ],
            "weather": [
                "what's the weather like", "tell me the weather", "is it raining",
                "how's the weather today", "weather forecast please", "is it sunny today",
                "what is the temperature", "is it hot outside", "is it cold today",
                "give me the weather report", "current weather", "today's weather",
                "show me the weather", "is it cloudy", "how's outside weather"
            ],
            "news": [
               "tell me the news", "latest headlines", "what's happening today",
                "give me some updates", "breaking news", "read me the news",
                "what's the news today", "update me with news", "current affairs",
                "anything happening now", "news headlines", "recent news",
                "give me recent updates", "top news", "latest updates please",
                "read headlines", "show me today's news", "what's trending",
            ],
            "set_reminder":[
                "set a reminder", "remind me","set reminder alarm","remind me to",
                "set reminder for","save a reminder for","reminder","alarm","save a reminder",
                "save to remind me","wake me","notify me","notify me for","notify"
            ],
            "send_message": [
                "send message to", 
                "message to", 
                "send whatsapp message to", 
                "send a message to", 
                "text to",
                "send sms to",
                "whatsapp message to"
            ],
            "bye": [
                "goodbye", "bye", "ok for now","see you later", "talk to you soon",
                "catch you later", "see ya", "farewell", "bye bye",
                "talk later", "until next time", "later", "peace out"
            ],
          
        }

        # Expand examples with synonyms
        expanded_intents = {}
        for intent, examples in base_intents.items():
            expanded = set()
            for phrase in examples:
                expanded.update(self._get_synonyms(phrase))
                expanded.add(phrase)  # keep original
            expanded_intents[intent] = list(expanded)

        return expanded_intents

    def train(self):
        """Train the ML model with expanded intent examples."""
        examples = []
        labels = []
        for intent, phrases in self.intent_examples.items():
            examples.extend(phrases)
            labels.extend([intent] * len(phrases))

        self.vectorizer.fit(examples)
        X = self.vectorizer.transform(examples)
        self.classifier.fit(X, labels)

    def predict(self, text):
        """Predict intent using ML + fuzzy matching."""
        # Step 1: ML prediction
        X_test = self.vectorizer.transform([text])
        ml_prediction = self.classifier.predict(X_test)[0]

        # Step 2: Fuzzy check
        best_match = None
        highest_score = 0
        for intent, phrases in self.intent_examples.items():
            for phrase in phrases:
                score = fuzz.ratio(text.lower(), phrase.lower())
                if score > highest_score:
                    highest_score = score
                    best_match = intent

        # If fuzzy confidence is high, trust it more
        if highest_score > 80:
            return best_match
        return ml_prediction
