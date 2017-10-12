def search_rabin_multi(text:str, patterns:list):
    """
    text - строка, в которой выполняется поиск
    patterns = [pattern_1, pattern_2, ..., pattern_n] - массив паттернов, которые нужно найти в строке text
    По аналогии с оригинальным алгоритмом, функция возвращает массив [indices_1, indices_2, ... indices_n]
    При этом indices_i - массив индексов [pos_1, pos_2, ... pos_n], с которых начинаетй pattern_i в строке text.
    Если pattern_i ни разу не встречается в строке text, ему соотвествует пустой массив, т.е. indices_i = []
    """
    work_pattern_indices = set()
    answers = [[] for pat in patterns]
    textset = set(text)
    patternsets = [set(pat) for pat in patterns]
    for i in range(len(patterns)): # Паттерны. алфавит которых не входит в алфавит текста, сразу отметаются
        if not patternsets[i].difference(textset):
            work_pattern_indices.add(i)

    ind = 1
    values = {}
    for sym in textset: # Символам в алфавите присваиваются числовые значения
        values[sym] = ind
        ind += 1
    # Эта версия работает от конца строки к началу. На скорость это влиять не должно.
    pattern_hashes_by_length = {} # Паттерны группируются по длине
    for i in work_pattern_indices:
        revpattern = patterns[i][::-1]
        pattern_hashes_by_length.setdefault(len(revpattern), set()).add((sum([(97 ** z) * values[revpattern[-z-1]] for z in range(0, len(revpattern))]), i))
    # start, end = 0, 0
    current_hash = 0
    worktext = text[::-1]
    for length in pattern_hashes_by_length.keys():
        end = length
        start = 0
        while end <= len(worktext):
            if start == 0:
                current_hash = [(97**z) * values[worktext[-z-1]] for z in range(start, end)]
                current_hash = sum(current_hash)
            else:
                prevlast = values[worktext[-start]]
                if end != len(worktext):
                    nextfirst = values[worktext[-end]]
                else:
                    nextfirst = values[worktext[0]]
                current_hash = (current_hash - prevlast + (nextfirst * 97**length)) / 97
            for hash, index in pattern_hashes_by_length[length]:
                if hash == current_hash:
                    answers[index].append(start)
            start +=1
            end += 1

    return answers

if __name__ == "__main__":
    ans = search_rabin_multi("ktozsubozibojowniciazakonajeho", ["ktoz", "ktozsu", "bo", "jown", "konaje", "jeho", "pravdevitezi", "чаша"])
    print("Done")

