import random
from itertools import combinations

# 설정값 입력
group_allocate = (4, 4, 4, 4)
L = sum(group_allocate)

# group_distribute
group_distribute = []
for i, g in enumerate(group_allocate):
    group_distribute += [i] * group_allocate[i]

# P_matrix 미리 구해놓기
P_matrix = []
for i in range(4):
    row = []
    for j in range(4):
        if i == j:
            row.append(1 + 0.125 / (group_allocate[i] * group_allocate[j]))
        elif (i-j) % 2 == 0:
            row.append(2.125 / (group_allocate[i] * group_allocate[j]))
        else:
            row.append(0.625 / (group_allocate[i] * group_allocate[j]))
    P_matrix.append(row)

# 참가 신청팀 입력하기 : team_dic = {0 : [-1, "힐조", "이동길", "이소현"], 1 : [-1, ....}
team_dic = dict()
with open("teams.txt", 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        team_dic[i] = [-1] + list(line.split())

# result.txt 만들기
W = open("result.txt", 'w', encoding='utf-8')

# 각 클럽별 딕셔너리 : club_dic = {"힐조" : [0, 1, 3, 7], "부산" : [4, 6], ....}
club_dic = dict()
for i in range(L):
    club =  team_dic[i][1]
    if club not in club_dic:
        club_dic[club] = []
    club_dic[club].append(i)

# 랜덤하게 5000번 실행하여 최소 기대값 구하기
min_expectation_value = 1000
for k in range(5000):
    random.shuffle(group_distribute) # 섞자
    for i, rnd in enumerate(group_distribute): # 섞은 값을 team_dic의 조번호(0~3) 항목(디폴트는 -1)에 대입
        team_dic[i][0] = rnd
    expectation_value = 0
    for club_name in club_dic.keys():
        if len(club_dic[club_name]) < 2:
            continue
        pairs = combinations(club_dic[club_name], 2)
        for pair in pairs:
            expectation_value += P_matrix[team_dic[pair[0]][0]][team_dic[pair[1]][0]]
    if expectation_value < min_expectation_value:
        min_expectation_value = expectation_value
        W.write(f"{k:>4}번째 실행까지 최소 기대값은 {min_expectation_value:0.20f}\n")

# 최소 기대값에 해당하는 대진표 랜덤하게 1000개 뽑기
count = 0
while count < 1000:
    random.shuffle(group_distribute) # 섞자
    for i, rnd in enumerate(group_distribute): # 섞은 값을 team_dic의 조번호(0~3) 항목(디폴트는 -1)에 대입
        team_dic[i][0] = rnd
    expectation_value = 0
    for club_name in club_dic.keys():
        if len(club_dic[club_name]) < 2:
            continue
        pairs = combinations(club_dic[club_name], 2)
        for pair in pairs:
            expectation_value += P_matrix[team_dic[pair[0]][0]][team_dic[pair[1]][0]]
    if expectation_value <= min_expectation_value:
        W.write(f"<대진표 후보 번호 {count:>4}>\n")
        for group_num in range(4):
            ABCD = chr(ord('A') + group_num)
            W.write(f"    {ABCD}조 :")
            temp = []
            for team_num in range(L):
                if team_dic[team_num][0] == group_num:
                    temp.append(team_num)
            random.shuffle(temp)
            for team_num in temp:
                W.write(f"  [{team_dic[team_num][1]:>2}] {team_dic[team_num][2]:>3} / {team_dic[team_num][3]:>3}")
            W.write("\n")
        count += 1
        

W.close()


# [3, 0, 1, 2, 0, 2, 2, 1, 0, 3, 2, 0, 3, 1]