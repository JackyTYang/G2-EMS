from common.models import Course
from common.models import ClassRoom


class AutoArrange:
    def __init__(self, isfirst):
        # ORM 读入数据，转为 list
        if isfirst:
            qsCourseLong = Course.objects.filter(Course_Term=12).values_list("Course_id", "Course_Capacity", "Course_Range",
                                                                             "Teacher_Id")
            qsCourseShort1 = Course.objects.filter(Course_Term=1).values_list("Course_id", "Course_Capacity",
                                                                              "Course_Range", "Teacher_Id")
            qsCourseShort2 = Course.objects.filter(Course_Term=2).values_list("Course_id", "Course_Capacity",
                                                                          "Course_Range", "Teacher_Id")
        else:
            qsCourseLong = Course.objects.filter(Course_Term=34).values_list("Course_id", "Course_Capacity",
                                                                             "Course_Range",
                                                                             "Teacher_Id")
            qsCourseShort1 = Course.objects.filter(Course_Term=3).values_list("Course_id", "Course_Capacity",
                                                                              "Course_Range", "Teacher_Id")
            qsCourseShort2 = Course.objects.filter(Course_Term=4).values_list("Course_id", "Course_Capacity",
                                                                              "Course_Range", "Teacher_Id")

        qsClassRoom = ClassRoom.objects.values_list("ClassRoom_id", "ClassRoom_Capacity")

        self.listCourseLong = list(qsCourseLong)
        self.listCourseShort1 = list(qsCourseShort1)
        self.listCourseShort2 = list(qsCourseShort2)

        self.listClassRoom = list(qsClassRoom)

        self.listCourseLong.sort(key=lambda x: x[1])
        self.listCourseShort1.sort(key=lambda x: x[1])
        self.listCourseShort2.sort(key=lambda x: x[1])

        self.listClassRoom.sort(key=lambda x: x[1])

        # 初始化时间池与结果列表
        self.timePool1 = [-1] * 13 * 7 * len(self.listClassRoom)

        self.listResult = [[0 for col in range(4)] for row in
                           range(len(self.listCourseLong) + len(self.listCourseShort1) + len(self.listCourseShort2))]
        self.pointer = 0

    def confict_teacher(self, teacher_id, time, pool, m_list):
        # 检查同一时间点 time 其他教室是否已安排该教师 teacher_id

        base = 7 * 13
        for i in range(len(self.listClassRoom)):
            other_course = pool[base * i + time]
            if other_course == -1:
                continue
            if m_list[other_course][3] == teacher_id:
                return True
        return False

    def _process(self, pool, m_list):
        arranged = True
        for i in range(len(m_list)):
            # 遍历每一堂课
            done = False
            j = 0
            while True:
                if j >= len(pool):
                    break
                room = int(j / (7 * 13))
                # 判断容量是否超出
                if self.listClassRoom[room][1] < m_list[i][1]:
                    j = j + 7 * 13
                    if j >= len(pool):
                        break
                # 遍历所有可以安排的可能
                if pool[j] == -1:
                    # 检查是否可安排
                    courseRange = m_list[i][2]
                    can_insert = True
                    day_in_week = int(int(j % (7 * 13)) / 13)
                    for k in range(courseRange):
                        # 判断该时间点该教室是否已安排
                        # 判断在同一个教室
                        # 判断在同一天
                        # 判读教师冲突
                        if pool[j + k] != -1 \
                                or int(((j + k) / (7 * 13))) != room \
                                or int((int((j + k) % (7 * 13)) / 13)) != day_in_week \
                                or self.confict_teacher(m_list[i][3], int((j + k) % (7 * 13)), pool, m_list):
                            can_insert = False
                            break
                    if can_insert == True:
                        # 可以安排课程
                        for k in range(courseRange):
                            pool[j + k] = i
                        self.listResult[self.pointer][0] = m_list[i][0]
                        self.listResult[self.pointer][1] = self.listClassRoom[room][0]
                        self.listResult[self.pointer][2] = int(j % (7 * 13))
                        self.listResult[self.pointer][3] = self.listResult[i][2] + courseRange - 1
                        self.pointer = self.pointer + 1
                        done = True
                        break
                j = j + 1

            if done == False:
                arranged = False
                break

        return arranged

    def process(self):
        # 进行自动排课
        arranged = self._process(self.timePool1, self.listCourseLong)
        self.timePool2 = self.timePool1.copy()
        arranged = arranged and self._process(self.timePool1, self.listCourseShort1)
        arranged = arranged and self._process(self.timePool2, self.listCourseShort2)
        return arranged
