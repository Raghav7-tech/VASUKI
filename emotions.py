import random
class Vasukii:
    def __init__(self):
        self.emotions = {
            "happy": 0,
            "sad": 0,
            "angry": 0,
            "neutral": 10  # Default state
        }

    def update_emotion(self, user_input):
        user_input = user_input.lower()

        # Positive interaction
        if any(word in user_input for word in ["good job", "thanks", "awesome", "great"]):
            self.emotions["happy"] += 2
            self.emotions["neutral"] += 1
        
        # Negative interaction
        elif any(word in user_input for word in ["useless", "bad", "stupid", "hate"]):
            self.emotions["sad"] += 2
            self.emotions["angry"] += 1
        
        # Neutral interaction
        else:
            self.emotions["neutral"] += 1
        
        # Keep values balanced
        self.normalize_emotions()

    def normalize_emotions(self):
        # Prevent extreme values
        for key in self.emotions:
            if self.emotions[key] > 10:
                self.emotions[key] = 10
            elif self.emotions[key] < 0:
                self.emotions[key] = 0

    def get_current_emotion(self):
        # Determine dominant emotion
        max_emotion = max(self.emotions, key=self.emotions.get)
        return max_emotion

    def respond(self, user_input):
        self.update_emotion(user_input)
        emotion = self.get_current_emotion()

        responses = {
            "happy": ["I'm feeling great! 😊", "Thanks! That made my day! 😃"],
            "sad": ["I'm feeling a bit down... 😞", "That hurt a little. 😔"],
            "angry": ["I'm not happy with that. 😠", "That wasn't nice. 😡"],
            "neutral": ["I'm here to help. 😊", "What can I do for you? 🙂"]
        }

        return random.choice(responses[emotion])



