"""Find and display the student or students with the highest total marks."""


def display_topper(students: list[dict]) -> None:
    """Print the name of the class topper, including ties."""
    highest_total = max(student["total"] for student in students)
    toppers = [
        student["name"]
        for student in students
        if student["total"] == highest_total
    ]
    print(f"\nTopper{'s' if len(toppers) > 1 else ''}: {', '.join(toppers)}")
