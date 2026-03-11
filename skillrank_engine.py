
class SkillRankEngine:

    def __init__(self):
        self.total_score = 0

    def analyze(self, curiosity_level):
        score_map = {
            1: 3,
            2: 8,
            3: 15
        }

        score_added = score_map.get(curiosity_level, 3)
        self.total_score += score_added

        return {
            "score_added": score_added,
            "total_score": self.total_score,
            "reason": "curiosity evaluation4"
        }
