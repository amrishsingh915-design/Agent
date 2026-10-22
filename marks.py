"""Collect marks for three students and display a formatted result table."""

from topper import display_topper


SUBJECTS = ("DBMS", "DSA", "OS")
STUDENT_COUNT = 3
MAX_MARKS_PER_SUBJECT = 100


def read_mark(student_name: str, subject: str) -> float:
    """Read and validate one subject mark."""
    while True:
        try:
            mark = float(input(f"Enter {subject} marks for {student_name} (0-100): "))
            if not 0 <= mark <= MAX_MARKS_PER_SUBJECT:
                raise ValueError("Marks must be between 0 and 100.")
        except ValueError as error:
            print(f"Error: {error}")
            continue
        return mark


def grade_for(percentage: float) -> str:
    """Assign a grade using the student's percentage."""
    if percentage >= 90:
        return "O"
    if percentage >= 80:
        return "A+"
    if percentage >= 70:
        return "A"
    if percentage >= 60:
        return "B+"
    return "F"


def main() -> None:
    students = []

    for number in range(1, STUDENT_COUNT + 1):
        name = input(f"\nEnter the name of student {number}: ").strip()
        while not name:
            print("Name cannot be empty.")
            name = input(f"Enter the name of student {number}: ").strip()

        marks = {
            subject: read_mark(name, subject)
            for subject in SUBJECTS
        }
        total = sum(marks.values())
        average = total / len(SUBJECTS)
        percentage = total / (len(SUBJECTS) * MAX_MARKS_PER_SUBJECT) * 100

        students.append(
            {
                "name": name,
                "marks": marks,
                "total": total,
                "average": average,
                "percentage": percentage,
                "grade": grade_for(percentage),
            }
        )

    headers = (
        "Name", *SUBJECTS, "Total", "Average", "Percentage", "Grade"
    )
    rows = [
        (
            student["name"],
            *(f'{student["marks"][subject]:.1f}' for subject in SUBJECTS),
            f'{student["total"]:.1f}',
            f'{student["average"]:.2f}',
            f'{student["percentage"]:.2f}%',
            student["grade"],
        )
        for student in students
    ]
    widths = [
        max(len(header), *(len(row[index]) for row in rows))
        for index, header in enumerate(headers)
    ]
    separator = "-+-".join("-" * width for width in widths)

    print("\nSTUDENT MARKS AND RESULTS")
    print(" | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print(separator)
    for row in rows:
        print(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))

    display_topper(students)


if __name__ == "__main__":
    main()