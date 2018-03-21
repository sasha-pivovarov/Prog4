from pattern.web import Wikipedia, plaintext
from string import punctuation
import re
from collections import Counter
from pprint import pprint



class WikiParser:
    def __init__(self):
        self.wiki = Wikipedia(language="en")
        pstring = punctuation.replace(".", "")
        self.punc = re.compile('[%s]' % re.escape(pstring))


    def get_articles(self, start, depth, max_count):
        iterations = 0
        links = [start]
        list_of_strings = []
        while iterations <= depth and len(list_of_strings) <= max_count:
            links_temp = []
            for link in links:
                if iterations <= depth and len(list_of_strings) <= max_count:
                    try:
                        article = self.wiki.article(link)
                        text = self.process(article.plaintext())
                        new_links = article.links
                        list_of_strings.append(text)
                        links_temp.extend(new_links)
                        print(f"Processed link {link}")
                    except AttributeError:
                        print(f"Skipped link {link}")
                        continue
                else:
                    break
            links = links_temp
            iterations += 1

        return list_of_strings

    def process(self, text):
        tokens = text.split(" ")
        return " ".join([self.punc.sub("", x.lower().strip()) for x in tokens])


class TextStatistics:
    def __init__(self, articles):
        self.articles = articles

    def get_top_3grams(self, n, use_idf=True):
        words = list(" ".join(self.articles))
        trigrams = Counter(zip(words, words[1:], words[2:]))
        if use_idf:
            trigrams = {key: value*self.get_idf(key) for key, value in trigrams.values()}
        sorted_items = sorted(trigrams.items(), key=lambda x: x[1], reverse=True)[:n]
        list_of_3grams_in_descending_order_by_freq = [x[0] for x in sorted_items]
        list_of_their_corresponding_freq = [x[1] for x in sorted_items]
        return list_of_3grams_in_descending_order_by_freq, list_of_their_corresponding_freq

    def get_top_words(self, n, use_idf=True):
        words = Counter(" ".join(self.articles).split())
        if use_idf:
            words = {key: value*self.get_idf(key) for key, value in words.values()}
        sorted_items = sorted(words.items(), key=lambda x: x[1], reverse=True)[:n]
        list_of_words_in_descending_order_by_freq = [x[0] for x in sorted_items]
        list_of_their_corresponding_freq = [x[1] for x in sorted_items]
        return list_of_words_in_descending_order_by_freq, list_of_their_corresponding_freq

    def get_idf(self, word_or_trigram):
        count = 0
        for article in self.articles:
            if word_or_trigram in article:
                count += 1
        try:
            idf = 1.0 / count
            return idf
        except ZeroDivisionError:
            return 0


class Experiment:
    def __init__(self, start="Natural language processing"):
        parser = WikiParser()
        articles = parser.get_articles(start, 1, 100)
        stats_full = TextStatistics(articles)
        stats_start = TextStatistics([articles[0]])
        top_start = stats_start.get_top_3grams(5), stats_start.get_top_words(5)
        top_full = stats_full.get_top_3grams(20), stats_full.get_top_words(20)
        self.results = {"start_3grams": top_start[0], "start_words": top_start[1],
                        "full_3grams": top_full[0], "full_words": top_full[1]}

    def show_results(self):
        print("Top trigrams from entire corpus with counts:\n")
        pprint(self.results["full_3grams"])
        print("Top trigrams from seed article:\n")
        pprint(self.results["start_3grams"])
        print("Top words from entire corpus:\n")
        pprint(self.results["full_words"])
        print("Top words from seed article:\n")
        pprint(self.results["start_words"])

    # Top trigramsfrom entire corpus with counts:
    #
    # ([('from', 'the', 'original'),
    #   ('archived', 'from', 'the'),
    #   ('natural', 'language', 'processing'),
    #   ('the', 'original', 'on'),
    #   ('the', 'use', 'of'),
    #   ('the', 'european', 'union'),
    #   ('of', 'the', 'european'),
    #   ('one', 'of', 'the'),
    #   ('a', 'b', 'c'),
    #   ('as', 'well', 'as'),
    #   ('the', 'number', 'of'),
    #   ('proceedings', 'of', 'the'),
    #   ('cambridge', 'university', 'press'),
    #   ('for', 'example', 'the'),
    #   ('such', 'as', 'the'),
    #   ('university', 'press', 'isbn'),
    #   ('the', 'united', 'states'),
    #   ('a', 'number', 'of'),
    #   ('the', 'end', 'of'),
    #   ('part', 'of', 'the')],
    #  [210,
    #   203,
    #   167,
    #   162,
    #   153,
    #   147,
    #   133,
    #   131,
    #   131,
    #   125,
    #   103,
    #   99,
    #   98,
    #   93,
    #   92,
    #   91,
    #   83,
    #   81,
    #   77,
    #   77])

    # Top trigrams from seed article:
    #
    # ([('natural', 'language', 'processing'),
    #   ('a', 'chunk', 'of'),
    #   ('chunk', 'of', 'text'),
    #   ('of', 'natural', 'language'),
    #   ('systems', 'based', 'on')],
    #  [7, 6, 6, 5, 4])

    # Top words from entire corpus:
    #
    # (['the',
    #   'of',
    #   'and',
    #   'in',
    #   'a',
    #   'to',
    #   'is',
    #   'for',
    #   'as',
    #   'that',
    #   'are',
    #   'language',
    #   'on',
    #   'by',
    #   'or',
    #   'with',
    #   'be',
    #   'from',
    #   'an',
    #   'it'],
    #  [20958,
    #   13690,
    #   9916,
    #   8877,
    #   8865,
    #   7098,
    #   5198,
    #   3648,
    #   3456,
    #   2898,
    #   2608,
    #   2588,
    #   2297,
    #   2240,
    #   2111,
    #   2056,
    #   1955,
    #   1783,
    #   1693,
    #   1598])

    # Top words from seed article:
    #
    # (['of', 'the', 'a', 'and', 'in'], [152, 148, 83, 73, 57])

if __name__ == "__main__":
    exp = Experiment()
    exp.show_results()