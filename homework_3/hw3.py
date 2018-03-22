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
            trigrams = {key: value*self.get_idf("".join(key)) for key, value in trigrams.items()}
        sorted_items = sorted(trigrams.items(), key=lambda x: x[1], reverse=True)[:n]
        list_of_3grams_in_descending_order_by_freq = [x[0] for x in sorted_items]
        list_of_their_corresponding_freq = [x[1] for x in sorted_items]
        return list_of_3grams_in_descending_order_by_freq, list_of_their_corresponding_freq

    def get_top_words(self, n, use_idf=True):
        words = Counter(" ".join(self.articles).split())
        if use_idf:
            words = {key: value*self.get_idf(key) for key, value in words.items()}
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
        articles = parser.get_articles(start, 1, 15)
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

    # Top
    # trigrams
    # from entire corpus
    # with counts:
    #
    # ([(' ', 't', 'h'),
    #   ('t', 'h', 'e'),
    #   ('h', 'e', ' '),
    #   (' ', 'i', 'n'),
    #   ('i', 'n', 'g'),
    #   ('e', 'd', ' '),
    #   (' ', 'o', 'f'),
    #   ('i', 'o', 'n'),
    #   ('o', 'f', ' '),
    #   (' ', 'a', 'n'),
    #   ('t', 'i', 'o'),
    #   ('o', 'n', ' '),
    #   ('a', 't', 'i'),
    #   ('n', 'g', ' '),
    #   ('e', 's', ' '),
    #   ('a', 'n', 'd'),
    #   ('n', 'd', ' '),
    #   ('i', 'n', ' '),
    #   (' ', 'c', 'o'),
    #   ('e', 'r', ' ')],
    #  [355.4375,
    #   326.3125,
    #   261.75,
    #   172.125,
    #   170.5625,
    #   166.8125,
    #   159.5,
    #   158.8125,
    #   152.0,
    #   150.0625,
    #   143.6875,
    #   141.75,
    #   137.5,
    #   134.0,
    #   126.9375,
    #   126.625,
    #   126.25,
    #   125.75,
    #   113.75,
    #   107.875])
    # Top
    # trigrams
    # from seed article:
    #
    # ([(' ', 't', 'h'),
    #   ('t', 'h', 'e'),
    #   ('i', 'n', 'g'),
    #   (' ', 'o', 'f'),
    #   ('i', 'o', 'n')],
    #  [226.0, 203.0, 198.0, 163.0, 156.0])
    # Top
    # words
    # from entire corpus:
    #
    # (['the',
    #   'of',
    #   'and',
    #   'in',
    #   'a',
    #   'arabic',
    #   'turing',
    #   'turings',
    #   'to',
    #   'is',
    #   'varieties',
    #   'dialects',
    #   'pronunciation',
    #   'for',
    #   'hodges',
    #   'arabic.',
    #   'as',
    #   'agglutinative',
    #   'that',
    #   'bletchley'],
    #  [248.9375,
    #   151.4375,
    #   105.3125,
    #   104.1875,
    #   97.5,
    #   93.5,
    #   88.25,
    #   88.0,
    #   84.4375,
    #   61.0625,
    #   53.0,
    #   50.0,
    #   44.0,
    #   43.875,
    #   41.0,
    #   41.0,
    #   39.5,
    #   37.0,
    #   35.25,
    #   32.0])
    # Top
    # words
    # from seed article:
    #
    # (['of', 'the', 'a', 'and', 'in'], [152.0, 148.0, 83.0, 73.0, 57.0])


if __name__ == "__main__":
    exp = Experiment()
    exp.show_results()