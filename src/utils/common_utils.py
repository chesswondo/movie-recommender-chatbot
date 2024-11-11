def extract_between(text: str, start: str, end: str):
    # Find the start and end positions
    start_idx = text.find(start) + len(start)
    end_idx = text.find(end, start_idx)
    
    # Extract the substring if both start and end are found
    if start_idx != -1 and end_idx != -1:
        return text[start_idx:end_idx]
    else:
        return text