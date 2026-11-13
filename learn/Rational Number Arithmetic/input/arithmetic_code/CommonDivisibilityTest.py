from __future__ import annotations

from typing import Set

from Output import log, log_indent, log_unindent
from WholeNumber import WholeNumber


#MARKDOWN_CDT
def common_divisibility_test(num: WholeNumber) -> Set[WholeNumber]:
    log_indent()
    try:
        ret: Set[WholeNumber] = set()
    
        last_digit: WholeNumber = WholeNumber.from_digit(num.digits[0])  # last digit is always at 0 idx
    
        log(f'Testing if {num} divisible by 2...')
        if last_digit == WholeNumber.from_int(0) \
                or last_digit == WholeNumber.from_int(2) \
                or last_digit == WholeNumber.from_int(4) \
                or last_digit == WholeNumber.from_int(6) \
                or last_digit == WholeNumber.from_int(8):
            log(f'Yes')
            ret.add(WholeNumber.from_int(2))
        else:
            log(f'No')
    
        log(f'Testing if {num}  divisible by 5...')
        if last_digit == WholeNumber.from_int(0) \
                or last_digit == WholeNumber.from_int(5):
            log(f'Yes');
            ret.add(WholeNumber.from_int(5))
        else:
            log(f'No');
    
        log(f'Testing if {num}  divisible by 10...')
        if last_digit == WholeNumber.from_int(0):
            log(f'Yes');
            ret.add(WholeNumber.from_int(10))
        else:
            log(f'No');
    
        log(f'Testing if {num} divisible by 3...')
        reduced_num: WholeNumber = num.copy()
        while True:
            digits = reduced_num.digits
            if len(digits) == 1:
                break
            reduced_num = sum([WholeNumber.from_int(d) for d in digits], WholeNumber.from_int(0))
    
        if reduced_num == WholeNumber.from_int(3) \
                or reduced_num == WholeNumber.from_int(6) \
                or reduced_num == WholeNumber.from_int(9):
            log(f'Yes')
            ret.add(WholeNumber.from_int(3))
        else:
            log(f'No')
    
        log(f'Testing if {num}  divisible by 6...')
        if WholeNumber.from_int(2) in ret and WholeNumber.from_int(3) in ret:
            log(f'Yes')
            ret.add(WholeNumber.from_int(6))
        else:
            log(f'NO')
    
        return ret
    finally:
        log_unindent()
#MARKDOWN_CDT


if __name__ == '__main__':
    print(f'{common_divisibility_test(WholeNumber.from_int(15))}')
