class ReadingReportMaker:
    def __init__(self, classroom, student):
        self.classroom = classroom
        self.student = student

    def make(self):
        return {'success': True}
