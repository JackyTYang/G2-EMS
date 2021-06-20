from common.models import Course
from common.models import ClassRoom

class AutoArrange:
    def __init__(self):
        # ORM 读入数据，转为 list

        qsCourse = Course.objects.values("Course_Id", "Course_Capacity", "Course_Range", "Teacher_Id")[0:3]
        qsClassRoom = ClassRoom.objects.values("ClassRoom_Id", "ClassRoom_Capacity")[0:1]
        self.listCourse = list(qsCourse)
        self.listClassRoom = list(qsClassRoom)
        self.listCourse.sort(key=(lambda x:x[1]), reverse=True)
        self.listClassRoom.sort(key=(lambda x:x[1]), reverse=True)

        # 初始化时间池与结果列表
        self.timePool = [-1]*13*7*len(self.listClassRoom)
        self.listResult = [[0] * 4]*len(self.listCourse)

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
            for j in range(len(self.timePool)):
                # 遍历所有可以安排的可能
                if self.timePool[j] == -1:
                    # 检查是否可安排
                    courseRange = self.listCourse[i][2]
                    can_insert=True
                    room = int(j / len(self.listClassRoom))
                    day_in_week = int((j % len(self.listClassRoom)) / 7)
                    for k in range(courseRange):
                                # 判断该时间点该教室是否已安排
                                # 判断在同一个教室
                                # 判断在同一天
                                # 判读教师冲突
                        if self.timePool[j+k] == True \
                                or int(((j+k) / len(self.listClassRoom))) != room \
                                or int(((j % len(self.listClassRoom)) / 7)) != day_in_week \
                                or self.confict_teacher(self.listCourse[i][3], (j % len(self.listClassRoom))):
                            can_insert=False
                            break
                    if can_insert==True:
                        # 可以安排课程
                        for k in range(courseRange):
                            self.timePool[j + k]=i
                        self.listResult[i][0]=self.listCourse[i][0]
                        self.listResult[i][1]=self.listClassRoom[room][0]
                        self.listResult[i][2]=int(((j % len(self.listClassRoom)) / 7))
                        self.listResult[i][3]=self.listResult[i][2]+courseRange-1
                        done=True

            if done == False:
                arranged = False
                break

        return arranged