# gui_utils.py
def validate_input(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False
