import sys
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def update():
    while True:
        try:
            scam_words = rooter_for_words(input("What's the scam word? ").lower())
            if not scam_words.isalpha():
                raise ValueError
            else:
                with open("/workspaces/123932397/project/scam_words.txt") as file:
                    words = file.read()
                    if scam_words in words:
                        print("word already exists")
                        option = input("Do you want to continue updating? (yes/no) ")
                        if option.lower().strip() == "no":
                            print("Thank you for using our programme.")
                            raise EOFError
                        if option.lower().strip() == "yes":
                            continue
                    else:
                        with open("/workspaces/123932397/project/scam_words.txt", "a") as file:
                            file.write(f"{scam_words}\n")
                        option = input("Word updated. Do you want to continue updating? (yes/no) ")
                        if option.lower().strip() == "no":
                            print("Thank you for using our programme.")
                            raise EOFError
                        if option.lower().strip() == "yes":
                            continue
        except EOFError:
            break
        except ValueError:
            sys.exit("Not a valid input")

def counter(tokens):
    scam_count = 0
    normal_count = 0
    with open("/workspaces/123932397/project/scam_words.txt") as file:
        file_contents = file.read()

    words = file_contents.split()
    #read each line in file, finding which tokens match the text in the each line of the file
    for string in tokens:
        for word in words:
            if string == word:
                scam_count += 1

    normal_count = int(len(tokens)) - int(scam_count)

    return [normal_count, scam_count]

def word_processor(text):
    #to remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    #to remove stopwords
    nltk.download('stopwords',quiet =True)

    stop_words = set(stopwords.words('english'))
    word_tokens = rooter_for_tokens(word_tokenize(text))
    filtered_text = [words for words in word_tokens if not words.lower() in stop_words]
    filtered_text = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_text.append(w)
    return filtered_text


def predict(normal_words, scam_words):
    if normal_words > scam_words:
        accuracy = round((normal_words / (normal_words + scam_words) * 100))
        return f"Your message is likely not a scam, with {accuracy}% certainty"
    elif normal_words == scam_words:
        return f"Your message could be a scam"
    else:
        accuracy = round((scam_words / (normal_words + scam_words) * 100))
        return f"Your message is likely a scam, with {accuracy}% certainty"

def blacklist(email):
    #if text is found to be a scam, store their email
    #use regex email checker to check if input is ok
    return bool(re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email))

def rooter_for_tokens(tokens):
    nltk.download("averaged_perceptron_tagger", quiet =True)
    nltk.download("wordnet", quiet=True)
    lemmatizer = WordNetLemmatizer()
    root_words = []
    for token in tokens:
        pos = nltk.pos_tag([token])[0][1]
        if pos.startswith('V'): # Check if the token is a verb
            root_word = lemmatizer.lemmatize(token, pos='v')
            if root_word == token: # If the token is not a verb in the base form
                root_word = lemmatizer.lemmatize(token, pos='n') # Treat it as a noun and get the base form
            root_word = lemmatizer.lemmatize(root_word, pos='v') # Get the base form of the verb
        elif pos.startswith('N'): # Check if the token is a noun
            root_word = lemmatizer.lemmatize(token, pos='n')
        else:
            root_word = token
        root_words.append(root_word)
    return root_words

def rooter_for_words(word):
    nltk.download("averaged_perceptron_tagger", quiet =True)
    nltk.download("wordnet", quiet=True)
    lemmatizer = WordNetLemmatizer()
    root_words = []
    pos = nltk.pos_tag([word])[0][1]
    if pos.startswith('V'): # Check if the token is a verb
        root_word = lemmatizer.lemmatize(word, pos='v')
        if root_word == word: # If the token is not a verb in the base form
            root_word = lemmatizer.lemmatize(word, pos='n') # Treat it as a noun and get the base form
        root_word = lemmatizer.lemmatize(root_word, pos='v') # Get the base form of the verb
    elif pos.startswith('N'): # Check if the token is a noun
        root_word = lemmatizer.lemmatize(word, pos='n')
    else:
        root_word = word
    root_words.append(root_word)
    return ''.join(root_words)

def main():
    user_input = input("Welcome to Scam Alert! To update scam word databank input 1, to check if your text is a scam input 2. ")
    if user_input == "1":
        update()
    elif user_input == "2":
        message = input("Paste your text here: ").lower()
        processed_w = word_processor(message)
        normal_words, scam_words = counter(processed_w)
        print(predict(normal_words, scam_words))
        if scam_words > normal_words:
            while True:
                email = input("Please input scammers email here to help us blacklist the scammer:")
                if blacklist(email):
                    with open("/workspaces/123932397/project/blacklist_email.txt", "a") as file:
                        file.write(f"{email}\n")
                    print("Thank you for using our programme. Have a nice day!")
                    break
                else:
                    print("Invalid email. Please try again")
        elif scam_words < normal_words:
            print("Considering that your message is likely not a scam, no scammer email will be required, thank you for using our programme. Have a nice day!")

    else:
        sys.exit("Invalid input")

if __name__ == "__main__":
    main()