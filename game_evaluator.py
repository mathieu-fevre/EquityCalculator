from functools import reduce
from itertools import groupby

from .hand_evaluator import HandEvaluator

class GameEvaluator:

    @classmethod
    def judge(self, table):
        winners = self.__find_winners_from(table.get_community_card(), table.seats.players)
        hand_info = self.__gen_hand_info_if_needed(table.seats.players, table.get_community_card())
        prize_map = self.__calc_prize_distribution(table.get_community_card(), table.seats.players)
        return winners, hand_info, prize_map


    @classmethod
    def __find_winners_from(self, community_card, players):
        score_player = lambda player: HandEvaluator.eval_hand(player.hole_card, community_card)
        active_players = [player for player in players if player.is_active()]
        scores = [score_player(player) for player in active_players]
        best_score = max(scores)
        score_with_players = [(score, player) for score, player in zip(scores, active_players)]
        winners = [s_p[1] for s_p in score_with_players if s_p[0] == best_score]
        return winners
