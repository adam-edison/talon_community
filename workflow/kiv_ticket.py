from talon import Module

mod = Module()


def join_ticket_numbers(numbers: list[int]) -> str:
    return ".".join(str(number) for number in numbers)


@mod.capture(rule="<number_small> (dot <number_small>)*")
def kiv_ticket_number(m) -> str:
    """Dotted ticket number such as 1.2.3"""
    return join_ticket_numbers(m.number_small_list)


@mod.capture(rule="kiv <user.kiv_ticket_number>")
def kiv_ticket(m) -> str:
    """Ticket label such as KIV-1.2.3"""
    return f"KIV-{m.kiv_ticket_number}"
