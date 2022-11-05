import json
import itertools

class Database:
  def __init__(self, filepath):
    file = open(filepath)
    self.data = json.load(file)

  def contexts(self):
    context_list = [key for key in self.data['Contexts']]
    return context_list

  def sentences(self, context):
    sentence_list = self.data['Contexts'][context]
    return sentence_list  # returns a list containing all the sentences corresponding to this context

  def sentences_containing(self, prefix):
    sentence_list = [sentence for sentence in itertools.chain.from_iterable(self.data['Contexts'].values()) if sentence.startswith(prefix)]
    return sentence_list  #returns a list containing the sentences that start with the given prefix

  def replace_sentence(self, context, old_sentence, new_sentence):
    self.data['Contexts'][context][self.data['Contexts'][context].index(old_sentence)] = new_sentence

    with open('sentences.json', 'w') as f:
      json.dump(self.data, f)

  def add_new_context(self, new_context):
    self.data['Contexts'][new_context] = []
    with open('sentences.json', 'w') as f:
      json.dump(self.data, f)

  def add_new_sentence(self, context, new_sentence):
    self.data['Contexts'][context].append(new_sentence)

    with open('sentences.json', 'w') as f:
      json.dump(self.data, f)