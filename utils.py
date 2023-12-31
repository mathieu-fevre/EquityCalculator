import random
from itertools import combinations

from card import Card
from deck import Deck
from hand_evaluator import HandEvaluator

NUMBER_OF_SIMULATIONS = 100000

def gen_cards(cards_str):
    return [Card.from_str(s) for s in cards_str]

def gen_cards_from_ids(cards_ids):
    return [Card.from_id(id) for id in cards_ids]

def estimate_hole_card_win_rate(nb_simulation, nb_player, hole_card, community_card=None):
    if not community_card: community_card = []
    win_count = sum([_montecarlo_simulation(nb_player, hole_card, community_card) for _ in range(nb_simulation)])
    return 1.0 * win_count / nb_simulation

def gen_deck(exclude_cards=None):
    deck_ids = range(1, 53)
    if exclude_cards:
        assert isinstance(exclude_cards, list)
        if isinstance(exclude_cards[0], str):
            exclude_cards = [Card.from_str(s) for s in exclude_cards]
        exclude_ids = [card.to_id() for card in exclude_cards]
        deck_ids = [i for i in deck_ids if not i in exclude_ids]
    return Deck(deck_ids)

def evaluate_hand(hole_card, community_card):
    assert len(hole_card)==2 and len(community_card)==5
    hand_info = HandEvaluator.gen_hand_rank_info(hole_card, community_card)
    return {
            "hand": hand_info["hand"]["strength"],
            "strength": HandEvaluator.eval_hand(hole_card, community_card)
            }

def _montecarlo_simulation(nb_player, hole_card, community_card):
    community_card = _fill_community_card(community_card, used_card=hole_card+community_card)
    unused_cards = _pick_unused_card((nb_player-1)*2, hole_card + community_card)
    opponents_hole = [unused_cards[2*i:2*i+2] for i in range(nb_player-1)]
    opponents_score = [HandEvaluator.eval_hand(hole, community_card) for hole in opponents_hole]
    my_score = HandEvaluator.eval_hand(hole_card, community_card)
    if my_score > max(opponents_score):
        return 1
    elif my_score == max(opponents_score):
        return 1.0/opponents_score.count(my_score)
    else:
        return 0

def _fill_community_card(base_cards, used_card):
    need_num = 5 - len(base_cards)
    return base_cards + _pick_unused_card(need_num, used_card)

def _pick_unused_card(card_num, used_card):
    used = [card.to_id() for card in used_card]
    unused = [card_id for card_id in range(1, 53) if card_id not in used]
    choiced = random.sample(unused, card_num)
    return [Card.from_id(card_id) for card_id in choiced]

def equity_calculator(hole_cards_1, hole_cards_2, community_cards=[]):
    count = 0
    for _ in range(NUMBER_OF_SIMULATIONS):
        # if _ % 10000 == 0: print(_)
        community_card = _fill_community_card(community_cards, used_card=hole_cards_1+hole_cards_2+community_cards)
        score_1 = HandEvaluator.eval_hand(hole_cards_1, community_card)
        # a = []
        # for card in community_card:
        #     a.append(card.__str__())
        # print(a)
        score_2 = HandEvaluator.eval_hand(hole_cards_2, community_card)
        if score_1 > score_2:
            count += 1
        elif score_1 == score_2:
            count += 0.5
    return round(float(count)/NUMBER_OF_SIMULATIONS, 4)

def exact_equity_calculator(hole_cards_1, hole_cards_2):
    tot = 0
    id_list = list(range(1,53))
    id_list.remove(hole_cards_1[0].to_id())
    id_list.remove(hole_cards_1[1].to_id())
    id_list.remove(hole_cards_2[0].to_id())
    id_list.remove(hole_cards_2[1].to_id())
    cards_list = [Card.from_id(i) for i in id_list]
    count = 0
    comb_list = combinations(cards_list, 5)
    # print(len(list(comb_list)))
    for comb in comb_list:
        tot +=1
        if not tot % 10000:
            print(tot)
        community_card = list(comb)
        score_1 = HandEvaluator.eval_hand(hole_cards_1, community_card)
        score_2 = HandEvaluator.eval_hand(hole_cards_2, community_card)
        if score_1 > score_2:
            count += 1
        elif score_1 == score_2:
            count += 0.5
    print(count)
    return 100*float(count)/tot
            
            
            
hand1 = [Card.from_str('SA'), Card.from_str('HA')]
hand2 = [Card.from_str('DA'), Card.from_str('SK')]
print(exact_equity_calculator(hand1, hand2))
