from .band_score import BAND_SCORE_MAPPER


class ReadingReportMaker:
    def __init__(self, classroom, student):
        self.classroom = classroom
        self.student = student

    def make(self):
        reports = []
        exercises = self.get_exercises()

        for exercise in exercises:
            report = self.new_report(exercise)
            submission = self.get_submission(exercise)

            if submission:
                report['submitted'] = True
                questions = exercise.questions.all()
                answers = submission.answers.all()

                report['passage_1'] = self.calculate_score(questions, answers, 1)
                report['passage_2'] = self.calculate_score(questions, answers, 2)
                report['passage_3'] = self.calculate_score(questions, answers, 3)
                report['total'] = report['passage_1'] + report['passage_2'] + report['passage_3']
                report['band_score'] = self.calculate_band(report['total'])

            reports.append(report)

        return reports

    @staticmethod
    def new_report(exercise):
        return {
            'exercise': exercise.identifier,
            'passage_1': 0,
            'passage_2': 0,
            'passage_3': 0,
            'total': 0,
            'band_score': 1,
            'submitted': False,
        }

    def get_exercises(self):
        return self.classroom.reading_exercises.all().prefetch_related('questions')

    def get_submission(self, exercise):
        return exercise.submissions.filter(submitter=self.student).prefetch_related('answers').first()

    def calculate_score(self, questions, answers, passage):
        questions = filter(
            lambda question: getattr(question, f'is_passage_{passage}')(),
            questions
        )

        score = 0
        for question in questions:
            answer = self.get_answer(answers, question)
            if answer:
                is_correct = question.check_answer(answer.content)
                if is_correct:
                    score += 1

        return score

    @staticmethod
    def calculate_band(score):
        return BAND_SCORE_MAPPER[score]

    @staticmethod
    def get_answer(answers, question):
        for answer in answers:
            if answer.question_number == question.number:
                return answer
