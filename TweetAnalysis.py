import json

def average(lst):
    return sum(lst) / len(lst)


with open('assets/jennison.json') as json_file:
    data = json.load(json_file)

tweets = open('assets/tables_JennisonTweets2.txt').read().splitlines()


sentiment = []
positive = []
neutral = []
negative = []

mostPositive = (None,0)
mostNeutral = (None,0)
mostNegative = (None,0)

for doc in data:
    if "documents" in doc:
        for d in doc.get('documents'):
            docId =  int(d.get("id"))
            #Add Sentiment            
            sentiment.append(d.get("sentiment"))

            #Add Positive
            pos = d.get("documentScores").get("positive")
            positive.append(pos)
            if pos > mostPositive[1]:
                mostPositive = (tweets[docId], pos)

            neut = d.get("documentScores").get("neutral")
            neutral.append(neut)
            if neut > mostNeutral[1]:
                mostNeutral = (tweets[docId], neut)

            neg = d.get("documentScores").get("negative")
            negative.append(neg)
            if neg > mostNegative[1]:
                mostNegative = (tweets[docId], neg)

print("\n" + str("#" * 16) + " Most Positive " + str("#" * 16))
print("Tweet: " + mostPositive[0])
print("Sentiment Score: " + str(mostPositive[1]))


print("\n" + str("#" * 16) + " Most Neutral " + str("#" * 16))
print("Tweet: " + mostNeutral[0])
print("Sentiment Score: " + str(mostNeutral[1]))

print("\n" + str("#" * 16) + " Most Negative " + str("#" * 16))
print("Tweet: " + mostNegative[0])
print("Sentiment Score: " + str(mostNegative[1]))

print("\n" + str("#" * 16) + " Average Positive Sentiment " + str("#" * 16))
print(average(positive))

print("\n" + str("#" * 16) + " Average Neutral Sentiment " + str("#" * 16))
print(average(neutral))

print("\n" + str("#" * 16) + " Average Negative Sentiment " + str("#" * 16))
print(average(negative))

print("\n" + str("#" * 16) + " Average Sentiment " + str("#" * 16))
print(max(set(sentiment), key = sentiment.count))
