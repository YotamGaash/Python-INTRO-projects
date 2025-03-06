import copy

import hangman_helper
##############################################################
#helek a'
#1.
def update_word_pattern(word, pattern, letter):
    pattern_lst = list(pattern)
    for i in range(len(word)):
        if word[i] == letter:
            pattern_lst[i]= letter
        else:
            continue
    return ''.join(pattern_lst)
##############################################################
#2.
def start_of_a_game(words_list):
    game_word = hangman_helper.get_random_word(words_list)
    # print(game_word)      DONT PRINT ANYTHING GON!
    # worng_guess_lst= []
    game_pattern= ''
    for i in range(len(game_word)):
        game_pattern +="_"
    return game_word, game_pattern
           # worng_guess_lst
##############################################################
#vaibility
def check_input_terms(player_input, worng_guess_lst, game_word):
    # if letter[0]== "!"and letter[1].isnumeric()== True:
        if player_input.isalpha() and player_input.islower() and (len(player_input) ==1 or len(player_input)== len(game_word)):
            if worng_guess_lst != []:
                for i in worng_guess_lst:
                    if i == player_input:
                        # print("You alrady inserct this letter")
                        return False
                return player_input

            return player_input
        else:
            # print( "hell you enter letters like shittt")
            return False
##############################################################
#Correct guess?
def check_guess_letter(game_word, player_input,):
    times_input_ocure_in_the_word= game_word.count(player_input)
    if times_input_ocure_in_the_word == 0:
        # print("well you suck at guessing")
        return False, times_input_ocure_in_the_word
    else:
        return True, times_input_ocure_in_the_word

def check_guess_word(game_word, player_input, game_pattern):
    times_input_ocure_in_the_word= game_pattern.count("_")
    if player_input == game_word:
        # print("GOD DAMN THAT GUESS")
        return True, times_input_ocure_in_the_word
    else:
        return False, times_input_ocure_in_the_word
##############################################################
# clac
def clac_score_letter(currunt_score, input_hit_status, times_input_ocure_in_the_word):
    currunt_score += -1
    if input_hit_status == True:
        times_input_ocure_in_the_word = (times_input_ocure_in_the_word * (times_input_ocure_in_the_word + 1)) // 2
        return currunt_score + times_input_ocure_in_the_word
    else:
        return currunt_score

def clac_score_word(currunt_score, input_hit_status, times_underline_in_game_pattern):
    currunt_score += -1
    if input_hit_status == True:
        times_underline_in_game_pattern = (times_underline_in_game_pattern * (times_underline_in_game_pattern + 1)) // 2
        return currunt_score + times_underline_in_game_pattern
    else:
        return currunt_score
##############################################################
#mid game func is the main func of the game
def mid_of_a_game(game_word, game_pattern, score, words_list ,worng_guess_lst):
    """
    this function is the mid of the game and does most of the game
    :param game_word: word
    :param game_pattern: patterv
    :param score: fgfgf
    :param worng_guess_lst:
    :return:
    """
    turn_counter= 1
    while  score > 0:
        hangman_helper.display_state(game_pattern, worng_guess_lst, score,f"this is your {turn_counter} turn")
        player_input_status, player_input=hangman_helper.get_input()
        if  player_input_status == 1:
            if check_input_terms(player_input, worng_guess_lst, game_word) == False:
                continue
            else:
                turn_counter += 1
                # this part does that
                player_guess_status, times_input_ocure_in_the_word_l =  check_guess_letter(game_word, player_input)
                score= clac_score_letter(score, player_guess_status, times_input_ocure_in_the_word_l)
                game_pattern = update_word_pattern(game_word, game_pattern, player_input)
                if player_guess_status == False:
                     worng_guess_lst.append(player_input)
        elif player_input_status ==2:
            if check_input_terms(player_input, worng_guess_lst, game_word) == False:
                continue
            else:
                turn_counter += 1
                player_guess_status, times_input_ocure_in_the_word_w= check_guess_word(game_word, player_input, game_pattern)
                score= clac_score_word(score, player_guess_status,times_input_ocure_in_the_word_w)
                if player_guess_status== True:
                    return True, score
        elif player_input_status ==3:
            turn_counter += 1
            score += -1
            # new_words_list= filter_words_list(words_list, game_pattern, worng_guess_lst)
            hangman_helper.show_suggestions(check_hints_words_lst(filter_words_list(words_list, game_pattern, worng_guess_lst),hangman_helper.HINT_LENGTH ))
        if game_word == game_pattern:
            return True, score
    return False, score

#########################################################################################################
#end of the game func
# ver 1
# def end_of_a_game(player_game_satus, game_word, score):
#     if player_game_satus == True:
#         print("you won, your score is", score)
#     else:
#         print("YOU LOST")
#         print("well that suck but the word was---->", game_word)

#ver 2
def end_of_a_game_seo(score):
    game_counter=1
    end_game_status = hangman_helper.play_again(f"You erned {score} in run of {game_counter} game/s!")
    if end_game_status == True:
        game_counter += 1
        return True
    else:
        return False

####################################################################################################
#helek b'
def filter_words_list(words, pattern, wrong_guess_lst):
    #try_to_excpe_from_out_loop= need to take care of it
    new_words_list= copy.copy(words)
    for i in words:
##############################################################next line is about the first term
        try_to_excpe_from_out_loop_counter = 0
        if len(i) != len(list(pattern)):
            new_words_list.remove(i)
            continue
##############################################################next line is about the thried term
        for j in wrong_guess_lst:
            if j in i:
                new_words_list.remove(i)
                try_to_excpe_from_out_loop_counter += 1
                break
##############################################################next line is about the secoand term
        if try_to_excpe_from_out_loop_counter == 0:
            for k in range(len(pattern)):
                if pattern[k] == "_":
                    continue
                else:
                    if i[k] == pattern[k]:
                        new_words_list.remove(i)
                        break
        else:
            continue
    return new_words_list

# x= hangman_helper.load_words()
# print(filter_words_list(x, "ab__d___", ["v", "x", "w"]))
# ####################################################################################
#list words filters: 1 by 1
# def filter_len_words(words, pattern):
#     for i in words:
#         if len(i) != len(pattern):
#             words.remove(i)
#     return words
#
#
# def filter_wrong_guess_words(words, worng_guess_lst):
#     for i in range(len(words)):
#         for j in worng_guess_lst:
#             if j in words[i]:
#                 del words[i]
#
#     return words
#
#     # for i in words:
#     #     for j in worng_guess_lst:
#     #         if j in i:
#     #             words.remove(i)
#     #
#     # return words
#
# def filter_wtfterm_words(words, pattern):
#     for i in words:
#         for k in range(len(pattern)):
#             if pattern[k] == "_":
#                 continue
#             else:
#                 if i[k] == pattern[k]:
#                     words.remove(i)
#     return words
###########################################################################
def check_hints_words_lst(words_list, hint_length):
    light_words_list=[]
    append_counter= copy.copy(hint_length)
    if len(words_list) > hint_length:
        while len(light_words_list) != hint_length:
            light_words_list.append(words_list[
                (hint_length- append_counter)*len(words_list)//hint_length
            ])
            append_counter += -1
        return light_words_list
        # light_words_list.append(words_list[0])
        # light_words_list.append(words_list[len(words_list)//])
    else:
         return words_list


 # x= ['aardvark','aardwolf','aaron','aback','abacus','abaft']
 # print(check_hints_words_lst(x))
###########################################################################################################################################################################
#main and run singel game func

def run_single_game(words_list, score):
    game_word, game_pettern = start_of_a_game(words_list)
    lost_win_status, score = mid_of_a_game(game_word, game_pettern, score, words_list ,[])
    #this end game lane is for ver 1 not ver 2. the ver2 ther is no end game in run single game but for every end of a game seoson.
    # end_of_a_game(lost_win_status, game_word, score )
    return score




def main():
    words_list = hangman_helper.load_words()
    end_game_status = True
    # score= 0
    score = hangman_helper.POINTS_INITIAL
    game_counter = 0
    while end_game_status == True :
        game_counter += 1
        score = run_single_game(words_list, score)
        end_game_status= end_of_a_game_seo(score)
        if end_game_status == True:
            continue
        else:
            print("well hoop you had fun, your score was", score)
            break

if __name__ == "__main__":
    main()