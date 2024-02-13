import time


class BreachProtocolSolver:
    def __init__(self, matrix, buffer_size, sequences, rewards):
        self.matrix = matrix
        self.buffer_size = buffer_size
        self.sequences = sequences
        self.rewards = rewards
        self.buffer = []

    def is_valid_sequence(self, sequence):
        if len(sequence) < 2:
            return False
        for i in range(len(sequence) - 1):
            token1 = sequence[i]
            token2 = sequence[i + 1]
            if abs(token1[0] - token2[0]) + abs(token1[1] - token2[1]) != 1:
                return False
        return True

    def calculate_reward(self, sequence):
        reward = 0
        for seq, rew in zip(self.sequences, self.rewards):
            if seq == sequence:
                reward += rew
        return reward

    def find_sequences(self):
        Nbuffer = self.buffer_size
        Matrix_Width = len(self.matrix)
        Matrix_Height = len(self.matrix[0])
        Matrix = self.matrix
        NSequence = len(self.sequences)
        arrSequence = self.sequences
        arrPoint = self.rewards

        max_reward, token_result, coordinate_result, elapsed_time = find(Nbuffer, Matrix_Width, Matrix_Height, matrix, NSequence, arrSequence, arrPoint)

        if max_reward == 0:
            print("Tidak ada solusi optimal yang ditemukan.")
        else:
            print(max_reward)
            print(' '.join(token_result))
            for i, coor in enumerate(coordinate_result):
                print(f"{coor[0]}, {coor[1]}")
            print(f"{int(elapsed_time * 1000)} ms")
            save_solution = input("Apakah ingin menyimpan solusi? (y/n) ")
            if save_solution.lower() == 'y':
                self.save_solution(max_reward, token_result, coordinate_result, elapsed_time)

    def save_solution(self, max_reward, token_result, coordinate_result, elapsed_time):
        with open("solution6.txt", "w") as file: #BUAT SECARA MANUAL NAMA FILE UNTUK MENYIMPAN SOLUSI NYA
            file.write(f"{max_reward}\n")
            file.write(' '.join(token_result) + "\n")
            for coor in coordinate_result:
                file.write(f"{coor[0]}, {coor[1]}\n")
            file.write(f"{int(elapsed_time * 1000)} ms\n")



def read_matrix_from_file(filename):
    matrix = []
    with open(filename, 'r') as file:
        buffer_size = int(file.readline().strip())
        matrix_width, matrix_height = map(int, file.readline().strip().split())
        print("Matrix Height:", matrix_height)
        print("Matrix:")
        for _ in range(matrix_height):
            row = file.readline().strip().split()
            row = [token for token in row]
            matrix.append(row)
            print(" ".join(row))
        number_of_sequences = int(file.readline().strip())
        print("Number of Sequences:", number_of_sequences)
        sequences = []
        rewards = []
        for _ in range(number_of_sequences):
            sequence = tuple(file.readline().strip().split())
            sequences.append(sequence)
            reward = int(file.readline().strip())
            rewards.append(reward)
        print("Sequences:", sequences)
        print("Rewards:", rewards)
    return matrix, buffer_size, sequences, rewards

def find(Nbuffer, Matrix_Width, Matrix_Height, matrix, NSequence, arrSequence, arrPoint):
    start = time.time()

    buff = Nbuffer

    coorAll = []

    coorRoot = []

    for i in range (0, Matrix_Width):
        coorRoot += [[[0, i]]]

    coorAll += coorRoot

    for i in range (1, buff):
        coorNew = []
        if i % 2 == 1:
            for coor in coorRoot :
                path = []
                path += coor
                abs, oor = coor[len(coor)-1][0], coor[len(coor)-1][1]
                for j in range (0, Matrix_Height):
                    path += [[j, oor]]
                    coorNew.append(path.copy()) 
                    path = path[:-1]

        if i % 2 == 0:
            for coor in coorRoot :
                path = []
                path += coor
                abs, oor = coor[len(coor)-1][0], coor[len(coor)-1][1]
                for j in range (0, Matrix_Width):
                    path += [[abs, j]]
                    coorNew.append(path.copy())  
                    path = path[:-1]

        coorAll += coorNew
        coorRoot = coorNew

    remove = []

    toRemove = 0

    for seq in coorAll:


        total = 0
        for coor in seq:
            for i in range (0, len(seq)):
                if coor == seq[i]:
                    total += 1
        if total > len(seq):
            remove.append(toRemove)
        toRemove += 1

    for j in range (len(remove)-1, -1, -1):
        coorAll.pop(remove[j])

    pointAll = [0] * len(coorAll)

    for i in range (0, len(coorAll)):
        for j in range (0, NSequence):
            if (len(coorAll[i]) >= len(arrSequence[j])):
                for k in range (0, len(coorAll[i]) - len(arrSequence[j]) + 1):
                    status = 0
                    for l in range (0, len(arrSequence[j])):
                        if (matrix[coorAll[i][k+l][0]][coorAll[i][k+l][1]] == arrSequence[j][l]):
                            status += 1
                    if (status == len(arrSequence[j])):
                        pointAll[i] += arrPoint[j]

    max = 0
    loc = 0
    tokenRes = []
    coorRes = []

    for i in range (0, len(pointAll)):
        if pointAll[i] > max:
            max = pointAll[i]
            loc = i

    step = len(coorAll[loc])

    for i in range (0, step):
        tokenRes.append(matrix[coorAll[loc][i][0]][coorAll[loc][i][1]])
        coorRes.append(coorAll[loc][i])
        coorRes[i][0], coorRes[i][1] = coorRes[i][1]+1,coorRes[i][0]+1

    end = time.time()
    elapsedTime = end - start

    return max, tokenRes, coorRes, elapsedTime

if __name__ == "__main__":
    matrix_file = "matriks6.txt" #MASUKKAN NAMA FILE YANG SUDAH BERADA DI DIRECTORY YANG SAMA
    matrix, buffer_size, sequences, rewards = read_matrix_from_file(matrix_file)
    solver = BreachProtocolSolver(matrix, buffer_size, sequences, rewards)
    solver.find_sequences()
