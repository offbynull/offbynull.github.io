import re

if __name__ == '__main__':
    print("<div style=\"margin:2em; background-color: #e0e0e0;\">", end="\n\n")
    try:
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        lines = filter(lambda l: not re.match(r'^\s*$', l), lines)

        print(f'<strong>↩PREREQUISITES↩</strong>', end='\n\n')
        for line in lines:
            print(f' * {line}', end='\n')
        print(end='\n')
    finally:
        print("</div>", end="\n\n")