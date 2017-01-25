import csv
import re

def csv_corpus(filename, data_index, size = 0):

    with open(filename, 'rt', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = [(p[data_index]) for p in reader]

    print('Lines in CSV: %d \n' % len(data))

    corp = open((filename[:-4] + '_corp.txt'), 'w', encoding='utf-8')
    for a in data:
        corp.write(a)

    print('Written to file: %s' % (filename[:-4] + '_corp.txt'))


def clean_html(html):

    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()

if __name__ == '__main__':

    csv_corpus('bug_forum.csv', 3)

    with open('bug_forum_corp.txt', 'rt', encoding='utf-8') as file:
        data = file.readlines()
        file.close()

print(type(data))
print(data[:50])

corp = [clean_html(line) for line in data]

print(type(corp))
print(corp[:50])
#    with open('bug_forum_corp_cleaned.txt', 'w', encoding='utf-8') as file:
 #       file.writelines(clean_html(data))
