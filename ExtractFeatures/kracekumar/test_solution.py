import re

class Stack(object):
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def is_empty(self):
        return not self.items
    def remove(self, item):
        self.items.remove(item)

def striptag(t):
    if '/' in t: # closing tag
        return t[2:-1]
    else:
        return t[1:-1]

def solve(text):
    # Just check if there is a missing < or >
    if (text.count("<") != text.count(">")):
        return "bad character in tag name"

    # regex search for tags (greedy)
    tags = re.compile(r'<.*?>')
    all_tags = tags.findall(text)
    all_tags.reverse()
    tag_stack = Stack()

    for tag in all_tags:
        c = striptag(tag)
        if len(c) > 10 or len(c) == 0:
            return "too many/few characters in tag"

        # if not find upper case alphabetic character
        # bad character in tag name
        reg = re.compile(r'[A-Z]*')
        match = reg.match(c)
        if not match.group():
            return "bad character in tag name"

        tag_stack.push(tag)

    while not tag_stack.is_empty():
        tag = tag_stack.pop()
        if tag.startswith("</"):
            return "no matching begin tag"
        end_tag = "</" + striptag(tag) + ">"
        if not end_tag in tag_stack.items:
            return "expected %s" % end_tag
        else:
            tag_stack.remove(end_tag)

    return "OK"


if __name__ == '__main__':
    tc = 1
    N = int(raw_input())
    while N:
        content = []
        for line in range(N):
            content.append(raw_input())
        input_html = "\n".join(content)
        result = solve(input_html)
        print "Case #%d: %s" % (tc, result)
        tc += 1
        N = int(raw_input())

