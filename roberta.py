from transformers import pipeline
import pickle
classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

sentences = ["i went to a college and wrote a test,and got average mark so my staff shouted at me"]
model_outputs = classifier(sentences)

# create an iterator object with write permission - model.pkl
with open('model_pkl', 'wb') as files:
    pickle.dump(classifier, files)


