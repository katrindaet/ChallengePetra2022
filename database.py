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



