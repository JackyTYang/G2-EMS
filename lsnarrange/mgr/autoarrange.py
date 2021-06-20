from common.models import Course
from common.models import ClassRoom

class AutoArrange:
    def __init__(self):
        # ORM 读入数据，转为 list

        qsCourse = Course.objects.values_list("Course_Id", "Course_Capacity", "Course_Range", "Teacher_Id")
        qsClassRoom = ClassRoom.objects.values_list("ClassRoom_Id", "ClassRoom_Capacity")

        self.listCourse = list(qsCourse)
        self.listClassRoom = list(qsClassRoom)
        self.listCourse.sort(key=lambda x:x[1])
        self.listClassRoom.sort(key=lambda x:x[1])

        # 初始化时间池与结果列表
        self.timePool = [-1]*13*7*len(self.listClassRoom)
        self.listResult = [[0 for col in range(4)] for row in range(len(self.listCourse))]

    def confict_teacher(self, teacher_id, time):
        # 检查同一时间点 time 其他教室是否已安排该教师 teacher_id

        base = 7*13
        for i in range(len(self.listClassRoom)):
            other_course=self.timePool[base*i+time]
            if other_course == -1:
                continue
            if self.listCourse[other_course][3]==teacher_id:
                return True
        return False

    def process(self):
        # 进行自动排课
        arranged = True
        for i in range(len(self.listCourse)):
            # 遍历每一堂课
            done = False
            j = 0
            while True:
                if j >= len(self.timePool):
                    break
                room = int(j / (7 * 13))
                # 判断容量是否超出
                if self.listClassRoom[room][1] < self.listCourse[i][1]:
                    j = j + 7 * 13
                    if j >= len(self.timePool):
                        break
                # 遍历所有可以安排的可能
                if self.timePool[j] == -1:
                    # 检查是否可安排
                    courseRange = self.listCourse[i][2]
                    can_insert=True
                    day_in_week = int(int(j % (7*13)) / 13)
                    for k in range(courseRange):
                                # 判断该时间点该教室是否已安排
                                # 判断在同一个教室
                                # 判断在同一天
                                # 判读教师冲突
                        if self.timePool[j+k] != -1 \
                                or int(((j+k) / (7*13))) != room \
                                or int((int((j+k) % (7*13)) / 13)) != day_in_week \
                                or self.confict_teacher(self.listCourse[i][3], int((j+k) % (7*13))):
                            can_insert=False
                            break
                    if can_insert==True:
                        # 可以安排课程
                        for k in range(courseRange):
                            self.timePool[j + k]=i
                        self.listResult[i][0]=self.listCourse[i][0]
                        self.listResult[i][1]=self.listClassRoom[room][0]
                        self.listResult[i][2]=int(j % (7*13))
                        self.listResult[i][3]=self.listResult[i][2]+courseRange-1
                        done=True
                        break
                j = j + 1

            if done == False:
                arranged = False
                break

        return arranged