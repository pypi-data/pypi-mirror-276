# rocat/template_utils.py

def prompt_template(instruction, constraints, output_format, input_text):
    """ 
    주어진 지시문, 제약 조건, 출력 형식 및 입력 텍스트를 사용하여 프롬프트 템플릿을 생성합니다.
    
    Args:
        instruction (str): 지시문.
        constraints (str): 제약 조건. 콤마로 구분된 문자열.
        output_format (str): 출력 형식.
        input_text (str): 입력 텍스트.
    
    Returns:
        str: 생성된 프롬프트 템플릿.
    """
    constraints = "\n".join(constraints.split(","))
    return f"""
#Instruction\n
{instruction}\n
\n
#Constraints\n
{constraints}\n
\n
#Output_Format\n
{output_format}\n
다른 설명은 출력하지 마세요.
\n
#Input_Text\n
{input_text}
"""
