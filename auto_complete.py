from fast_autocomplete import autocomplete_factory
import json

class auto_complete:
    def __init__(self,dataset_path):
        self.dataset = dataset_path
        with open(self.dataset) as json_file:
            self.data = json.load(json_file)
        content_files = {
            'words': {
                'filepath': self.dataset,
                'compress': True  # means compress the graph data in memory
            }
        }
        self.autocomplete = autocomplete_factory(content_files=content_files)


    def predict(self, word_prefix):
        predict = self.autocomplete.search(word=word_prefix)
        return [words[0] for words in predict]

    #if text_field has a space after (word finished)
    def increment_count(self, word):
        self.autocomplete.update_count_of_word(word=word, count=self.autocomplete.get_count_of_word(word)+1)
        self.data[word] =[{ }, "", self.autocomplete.get_count_of_word(word)]


    def save_json(self):
        with open(self.dataset, "w") as outfile:
            json.dump(self.data, outfile)

