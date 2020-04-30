class FightRecorder:
    fight_result_list = []

    def append(self, fight_result: bool):
        self.fight_result_list.append(fight_result)
        return len(self.fight_result_list)

    def print_recorder(self):
        win_count = self.fight_result_list.count(True)
        fail_count = self.fight_result_list.count(False)
        win_rate = round(win_count / len(self.fight_result_list))
        print('关卡战斗次数累计：%d. 失败次数累计: %d. 胜率: %d.' % (win_count, fail_count, win_rate))

    def get_total_count(self):
        return len(self.fight_result_list)

    def get_last_fail_count(self):
        count = 0
        for i in range(len(self.fight_result_list), -1, -1):
            if self.fight_result_list[i]:
                return count
            else:
                count += 1
