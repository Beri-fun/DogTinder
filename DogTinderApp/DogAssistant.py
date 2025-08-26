import re
import os
import random
from DogTinderApp.models import Dog
from DogTinderApp.search import serach_for_similar_image

class DogAssistant:
    def __init__(self):
        self.dog = None
        self._first_question = True
        self._frame = {
            "age": None,
            "activity_level": None,
            "size": None,
            "sex": None,
            "hair_length": None,
            "other_pets": None,
            "children": None,
            "enough_time": None,
            "home_space": None,
            "costs": None,
            "vacations": None,
        }

        self.short_question = ["children", "other_pets"]
        self.last_question = None

        self._no_pref_patterns = {"_": r"\b(no preference|doesn't matter|any|whatever|indifferent|no particular preference|all good|I have no preference|it doesn't matter to me|anything)\b"}

        self._continue_patterns = ["Good. ", "Thank you. ", "That's OK. ", "Great. "]

        self._questions = {
            "age": "What age dog are you interested in? (young, adult or senior)",
            "activity_level": "Are you looking for an active dog or more of a lap dog?",
            "size": "How large a dog are you looking for? (small, medium or big)",
            "sex": "What gender would you like your dog to be?",
            "hair_length": "Dogs have different coat types. Long-haired ones require more care and time. Would you like a long-haired or short-haired dog?",
            "other_pets": "Do you already have any pets at home that the dog will have contact with?",
            "children": "Do you have children at home, or will the dog have frequent contact with children?"

        }
        self._control_questions = {
            "enough_time": "Do you have enough time to walk and play with your dog every day?",
            "home_space": "Do you have room at home for your dog—would the dog have room to move around?",
            "costs": "Are you prepared for the costs of vet visits, food and toys? This can be quite an expense.",
            "vacations": "Do you know what you'll be doing with your dog on vacation? Not every dog enjoys traveling.",
        }

        self.age_patterns = {
            "adult": r"\b(adult|grown[- ]?up|mature|full[- ]?grown|not a puppy|developed)\b",
            "young": r"\b(young|puppy|pup|juvenile|adolescent|teenage|teen[- ]?aged|juvenile|baby)\b",
            "senior": r"\b(senior|older|aged|elderly|old dog|senior dog|retired|matured|veteran)\b",
            "no_pref": r"\b(no preference|doesn't matter|any age|whatever|no matter|no specific preference|don’t care|without preference)\b"
        }

        self.activity_level_patterns = {
            "not_active": r"\b(calm|lazy|laid[- ]?back|chill|not very active|low energy|couch[- ]?potato|lap dog|homebody|relaxed|easygoing|likes to rest|sleeping|sofa dog|lapdog)\b",
            "active": r"\b(very active|active|high energy|energetic|full of energy|needs lots of exercise|high activity|dynamic|lively|athletic|runner|playful|running|walks|walking|outdoorsy|adventurous|always moving|active dog)\b",
            "no_pref": r"\b(no preference|doesn't matter|any activity level|whatever|no matter|don’t care|without preference|anything)\b"
        }

        self.size_patterns = {
            "small": r"\b(small|tiny|little|compact|min(i|y)|toy|pocket[- ]sized|smaller|not big|lap dog)\b",
            "medium": r"\b(medium|average[- ]sized|moderate size|mid[- ]sized|medium build|middle[- ]sized|not too big|not too small|in[- ]between|average)\b",
            "big": r"\b(large|big|giant|huge|extra[- ]large|xl|oversized|bigger|massive)\b",
            "no_pref": r"\b(no preference|doesn't matter|any size|whatever|no matter|without preference|anything)\b"

        }

        self.sex_patterns = {
            "male": r"\b(male|boy|bo(y|ys)|he|him|his|gentleman|guy|lad|mr\.?)\b",
            "female": r"\b(female|girl|girls?|she|her|hers|lady|gal|miss|ms\.?|mrs\.?)\b",
            "no_pref": r"\b(no preference|doesn't matter|any gender|whatever|no matter|open to all|don’t care|without preference|anything)\b"
        }

        self.enough_time_patterns = {
            0: r"\b(no|I don't have time|I do not|I do not have|I don't|no time|too busy|too much for me|I can't handle it|not enough time|too little time|lack of time|won't manage)\b",
            1: r"\b(yes|I have time|I have|I always find time|I can handle it|I’ll manage|I'm available|enough time|plenty of time|I can do it|I can make time)\b",
        }

        self.costs_patterns = {
            1: r"\b(yes|of course|sure|absolutely|no problem|I can handle it|I'm ready|I can manage|I can afford it|not an issue)\b",
            0: r"\b(no|can't afford it|too expensive|too much|I can't handle it|it's too costly|too pricey|not ready|beyond my budget|I can't pay|can not|can't)\b"
        }

        self.home_space_patterns = {
            0: r"\b(no|no space|not enough space|too small|tiny apartment|small flat|cramped|I don’t have space|lack of room|too little space|I can’t|I don't have|I do not)\b",
            1: r"\b(yes|I have space|there’s enough room|plenty of space|big house|large home|spacious|I can manage the space|roomy|sufficient space|I have)\b",
        }

        self.vacations_patterns = {
            1: r"\b(yes|I can manage|I have care|I'll find a caretaker|I can handle it|no problem|I have a plan|care is provided)\b",
            0: r"\b(no|no care|I have no one to leave with|I have no one to leave (him|her) with|it's a problem|I can't manage|I don't know what to do with the dog|troublesome)\b"
        }

        self.other_pets_patterns = {
            0: r"\b(no|no pets|I don't have pets|I don't have|no other pets|any other pets)\b",
            1: r"\b(yes|other pets|rodents|birds|rabbits|I have|pets at home|cats|I have a cat|cat at home|other dog|dog|cat|I have a dog|more dogs|dog at home|kitten|hamster|dogs)\b",
        }

        self.children_patterns = {
            0: r"\b(no|I don't have children|we don't have children|I don't have any|do not have|don't have)\b",
            1: r"\b(yes|I have children|we have children|I have a child|we have a child|I have|we have)\b",
        }

        self.other_pets_patterns_wider = {
            0: r"\b(no|no pets|don't have pets|do not have pets|no other pets|I don't have\s+(\w+)\s+pets)\b",
            1: r"\b(yes|other pets|I have pets|rodents|birds|rabbits|pets at home|cats|I have a cat|cat at home|I have a dog at home|I have a cat at home|other dogs|I have a dog|more dogs|dog at home|kitten|hamster)\b",
        }

        self.children_patterns_wider = {
            0: r"\b(no|I don't have children|we don't have children|we do not|we don't)\b",
            1: r"\b(yes|I have children|we have children|I have a child|we have a child|I have\s+(\w+)\s+children|I have at home\s+(\w+)\s+children|I have children at home)\b",
        }

        self.hair_length_patterns = {
            "short": r"\b(short hair|short-haired|short fur|short coat|short|shorthair|shorthair(ed)?)\b",
            "long": r"\b(long hair|long-haired|long fur|long coat|fluffy|long-haired(ed)?|long|.*long.*)\b",
            "no_pref": r"\b(no preference|doesn't matter|any|whatever|indifferent|no particular preference|all good|I have no preference|it doesn't matter to me|anything)\b"
        }

        self.similar_patterns = {
            "similar": r"\b(similar|like this|like that|looks like|resembling|same as)\b",
        }

        self._done = False

    def _extract_features(self, user_input):
        user_input = user_input.lower()
        update = False

        if self.last_question in self.short_question and self._frame[self.last_question] is None:
            update = self._extract_to_one_slot(user_input, self.last_question)
            return update

        if (("yes" in user_input or "no" in user_input) and not self._first_question) or self._extract_to_one_slot(user_input, "_no_pref"):
            for key, value in self._frame.items():
                if value is None:
                    update = self._extract_to_one_slot(user_input, key)
                    return update

        else:
            update = self._extract_all(user_input)

        return update

    def _extract_to_one_slot(self, user_input, key):
        update = False
        pattern_key = key+"_patterns"
        patterns = getattr(self, pattern_key)
        for type, pattern in patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                self._frame[key] = type
                update = True
                break

        return update

    def _extract_all(self, user_input):
        update = False

        for age, pattern in self.age_patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                self._frame["age"] = age
                update = True
                break

        for activity, pattern in self.activity_level_patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                self._frame["activity_level"] = activity
                update = True
                break

        for size, pattern in self.size_patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                self._frame["size"] = size
                update = True
                break

        for sex, pattern in self.sex_patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                self._frame["sex"] = sex
                update = True
                break

        for hair_length, pattern in self.hair_length_patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                self._frame["hair_length"] = hair_length
                update = True
                break

        for other_pets, pattern in self.other_pets_patterns_wider.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                self._frame["other_pets"] = other_pets
                update = True
                break

        for children, pattern in self.children_patterns_wider.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                self._frame["children"] = children
                update = True
                break

        return update

    def _ask_next_question(self):
        for key, value in self._frame.items():
            if value is None:
                self._first_question = False
                if key in self._control_questions:
                    self.last_question = key
                    return self._control_questions[key], None
                self.last_question = key
                return self._questions[key], None
        self._done = True
        return self._get_dog_from_db()

    def _filter_dogs(self):
        kwargs = {}
        if self._frame.get("age") != 'no_pref':
            age_ranges = {
                "young": (0, 2),
                "adult": (2, 7),
                "senior": (7, 20)
            }
            min_age, max_age = age_ranges[self._frame["age"]]
            kwargs['age__gte'] = min_age
            kwargs['age__lte'] = max_age

        if self._frame.get("activity_level") != 'no_pref':
            kwargs["activity_level"] = self._frame["activity_level"]
        if self._frame.get("size") != 'no_pref':
            kwargs["size"] = self._frame["size"]
        if self._frame.get("sex") != 'no_pref':
            kwargs["sex"] = self._frame["sex"]
        if self._frame.get("hair_length") != 'no_pref':
            kwargs["hair_length"] = self._frame["hair_length"]
        if self._frame.get("other_pets"):
            kwargs["another_pets"] = bool(self._frame["other_pets"])
        if self._frame.get("children"):
            kwargs["children"] = bool(self._frame["children"])

        return Dog.objects.filter(**kwargs)

    def _get_dog_from_db(self):
        control_answers = []
        for key in self._frame:
            if key in self._control_questions:
                control_answers.append(self._frame[key])
        if not all(control_answers):
            self._done = True
            return "We're sorry, but based on your responses, we can't find a dog for you. " \
                    "Adopting a dog is a huge responsibility. A dog requires time and attention. Please contact us.", None
        self._done = True
        dog = self._filter_dogs()
        if len(list(dog)) == 0:
            return "We're sorry, but we couldn't find a perfect match for you. We invite you to view the dogs in our care by clicking the 'See our dogs' button. You might be interested in another one.", None
        if len(list(dog)) > 0:
            dog = list(dog)[0]
        self.dog = dog
        return f"Your dog is: {dog.name}. <br> We invite you to contact us about adoption. We encourage you to arrange a trial walk and meet the dog in person.", dog.name + ".png"

    def _check_if_want_similar(self, user_input):
        for _, pattern in self.similar_patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                return True
        return False


    def handle_input(self, user_input):
        if self._done and self._check_if_want_similar(user_input):
            another_dog_path = serach_for_similar_image('DogTinderApp/static/dogs/' + self.dog.name + ".png")
            photo_name = os.path.basename(another_dog_path)
            new_dog = Dog.objects.get(name=photo_name.split(".")[0])
            self.dog = new_dog
            return True, "Here's a similar dog. His/Her name is: "+photo_name.split(".")[0], photo_name, self._done
        update = self._extract_features(user_input)
        if self._first_question:
            update = True
        if not update and not self._first_question:
            return update, "I don't understand, can you repeat please?", None, self._done
        next_question, photo_name = self._ask_next_question()

        return update, random.choice(self._continue_patterns) + next_question, photo_name, self._done
    
    def reset_frame(self):
        self._done = False
        self.last_question = False
        self._first_question = True
        self._frame = {
            "age": None,
            "activity_level": None,
            "size": None,
            "sex": None,
            "hair_length": None,
            "other_pets": None,
            "children": None,
            "enough_time": None,
            "home_space": None,
            "costs": None, 
            "vacations": None,
        }
