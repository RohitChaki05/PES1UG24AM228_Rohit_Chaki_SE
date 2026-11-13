def parse_order(text):
    if not isinstance(text, str) or ":" not in text:
        raise ValueError("Invalid order format, expected size:copies")
    parts = text.split(":", 1)
    size = parts[0].strip()
    copies_str = parts[1].strip()
    if not copies_str.isdigit():
        raise ValueError("Copies must be an integer")
    return size.upper(), int(copies_str)


def file_size_average(sizes_csv):
    if not isinstance(sizes_csv, str) or not sizes_csv.strip():
        raise ValueError("Invalid CSV input")
    try:
        values = [int(r.strip()) for r in sizes_csv.split(",") if r.strip()]
    except ValueError:
        raise ValueError("All file sizes must be integers")
    if not values:
        raise ValueError("Empty value list")
    return sum(values) // len(values)


def payable_amount(text):
    if not isinstance(text, str) or "|" not in text:
        raise ValueError("Invalid format, expected amount|discount")
    parts = text.split("|", 1)
    try:
        amount = float(parts[0].strip())
        discount = float(parts[1].strip())
    except ValueError:
        raise ValueError("Amount and discount must be numeric")
    total = amount * 1.18 - discount
    return max(total, 0.0)


def main():
    print("==== Running parse_order ====")
    try:
        user_input = input("Enter print size:copies (e.g. 4x6:25): ")
        result = parse_order(user_input)
        print("Size and Copies:", result)
    except Exception as e:
        print("Error:", e)

    print("\n==== Running file_size_average ====")
    try:
        user_input = input("Enter file sizes in MB as CSV (e.g. 4,8,12): ")
        result = file_size_average(user_input)
        print("Average File Size:", result)
    except Exception as e:
        print("Error:", e)

    print("\n==== Running payable_amount ====")
    try:
        user_input = input("Enter amount|discount (e.g. 450|50): ")
        result = payable_amount(user_input)
        print("Payable Amount:", result)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()