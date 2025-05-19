import re
from ollama import chat
from ollama import ChatResponse

def generate_filter(msg):
    # gemma3:1bb
    response: ChatResponse = chat(model='codellama', messages=[
        {'role': 'system', 'content': """
You are a Python assistant specialized in image processing.
Do not check if the file exists. Do not use try-except.
When the user gives an instruction related to image processing, respond with raw Python code only — just the core lines that perform the operation using only cv2 (OpenCV). Do not include functions or comments.
The code must be a minimal set of executable lines suitable for use with exec().
If the user provides a filename, use it as the input path. If not, use 'image.jpg' as the default input path.
Always load the image using: image = cv2.imread('path')
Always write the result using: cv2.imwrite('path', image)
Never include cv2.imshow, cv2.waitKey, or cv2.destroyAllWindows.
If a filter modifies the image, always assign the result to the same variable: image = cv2.<operation>(image, ...)

Use the correct OpenCV constant for operations that require it.
Always prefer OpenCV constants (e.g., cv2.INTER_LINEAR, cv2.BORDER_REFLECT, cv2.ROTATE_(number)_CLOCKWISE) over plain numbers or strings when applicable.
"""},
        {'role': 'user', 'content': f'{msg}'},
    ])
    return response['message']['content']

def remove_imports(message: str) -> str:
    lines = message.splitlines()
    filtered_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('```'):
            continue
        if re.match(r'^(import|from)\s+', line):
            continue
        if 'cv2.imshow' in line or 'cv2.waitKey' in line:
            continue
        filtered_lines.append(line)
    return '\n'.join(filtered_lines).strip()

def modify_cv2_code(code_str,file_name,ext):
    lines = code_str.strip().split('\n')
    modified_lines = []
    last_assigned_var = None
    imwrite_found = False

    for line in lines:
        line = line.strip()

        # Fix imread path
        if f"cv2.imread(f'{file_name}.{ext}')" in line:
            line = line.replace(f"cv2.imread('{file_name}.{ext}')", f"cv2.imread('images/{file_name}.{ext}')")

        # Track the assigned variable
        if '=' in line and 'cv2.imread' in line:
            last_assigned_var = line.split('=')[0].strip()

        # Fix unassigned operations like Laplacian
        if line.startswith("cv2.") and '=' not in line and last_assigned_var or not line.startswith(f'{last_assigned_var}'):
            if last_assigned_var:
                line = f"{last_assigned_var} = {line}"

        # Fix imwrite to use correct path and variable
        if 'cv2.imwrite' in line:
            imwrite_found = True
            line = f"cv2.imwrite('Image_processing_bot/images/output.jpg', {last_assigned_var})"

        modified_lines.append(line)

    # If imwrite is missing, add it at the end
    if not imwrite_found and last_assigned_var:
        modified_lines.append(f"cv2.imwrite('images/output.jpg', {last_assigned_var})")

    return '\n'.join(modified_lines)


def generate_code(msg,file_name,ext):
    response = generate_filter(msg)
    filtered_response = remove_imports(response)
    filtered_response = modify_cv2_code(filtered_response,file_name,ext)
    return filtered_response
