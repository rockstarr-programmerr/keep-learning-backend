from datetime import timedelta

from .band_score import BAND_SCORE_MAPPER


class ReadingReportMaker:
    def __init__(self, classroom, student):
        self.classroom = classroom
        self.student = student

    def make(self, exercise_pk=None, detail=True):
        reports = []
        exercises = self.get_exercises()

        for exercise in exercises:
            if exercise_pk and exercise_pk != exercise.pk:
                continue

            report = self.new_report(exercise)
            submission = self.get_submission(exercise)

            if submission:
                report['submitted'] = True
                report['time_taken'] = submission.time_taken
                report['submit_datetime'] = submission.submit_datetime

                questions = exercise.questions.all().prefetch_related('answers')
                answers = submission.answers.all()

                passage_1_report = self.passage_report(questions, answers, 1)
                passage_2_report = self.passage_report(questions, answers, 2)
                passage_3_report = self.passage_report(questions, answers, 3)

                report['passage_1_total'], report['passage_1_detail'] = passage_1_report
                report['passage_2_total'], report['passage_2_detail'] = passage_2_report
                report['passage_3_total'], report['passage_3_detail'] = passage_3_report

                report['total'] = (
                    report['passage_1_total'] +
                    report['passage_2_total'] +
                    report['passage_3_total']
                )
                report['band_score'] = self.calculate_band(report['total'])

            if not detail:
                del report['passage_1_detail']
                del report['passage_2_detail']
                del report['passage_3_detail']

            reports.append(report)

        return reports

    @staticmethod
    def new_report(exercise):
        return {
            'exercise': exercise,
            'time_taken': timedelta(seconds=0),
            'submit_datetime': None,
            'passage_1_total': 0,
            'passage_2_total': 0,
            'passage_3_total': 0,
            'passage_1_detail': [],
            'passage_2_detail': [],
            'passage_3_detail': [],
            'total': 0,
            'band_score': 1,
            'submitted': False,
        }

    @staticmethod
    def new_detail():
        return {
            'question_number': None,
            'submitted_answer': '',
            'possible_answers': [],
            'is_correct': False,
        }

    def get_exercises(self):
        return self.classroom.reading_exercises.all().prefetch_related('questions')

    def get_submission(self, exercise):
        return exercise.submissions.filter(submitter=self.student).prefetch_related('answers').first()

    def passage_report(self, questions, answers, passage):
        questions = filter(
            lambda question: getattr(question, f'is_passage_{passage}')(),
            questions
        )

        score = 0
        details = []
        related_answers = []
        related_remains = 0

        for question in questions:
            detail = self.new_detail()
            answer = self.get_answer(answers, question)
            possible_answers = question.get_answers_content()

            detail['question_number'] = question.number
            detail['possible_answers'] = possible_answers

            is_related = len(possible_answers) > 1
            if not is_related:
                related_answers = []
            elif not related_remains:
                related_remains = len(possible_answers)
                related_answers = []

            is_correct = False
            if answer:
                is_correct = question.check_answer(answer.content, related_answers=related_answers)
                if is_correct:
                    score += 1

                detail['submitted_answer'] = answer.content
                detail['is_correct'] = is_correct

            if related_remains:
                related_remains -= 1
                if not related_remains:
                    related_answers = []
                elif answer and is_correct:
                    related_answers.append(answer.content)

            details.append(detail)

        return score, details

    @staticmethod
    def calculate_band(score):
        return BAND_SCORE_MAPPER[score]

    @staticmethod
    def get_answer(answers, question):
        for answer in answers:
            if answer.question_number == question.number:
                return answer
