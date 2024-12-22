prompt_template = """
You are an expert at creating questions based on coding materials and documentation.
Your goal is to prepare a coder or programmer for their exam and coding tests.
You do this by asking questions about the text below:

-----------
{text}
-----------

Create questions that will prepare the coders or programmers for their tests.
Make sure not to lose any important information.

QUESTIONS:
"""


## Refine prompt template
refine_template = ("""
You are an expert at creating practise question based on coding materials and documents.
Your goal is to help a coder or programmer prepare for a coding test.
We have received some pratice questions to a certain extent: {existing_answer}.
We have the option to refine the existing question or add new ones.
(only if necessary) with some more contact context below.

-----------
{text}
-----------
                   
Given the new context refine the original question in English.
If the context is not helpful please provide the original questions.
QUESTIONS:
                   
""")