def generate_questions(request, data):
    return 
    questions = []
    types = ["multichoices", ]
    
    for _ in range(number_of_question):
        question = get_random_question(type_of_question, chapter_span)
        question.difficulty = random.randint(average_difficulties - 2, average_difficulties + 2)
        questions.append(question)

    duration = calculate_duration(questions)
    while duration < minimum_duration or duration > maximum_duration:
        questions.pop()
        duration = calculate_duration(questions)

    return questions

def get_random_question(type_of_question, chapter_span):

    question = None
    while question is None:
        question = random.choice(get_questions_by_type(type_of_question, chapter_span))
        if question.chapter_span != chapter_span:
            question = None

    return question

def get_questions_by_type(type_of_question, chapter_span):

    questions = []
    for question in get_all_questions():
        if question.type == type_of_question and question.chapter_span == chapter_span:
            questions.append(question)

    return questions
