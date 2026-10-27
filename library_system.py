"""Library loan, fine and renewal tracker."""
import ast
import json
import operator
from datetime import datetime

loans = {}
FINE_PER_DAY = 2
ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
}


def add_book_loan(student_id, book_id, dates=None):
    """Record that a student borrowed a book."""
    if not student_id:
        print("Loan rejected: student id is required")
        return
    if not isinstance(book_id, str):
        print(f"Loan rejected: book id {book_id!r} must be a string")
        return
    if dates is None:
        dates = []
    dates.append(str(datetime.now()))
    loans[student_id] = loans.get(student_id, []) + [book_id]
    print(
        f"{student_id} borrowed {book_id} "
        f"(loan dates on record: {len(dates)})"
    )


def return_book(student_id, book_id):
    """Remove a book from a student's loans."""
    try:
        loans[student_id].remove(book_id)
        if len(loans[student_id]) == 0:
            del loans[student_id]
    except (KeyError, ValueError):
        print(f"No record of {student_id} holding {book_id}")


def calculate_fine(days_overdue):
    """Return the fine for the days overdue (never negative)."""
    return max(days_overdue, 0) * FINE_PER_DAY


def renew_book(student_id, book_id, extra_days):
    """Renew a borrowed book. Renewals do not change the fine rate."""
    if extra_days <= 0:
        print("Renewal rejected: extra days must be positive")
        return
    if book_id not in loans.get(student_id, []):
        print(f"Cannot renew: {student_id} does not hold {book_id}")
        return
    print(f"Renewed {book_id} for {student_id} by {extra_days} days")


def load_records(file="loans.json"):
    """Load loan records from a JSON file into memory."""
    try:
        with open(file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        print(f"No saved records found at {file}")
        return
    loans.clear()
    loans.update(data)


def save_records(file="loans.json"):
    """Save the current loan records to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(loans, handle)


def _eval_node(node, days):
    """Evaluate a parsed fine rule using only safe operations."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id == "days":
        return days
    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPS:
        left = _eval_node(node.left, days)
        right = _eval_node(node.right, days)
        return ALLOWED_OPS[type(node.op)](left, right)
    raise ValueError("Unsupported fine rule")


def fine_from_rule(rule, days):
    """Compute a fine from a rule such as 'days * 2 + 10'."""
    return _eval_node(ast.parse(rule, mode="eval").body, days)


def print_report():
    """Print every student and the books they have borrowed."""
    print("Loan Report")
    for student, books in loans.items():
        print(student, "->", books)


def main():
    """Run a demo of the loan system."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", 4521)  # book id should be a string
    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)
    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))
    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    try:
        print("S102 owes:", calculate_fine(int(days)))
    except ValueError:
        print("Please enter a whole number of days.")
    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()