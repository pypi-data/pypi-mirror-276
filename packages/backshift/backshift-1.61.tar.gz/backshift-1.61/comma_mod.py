
"""Handle commas in a (potentially large) number."""


def gimme_commas(number):
    """Accept a number, return a comma'd string."""
    string = str(number)
    reversed_string = string[::-1]
    commad_reversed_list = []
    for charno, char in enumerate(reversed_string):
        if charno != 0 and charno % 3 == 0:
            commad_reversed_list.append(',')
        commad_reversed_list.append(char)
    commad_list = commad_reversed_list[:]
    commad_list.reverse()
    return ''.join(commad_list)
