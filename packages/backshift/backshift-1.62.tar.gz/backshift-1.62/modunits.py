#!/usr/bin/env python3

"""Convert computer-friendly numbers to human-readable numbers with units at various levels of detail."""

# if you want to use me as a python module, please rename me to modunits.py
# if you want to use me as a standalone executable, please rename me to modunits
# if you want to use me as both, please name me whatever and symlink :)

import re
import sys
import typing


def builtins() -> typing.List[str]:
    """Legal options for builtin varieties of modular units."""
    list_ = ['computer-size', 'computer-bit-seconds', 'computer-byte-hours', 'time']
    list_.sort()
    return list_


def detail_options() -> typing.List[str]:
    """Legal options for what level of detail we want."""
    list_ = ['list', 'string-list', 'highest', 'two-highest', 'highest-and-fraction', 'all']
    list_.sort()
    return list_


def units_type() -> typing.List[str]:
    """Legal options for abbreviation or not."""
    list_ = ['unabbreviated', 'abbreviated']
    list_.sort()
    return list_

# This one is very primitive class usage - it's basically just a struct, IE, no methods to speak of.  Using tuples and lists was
# getting too messy - this is much more descriptive


class Type(object):
    """Hold data about whether we should output units abbreviated or unabbreviated, and what to divide by (?)."""

    # pylint: disable=R0903
    # R0903: We don't need a lot of public methods; we're just a container

    def __init__(self, threshold: typing.Optional[int], unabbreviated: str, abbreviated: str) -> None:
        """Initialize."""
        self.threshold = threshold
        self.unabbreviated = unabbreviated
        self.abbreviated = abbreviated


class Item(object):
    """Hold one of the modular pieces of our number."""

    # pylint: disable=R0903
    # R0903: We don't need a lot of public methods
    def __init__(self, amount: float, type_: Type, after: bool, units: str, fractional_part_length: int) -> None:
        """Initialize."""
        # pylint: disable=R0913
        # R0913: We need a number of arguments; I'd make them named-only if this didn't need to run on older python's
        self.amount = amount
        self.type_ = type_
        self.after = after
        self.units = units
        self.fractional_part_length = fractional_part_length

    # this handles units and before/after, but not things like commas or the detail level.  Comma processing and detail level
    # processing will build on this

    def __str__(self):
        """Return a string version."""
        str_amount = str(self.amount)
        if '.' in str_amount and self.fractional_part_length >= 1:
            fields = str_amount.split('.')
            if len(fields) == 2:
                # slow but simple
                while len(fields[1]) > self.fractional_part_length:
                    fields[1] = fields[1][:-1]
                while len(fields[1]) < self.fractional_part_length:
                    fields[1] += '0'
                str_amount = '%s.%s' % (fields[0], fields[1][0:self.fractional_part_length])
        if self.units == 'unabbreviated':
            unit = self.type_.unabbreviated
        elif self.units == 'abbreviated':
            unit = self.type_.abbreviated
        else:
            sys.stderr.write('%s: Internal error: Illegal value for units\n' % sys.argv[0])
            usage(1)
        if self.after:
            if self.units == 'abbreviated':
                str_amount += unit
            else:
                str_amount += ' ' + unit
        else:
            str_amount = unit + ': ' + str_amount
        return str_amount


def modunits(
        unitsvector: typing.Union[str, typing.List[Type]],
        number: int,
        detail: str = 'highest-and-fraction',
        units: str = "abbreviated",
        comma: bool = True,
        reverse: bool = False,
        after: bool = True,
        fractional_part_length: int = -1,
):
    # pylint: disable=R0913
    # R0913: We need a number of arguments; I'd make them named-only if this didn't need to run on older python's
    """
    Convert a number with computer-friendly units into something more human-readable.

    Main entry point for the module.

    detail can be:
            list (implies that we will ignore units and comma)
            highest (implies that we will ignore comma)
            two-highest
            highest-and-fraction (default)
            all
    units can be:
            unabbreviated
            abbreviated (default)
    comma can be:
            0 (default)
            1
    reverse can be:
            0 (default)
            1
    after can be:
            0 (default)
            1

    time expects seconds
    computer-size-iec expects bytes (http://en.wikipedia.org/wiki/Zettabyte)
    computer-size and computer-size-si are the same thing.  They expect bytes (see wikipedia URL above)
    computer-bit-seconds and computer-bits-per-second-iec are the same thing.  They both expect bits/second
    computer-bits-per-second-si expects bits/second
    computer-byte-hours and computer-bytes-per-hour-iec are the same thing.  They both expect bytes/hour
    computer-bytes-per-hour-si expects bytes/hour
    """
    iec_fundament = 2 ** 10
    si_fundament = 10 ** 3

    internalvector = unitsvector
    if isinstance(internalvector, str):
        if internalvector == 'time':
            internalnumber = number
            internalvector = [
                Type(60, 'seconds', 's'),
                Type(60, 'minutes', 'm'),
                Type(24, 'hours', 'h'),
                Type(365, 'days', 'da'),
                Type(100, 'years', 'y'),
                Type(None, 'centuries', 'c'),
            ]
        elif internalvector in ['computer-size-iec']:
            internalnumber = number
            internalvector = [
                Type(iec_fundament, 'bytes', 'B'),
                Type(iec_fundament, 'kibibytes', 'Ki'),
                Type(iec_fundament, 'mebibytes', 'Mi'),
                Type(iec_fundament, 'gibibytes', 'Gi'),
                Type(iec_fundament, 'tebibytes', 'Ti'),
                Type(iec_fundament, 'pebibytes', 'Pi'),
                Type(iec_fundament, 'exbibytes', 'Ei'),
                Type(iec_fundament, 'zebibytes', 'Zi'),
                Type(None, 'yobibytes', 'Yi'),
            ]
        elif internalvector in ['computer-size', 'computer-size-si']:
            internalnumber = number
            internalvector = [
                Type(si_fundament, 'bytes', 'B'),
                Type(si_fundament, 'kilobytes', 'k'),
                Type(si_fundament, 'megabytes', 'M'),
                Type(si_fundament, 'gigabytes', 'G'),
                Type(si_fundament, 'terabytes', 'T'),
                Type(si_fundament, 'petabytes', 'P'),
                Type(si_fundament, 'exabytes', 'E'),
                Type(si_fundament, 'zettabytes', 'Z'),
                Type(None, 'yottabytes', 'Y'),
            ]
        elif internalvector in ['computer-bit-seconds', 'computer-bits-per-second-iec']:
            internalnumber = number
            internalvector = [
                Type(iec_fundament, 'bits/s', 'b/s'),
                Type(iec_fundament, 'kibibits/second', 'ki/s'),
                Type(iec_fundament, 'mebibits/second', 'mi/s'),
                Type(iec_fundament, 'gibibits/second', 'gi/s'),
                Type(iec_fundament, 'tebibits/second', 'ti/s'),
                Type(iec_fundament, 'pebibits/second', 'pi/s'),
                Type(iec_fundament, 'exbibits/second', 'ei/s'),
                Type(iec_fundament, 'zebibits/second', 'zi/s'),
                Type(None, 'yobibits/second', 'yi/s'),
            ]
        elif internalvector in ['computer-bits-per-second-si']:
            internalnumber = number
            internalvector = [
                Type(si_fundament, 'bits/s', 'b/s'),
                Type(si_fundament, 'kilobits/second', 'k/s'),
                Type(si_fundament, 'megabits/second', 'm/s'),
                Type(si_fundament, 'gigabits/second', 'g/s'),
                Type(si_fundament, 'terabits/second', 't/s'),
                Type(si_fundament, 'petabits/second', 'p/s'),
                Type(si_fundament, 'exabits/second', 'e/s'),
                Type(si_fundament, 'zettabits/second', 'z/s'),
                Type(None, 'yottabits/second', 'y/s'),
            ]
        elif internalvector in ['computer-byte-hours', 'computer-bytes-per-hour-iec']:
            internalnumber = number
            internalvector = [
                Type(iec_fundament, 'bytes/hour', 'B/hr'),
                Type(iec_fundament, 'kibibytes/hour', 'Ki/hr'),
                Type(iec_fundament, 'mebibytes/hour', 'Mi/hr'),
                Type(iec_fundament, 'gibibytes/hour', 'Gi/hr'),
                Type(iec_fundament, 'tebibytes/hour', 'Ti/hr'),
                Type(iec_fundament, 'pebibytes/hour', 'Pi/hr'),
                Type(iec_fundament, 'exbibytes/hour', 'Ei/hr'),
                Type(iec_fundament, 'zebibytes/hour', 'Zi/hr'),
                Type(None, 'yobibytes/hour', 'Yi/hr'),
            ]
        elif internalvector in ['computer-bytes-per-hour-si']:
            internalnumber = number
            internalvector = [
                Type(si_fundament, 'bytes/hour', 'B/hr'),
                Type(si_fundament, 'kilobytes/hour', 'k/hr'),
                Type(si_fundament, 'megabytes/hour', 'M/hr'),
                Type(si_fundament, 'gigabytes/hour', 'G/hr'),
                Type(si_fundament, 'terabytes/hour', 'T/hr'),
                Type(si_fundament, 'petabytes/hour', 'P/hr'),
                Type(si_fundament, 'exabytes/hour', 'E/hr'),
                Type(si_fundament, 'zettabytes/hour', 'Z/hr'),
                Type(None, 'yottabytes/hour', 'Y/hr'),
            ]
        else:
            sys.stderr.write('Sorry, I do not have a predefined units vector called %s\n' % unitsvector)
            sys.exit(1)
    assert isinstance(internalvector, list)
    return _chopit(internalvector, internalnumber, detail, units, comma, reverse, after, fractional_part_length)


def _chopit(
        list_: typing.List[Type],
        number: int,
        detail: str,
        units: str,
        comma: int,
        reverse: int,
        after: bool,
        fractional_part_length: int,
):
    # pylint: disable=R0912,R0913
    # R0912: We need a few branches
    # R0913: We need a number of arguments; I'd make them named-only if this didn't need to run on older python's
    """Compute our list of numbers."""
    temp = number
    remainder = 0
    item_list: typing.List[Item] = []
    for element in list_:
        if temp == 0:
            break
        if element.threshold is None:
            (quotient, remainder) = 0, temp
        else:
            (quotient, remainder) = divmod(temp, element.threshold)
        item_list.append(Item(int(remainder), element, after, units, fractional_part_length))
        if element.threshold is None:
            break
        temp = quotient

    # handle the "0" case a little bit specially here, to avoid special cases below
    if not item_list:
        item_list.append(Item(0, list_[0], after, units, fractional_part_length))

    # at this point, item_list should be a list of parts of the number, from least significant to most
    if detail == 'string-list':
        # pretty simple, and probably the easiest to build on :)  Just returns the list we built
        return [str(item) for item in item_list]
        # return early - don't fall through
    elif detail == 'list':
        # pretty simple, and probably the easiest to build on :)  Just returns the list we built
        return item_list
        # return early - don't fall through
    elif detail == 'highest':
        # chop off all but the most significant term - least significant are in the low-numbered list elements
        while item_list[1:]:
            del item_list[0]
        # and fall through
    elif detail == 'two-highest':
        # chop off all but the most significant two terms - least
        # significant are in the low-numbered list elements
        while item_list[2:]:
            del item_list[0]
        # and fall through
    elif detail == 'highest-and-fraction':
        # this one's pretty different from the others, so we handle it
        # here, entirely, rather than falling through for further
        # processing.  we create a single "item" (of type item_class) that
        # will hold the whole number + fraction for the most and 2nd most
        # signficant items.  Then we return it immediately.
        item = item_list[-1]
        if item_list[1:]:
            # if we have at least two elements, then use the second from the end for the fraction
            assert item_list[-2].type_.threshold is not None
            item.amount += item_list[-2].amount / item_list[-2].type_.threshold
        return str(item)
        # return early - don't fall through
    elif detail == 'all':
        # don't need to do anything for this one yet :)
        pass
        # and fall through
    else:
        sys.stderr.write('%s: Internal error: Illegal detail level %s in modunits.py\n' % (sys.argv[0], detail))

#    print '3 detail level is',detail
    # note that even detail == 'highest' works with this code
    if reverse:
        # and the units move right alone with the numbers
        item_list.reverse()

    if comma:
        separator = ', '
    else:
        separator = ' '

    return separator.join(str(item) for item in item_list)


def usage(retval: int) -> None:
    """Give usage message to user."""
    sys.stderr.write(
        'Usage: %s [-h] -t type [-d detail] [-u unitstype] [-c] [-r] [-a] [-s] [-n number] [-D digits]\n' % (sys.argv[0], )
    )
    sys.stderr.write('-h\t\tgive this help message\n')
    sys.stderr.write('-t type\t\tSpecify the type of numbers to be reformatted.  Required.\n')
    sys.stderr.write('\t\tCurrently legal values are:\n')
    for type_ in builtins():
        sys.stderr.write('\t\t\t%s\n' % type_)
    sys.stderr.write('-d detail\tSpecify the type of numbers to be reformatted\n')
    sys.stderr.write('\t\tCurrently legal values are:\n')
    for detail in detail_options():
        sys.stderr.write('\t\t\t%s\n' % detail)
    sys.stderr.write('-u unitstype\tSpecify if units should be abbreviated or spelled out in full\n')
    sys.stderr.write('\t\tCurrently legal values are:\n')
    for units in units_type():
        sys.stderr.write('\t\t\t%s\n' % units)
    sys.stderr.write('-c\t\tseparate with commas\n')
    sys.stderr.write('-r\t\toutput in reverse\n')
    sys.stderr.write('-a\t\tput the units after the numbers, not before.  A bit shorter\n')
    sys.stderr.write('-n number\tSpecify a number to be reformatted.  Can be repeated\n')
    sys.stderr.write('-s\t\tRead numbers from stdin\n')
    sys.stderr.write('\n')
    sys.stderr.write('-D\t\tNumber of digits to output after a decimal point (ignored for all but -d highest-and-fraction)\n')
    sys.stderr.write('\n')
    sys.stderr.write('You can specify both -s and -n, but if you do, the -n numbers\n')
    sys.stderr.write('\twill be processed before the numbers read from stdin.\n')
    sys.stderr.write('\n')
    sys.stderr.write('Or in your python, "import modunits"\n')
    sys.exit(retval)


class Options(object):
    # pylint: disable=R0902
    # R0902: We are primarily a container; we need some instance attributes
    """Hold, parse and verify command line options."""

    def __init__(self) -> None:
        """Initialize."""
        self.from_stdin = 0
        self.from_argv = 0
        self.numbers: typing.List[float] = []
        self.units = ''
        self.detail = 'highest-and-fraction'
        self.units = "abbreviated"
        self.comma = False
        self.reverse = False
        self.after = False
        self.type_ = ''
        self.fractional_part_length = -1

    def parse_argv(self, argv: typing.List[str]) -> None:
        # pylint: disable=R0912
        # R0912: We need a few branches
        """Dissect our argv into something useful."""
        while argv[1:]:
            if argv[1] in ['-h', '--help']:
                usage(0)
            elif argv[1] == '-t' and argv[2:]:
                self.type_ = argv[2]
                del argv[1]
            elif argv[1] == '-d' and argv[2:]:
                if argv[2] in detail_options():
                    self.detail = argv[2]
                else:
                    sys.stderr.write('%s: Illegal detail spec %s\n' % (argv[0], argv[2]))
                    usage(1)
                del argv[1]
            elif argv[1] == '-u' and argv[2:]:
                if argv[2] in units_type():
                    self.units = argv[2]
                else:
                    sys.stderr.write('%s: Illegal units spec %s\n' % (argv[0], argv[2]))
                    usage(1)
                del argv[1]
            elif argv[1] == '-c':
                self.comma = True
            elif argv[1] == '-r':
                self.reverse = True
            elif argv[1] == '-a':
                self.after = True
            elif argv[1] == '-s':
                self.from_stdin = 1
            elif argv[1] == '-n' and argv[2:]:
                self.from_argv = 1
                whole_number_string = re.sub(r'\.[0-9]*$', '', argv[2])
                if int(whole_number_string) == float(argv[2]):
                    self.numbers.append(int(whole_number_string))
                else:
                    self.numbers.append(float(argv[2]))
                del argv[1]
            elif argv[1] == '-D' and argv[2:]:
                self.fractional_part_length = int(argv[2])
                del argv[1]
            else:
                sys.stderr.write('%s: Illegal option %s\n' % (argv[0], argv[1]))
                usage(1)
            del argv[1]

    def check_options(self) -> None:
        """Verify that the options specified make sense."""
        if self.type_ == '':
            sys.stderr.write('%s: -t is a required option\n' % sys.argv[0])
            usage(1)

        if not self.from_argv and not self.from_stdin:
            sys.stderr.write('%s: Warning: You probably want to specify either -s -or -n\n' % sys.argv[0])


def main() -> None:
    """Convert to human-readable form of units."""
    options = Options()
    options.parse_argv(sys.argv)
    options.check_options()

    if options.from_argv:
        for number in options.numbers:
            print(modunits(
                options.type_,
                int(number),
                options.detail,
                options.units,
                options.comma,
                options.reverse,
                options.after,
                options.fractional_part_length,
            ))

    if options.from_stdin:
        for line in sys.stdin:
            print(modunits(
                options.type_,
                int(line),
                options.detail,
                options.units,
                options.comma,
                options.reverse,
                options.after,
                options.fractional_part_length,
            ))

    sys.exit(0)


if __name__ == '__main__':
    main()
