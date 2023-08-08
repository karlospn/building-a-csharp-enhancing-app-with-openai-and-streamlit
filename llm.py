import openai
import os

xml_comments_prompt = '''
Given a csharp file content, you must add elaborate and high quality XML comments for any method, class, enum or interface. 
Don't add comments on anything else. Exclude anything else when trying to add comments, for example do not try to add XML comments on class properties or class constants.
If any method, class, enum or interface already contains an XML comment, then try to improve it.
You must respond only with the generated csharp code and nothing else.

csharp file content:
{csharp_file_content}
'''

explain_prompt = '''
Explain in an easy and concise way what the given csharp code is doing. 
The response must be in markdown format and contain only a list of bullet points.

csharp code:
{csharp_file_content}
'''

suggestions_prompt = '''
Given a csharp file content, try to suggest no more than 2 or 3 quality code improvements.
Don't mention anything about code comments.
Do not show any source code. Just respond with a list of 2 or 3 suggestions.
If you don't have any suggestion or you don't have enough information, then respond saying only: no suggestions found."

csharp code:
{csharp_file_content}
'''

unit_tests_prompt = '''
Given a csharp file content, try to create some Unit Tests.
Only create Unit Tests if it those might be valuable for the application.
The tests should be using xUnit and Moq.
Follow a naming standard of Given_x_When_y_Then_z.
If you decide that creating the unit tests make sense, then respond only with the generated csharp code and nothing else.
If you decide that creating the unit tests doesn't make sense, then respond saying only: No unit tests available for this file.

csharp file content:
{csharp_file_content}
'''

def generate_xml_comments(code):
    
    prompt = xml_comments_prompt.format(csharp_file_content=code)
    message = _get_messages(prompt)

    response = openai.ChatCompletion.create(
        engine=_get_llm_model(),
        messages = message,
        temperature=0.5,
        max_tokens=8000,
    )

    return response.choices[0].message.content.strip()

def explain_code(code):

    prompt = explain_prompt.format(csharp_file_content=code)
    message = _get_messages(prompt)

    response = openai.ChatCompletion.create(
        engine=_get_llm_model(),
        messages = message,
        temperature=0.5,
        max_tokens=8000,
    )

    return response.choices[0].message.content.strip()

def suggest_code_improvements(code):

    prompt = suggestions_prompt.format(csharp_file_content=code)
    message = _get_messages(prompt)

    response = openai.ChatCompletion.create(
        engine=_get_llm_model(),
        messages = message,
        temperature=0,
        max_tokens=8000,
    )

    return response.choices[0].message.content.strip()

def generate_unit_tests(code):
    
    prompt = unit_tests_prompt.format(csharp_file_content=code)
    message = _get_messages(prompt)

    response = openai.ChatCompletion.create(
        engine=_get_llm_model(),
        messages = message,
        temperature=0.3,
        max_tokens=8000,
    )

    return response.choices[0].message.content.strip()

def _get_llm_model():
    return os.getenv('AZURE_OPENAI_GPT4_MODEL_NAME')

def _get_messages(prompt):
    message = [
        { "role": "system", "content":  "You are an app assistant trying to improve the source code of a csharp file." },
        {"role": "user", "content": prompt}
    ]

    return message